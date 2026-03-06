# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Dokploy CLI — dynamically generated from the OpenAPI spec."""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx

DEFAULT_BASE_URL = os.environ.get("DOKPLOY_URL", "").rstrip("/") or None
CACHE_DIR = Path.home() / ".cache" / "dokploy"
CACHE_TTL = 3600  # 1 hour


def load_token(org: str) -> str:
    key = f"DOKPLOY_{org.upper()}"
    token = os.environ.get(key)
    if token:
        return token
    result = subprocess.run(
        ["fnox", "get", key], capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: failed to get {key} from fnox: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def fetch_spec(base_url: str, token: str) -> dict:
    with httpx.Client(timeout=30) as client:
        resp = client.get(
            f"{base_url}/settings.getOpenApiDocument",
            headers={"x-api-key": token},
        )
        resp.raise_for_status()
        return resp.json()


def get_spec(org: str, base_url: str, token: str, refresh: bool = False) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{org.lower()}_openapi.json"

    if not refresh and cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < CACHE_TTL:
            return json.loads(cache_file.read_text())

    spec = fetch_spec(base_url, token)
    cache_file.write_text(json.dumps(spec))
    return spec


def openapi_type_to_python(schema: dict) -> tuple[type | None, str]:
    """Return (python_type, description_suffix) from an OpenAPI schema."""
    t = schema.get("type")
    if t == "integer":
        return int, ""
    if t == "number":
        return float, ""
    if t == "boolean":
        return None, ""  # handled as store_true
    if t == "array":
        return str, " (JSON array)"
    if t == "object":
        return str, " (JSON object)"
    return str, ""


def build_endpoint_parser(subparsers, path: str, method: str, details: dict):
    """Add a subcommand for a single endpoint."""
    cmd_name = path.lstrip("/")
    desc = details.get("summary", details.get("description", f"{method.upper()} /{cmd_name}"))
    parser = subparsers.add_parser(cmd_name, help=desc)
    parser.set_defaults(_method=method, _path=path)

    # GET query parameters
    for param in details.get("parameters", []):
        if param.get("in") != "query":
            continue
        name = param["name"]
        schema = param.get("schema", {})
        required = param.get("required", False)
        py_type, suffix = openapi_type_to_python(schema)
        flag = f"--{name}"
        kwargs: dict = {}
        if py_type is not None:
            kwargs["type"] = py_type
        else:
            # boolean
            kwargs["action"] = "store_true"
        if not required:
            kwargs["default"] = None
        else:
            if "action" not in kwargs:
                kwargs["required"] = True
        help_text = param.get("description", name) + suffix
        if "enum" in schema:
            kwargs["choices"] = schema["enum"]
            help_text += f" (choices: {schema['enum']})"
        kwargs["help"] = help_text
        parser.add_argument(flag, **kwargs)

    # POST/PUT/PATCH/DELETE request body
    rb_schema = (
        details.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
    )
    required_fields = set(rb_schema.get("required", []))
    properties = rb_schema.get("properties", {})

    if properties:
        parser.add_argument(
            "--stdin", action="store_true", default=False,
            help="Read JSON body from stdin instead of flags",
        )

    for prop_name, prop_schema in properties.items():
        flag = f"--{prop_name}"
        py_type, suffix = openapi_type_to_python(prop_schema)
        kwargs = {}
        if py_type is not None:
            kwargs["type"] = py_type
        else:
            kwargs["action"] = "store_true"
        desc_text = prop_schema.get("description", prop_name) + suffix
        if "enum" in prop_schema:
            kwargs["choices"] = prop_schema["enum"]
            desc_text += f" (choices: {prop_schema['enum']})"
        kwargs["help"] = desc_text
        if prop_name in required_fields and "action" not in kwargs:
            kwargs["required"] = True
        else:
            kwargs["default"] = None
        parser.add_argument(flag, **kwargs)


def coerce_body_value(value, schema: dict):
    """Coerce a CLI string value to the appropriate JSON type."""
    if value is None:
        return None
    t = schema.get("type")
    if t in ("array", "object"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    if t == "boolean":
        return bool(value)
    if t == "integer":
        return int(value)
    if t == "number":
        return float(value)
    return value


def execute(args, base_url: str, token: str, pretty: bool):
    method = args._method
    path = args._path
    url = f"{base_url}{path}"
    headers = {"x-api-key": token, "Content-Type": "application/json"}

    # Build query params for GET
    params = {}
    body = None

    if method == "get":
        # Collect all non-internal args as query params
        for key, val in vars(args).items():
            if key.startswith("_") or val is None:
                continue
            params[key] = val
    else:
        # Build request body
        if getattr(args, "stdin", False):
            body = json.loads(sys.stdin.read())
        else:
            body = {}
            for key, val in vars(args).items():
                if key.startswith("_") or key in ("stdin", "pretty"):
                    continue
                if val is None:
                    continue
                body[key] = val
            if not body:
                body = None

    with httpx.Client(timeout=60) as client:
        resp = client.request(
            method.upper(),
            url,
            headers=headers,
            params=params or None,
            json=body,
        )
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
            sys.exit(1)

    # Print response
    try:
        data = resp.json()
    except Exception:
        print(resp.text)
        return

    if pretty:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data))


def list_commands(spec: dict):
    """Print all available commands grouped by resource."""
    paths = spec.get("paths", {})
    groups: dict[str, list[tuple[str, str, str]]] = {}
    for path, methods in sorted(paths.items()):
        for method, details in methods.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            cmd = path.lstrip("/")
            parts = cmd.split(".", 1)
            group = parts[0] if len(parts) > 1 else "other"
            desc = details.get("summary", details.get("description", ""))
            groups.setdefault(group, []).append((cmd, method.upper(), desc))

    for group in sorted(groups):
        print(f"\n{group}:")
        for cmd, method, desc in groups[group]:
            line = f"  {cmd:<45} {method:<6}"
            if desc:
                line += f" {desc}"
            print(line)


def main():
    # Pre-parse to extract --project, --url, --list, --refresh-cache, --pretty
    # before dynamically building subcommands
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--org", default="DEFAULT", help="fnox key suffix for Dokploy org (default: DEFAULT)")
    pre.add_argument("--url", default=None, help="Override base URL")
    pre.add_argument("--list", action="store_true", help="List all available commands")
    pre.add_argument("--refresh-cache", action="store_true", help="Force refresh the cached OpenAPI spec")
    pre.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    pre_args, remaining = pre.parse_known_args()

    org = pre_args.org
    base_url = pre_args.url or DEFAULT_BASE_URL
    if not base_url:
        # Try fnox as last resort
        result = subprocess.run(["fnox", "get", "DOKPLOY_URL"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            base_url = result.stdout.strip().rstrip("/")
        else:
            print("Error: No Dokploy URL configured. Set DOKPLOY_URL env var, store it in fnox, or pass --url.", file=sys.stderr)
            sys.exit(1)
    token = load_token(org)
    spec = get_spec(org, base_url, token, refresh=pre_args.refresh_cache)

    if pre_args.list:
        list_commands(spec)
        return

    if not remaining:
        pre.print_help()
        print("\nUse --list to see all available commands.")
        sys.exit(1)

    # Build full parser with subcommands from spec
    parser = argparse.ArgumentParser(
        prog="dokploy",
        description="Dokploy CLI — dynamically generated from the OpenAPI spec",
        parents=[pre],
    )
    subparsers = parser.add_subparsers(dest="_command")

    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            build_endpoint_parser(subparsers, path, method, details)

    args = parser.parse_args()
    if not hasattr(args, "_method"):
        parser.print_help()
        sys.exit(1)

    execute(args, base_url, token, pre_args.pretty)


if __name__ == "__main__":
    main()

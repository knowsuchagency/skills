# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fal-client>=0.5.0",
#     "httpx",
# ]
# ///
"""Generate images using fal.ai (GPT-Image 2, with GPT-Image 1.5 fallback for transparency)."""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import httpx

MODELS = {
    "gpt-2": "openai/gpt-image-2",
    "gpt": "fal-ai/gpt-image-1.5",
}

RATIO_TO_WXH = {
    "1:1": "1024x1024",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "4:3": "1536x1024",
    "3:4": "1024x1536",
    "21:9": "1536x1024",
}

# gpt-image-2 only accepts these enum presets (or a {width, height} object).
SIZE_TO_GPT2_PRESET = {
    "1024x1024": "square_hd",
    "1536x1024": "landscape_4_3",
    "1024x1536": "portrait_4_3",
    "1:1": "square_hd",
    "4:3": "landscape_4_3",
    "3:4": "portrait_4_3",
    "16:9": "landscape_16_9",
    "9:16": "portrait_16_9",
    "21:9": "landscape_16_9",
}

ALL_SIZES = ["1024x1024", "1536x1024", "1024x1536"] + list(RATIO_TO_WXH)


def load_fal_key() -> str:
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    result = subprocess.run(
        ["fnox", "get", "FAL_KEY"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error: failed to get FAL_KEY from fnox: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-")


def download_image(url: str, dest: Path) -> None:
    with httpx.Client(follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
        dest.write_bytes(resp.content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate images via fal.ai")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--model", default="gpt-2", choices=list(MODELS),
                        help="Model to use (default: gpt-2). Use `gpt` (gpt-image-1.5) for transparent backgrounds.")
    parser.add_argument("--size", default="1024x1024", choices=ALL_SIZES,
                        help="Image size as WxH or aspect ratio (default: 1024x1024)")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--num-images", type=int, default=1, choices=range(1, 5))
    parser.add_argument("--format", default="png", choices=["jpeg", "png", "webp"], dest="output_format")
    parser.add_argument("--background", default="auto", choices=["auto", "transparent", "opaque"],
                        help="Transparent background only works with --model gpt (gpt-image-1.5).")
    naming = parser.add_mutually_exclusive_group()
    naming.add_argument("--filename", default=None, help="Output base name (no extension)")
    naming.add_argument("--output", default=None, help="Output path stem (no extension, overrides --output-dir)")
    parser.add_argument("--output-dir", default=tempfile.gettempdir())
    args = parser.parse_args()

    os.environ["FAL_KEY"] = load_fal_key()

    import fal_client

    model_id = MODELS[args.model]

    if args.model == "gpt-2":
        image_size = SIZE_TO_GPT2_PRESET[args.size]
    else:
        image_size = RATIO_TO_WXH.get(args.size, args.size)

    arguments: dict = {
        "prompt": args.prompt,
        "image_size": image_size,
        "quality": args.quality,
        "num_images": args.num_images,
        "output_format": args.output_format,
    }
    if args.model == "gpt":
        arguments["background"] = args.background
    elif args.background == "transparent":
        print("Warning: transparent background only works with --model gpt; ignoring.", file=sys.stderr)

    result = fal_client.subscribe(model_id, arguments=arguments)

    if args.output:
        base = Path(args.output)
        base.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        if args.filename:
            base = output_dir / args.filename
        else:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            slug = slugify(args.prompt)
            base = output_dir / f"{timestamp}-{slug}"

    for i, image in enumerate(result["images"]):
        ext = args.output_format
        suffix = f"-{i + 1}" if args.num_images > 1 else ""
        dest = base.parent / f"{base.name}{suffix}.{ext}"
        download_image(image["url"], dest)
        print(dest)


if __name__ == "__main__":
    main()

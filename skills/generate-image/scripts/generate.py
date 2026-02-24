# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fal-client>=0.5.0",
#     "httpx",
# ]
# ///
"""Generate images using fal.ai (Gemini / GPT-Image)."""

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
    "gemini-flash": "fal-ai/gemini-25-flash-image",
    "gemini-pro": "fal-ai/gemini-3-pro-image-preview",
    "gpt": "fal-ai/gpt-image-1.5",
}

WXH_TO_RATIO = {"1024x1024": "1:1", "1536x1024": "4:3", "1024x1536": "3:4"}
RATIO_TO_WXH = {
    "1:1": "1024x1024",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "4:3": "1536x1024",
    "3:4": "1024x1536",
    "21:9": "1536x1024",
}
QUALITY_TO_RESOLUTION = {"low": "1K", "medium": "2K", "high": "4K"}

ALL_SIZES = list(WXH_TO_RATIO) + list(RATIO_TO_WXH)


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
    parser.add_argument("--model", default="gemini-flash", choices=list(MODELS),
                        help="Model to use (default: gemini-flash)")
    parser.add_argument("--size", default="1024x1024", choices=ALL_SIZES,
                        help="Image size as WxH or aspect ratio (default: 1024x1024)")
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    parser.add_argument("--num-images", type=int, default=1, choices=range(1, 5))
    parser.add_argument("--format", default="png", choices=["jpeg", "png", "webp"], dest="output_format")
    parser.add_argument("--background", default="auto", choices=["auto", "transparent", "opaque"])
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility (Gemini only)")
    parser.add_argument("--output-dir", default=tempfile.gettempdir())
    args = parser.parse_args()

    os.environ["FAL_KEY"] = load_fal_key()

    import fal_client

    model_id = MODELS[args.model]
    is_gemini = args.model.startswith("gemini")

    if is_gemini:
        if args.background == "transparent":
            print("Warning: transparent background not supported with Gemini, using opaque.", file=sys.stderr)

        aspect_ratio = WXH_TO_RATIO.get(args.size, args.size)

        arguments: dict = {
            "prompt": args.prompt,
            "num_images": args.num_images,
            "aspect_ratio": aspect_ratio,
            "output_format": args.output_format,
        }
        if args.seed is not None:
            arguments["seed"] = args.seed
        if args.model == "gemini-pro":
            arguments["resolution"] = QUALITY_TO_RESOLUTION[args.quality]
    else:
        image_size = RATIO_TO_WXH.get(args.size, args.size)

        arguments = {
            "prompt": args.prompt,
            "image_size": image_size,
            "quality": args.quality,
            "num_images": args.num_images,
            "output_format": args.output_format,
            "background": args.background,
        }

    result = fal_client.subscribe(model_id, arguments=arguments)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = slugify(args.prompt)

    for i, image in enumerate(result["images"]):
        ext = args.output_format
        suffix = f"-{i + 1}" if args.num_images > 1 else ""
        filename = f"{timestamp}-{slug}{suffix}.{ext}"
        dest = output_dir / filename
        download_image(image["url"], dest)
        print(dest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generic Warhammer faction xlsx builder.

Usage:
  python build.py <faction_key> [<faction_key> ...]
  python build.py --all
  python build.py --list

Examples:
  python build.py flesh_eater_courts
  python build.py nighthaunt ossiarch_bonereapers soulblight_gravelords
  python build.py --all
"""

import sys
from pathlib import Path

from faction_registry import FactionRegistry
from factions import FACTIONS
from image_pipeline import ImagePipeline
from worksheet_builder import WorksheetBuilder

_IMG_DIR  = Path("data/images")
_registry = FactionRegistry(FACTIONS)


def build_faction(key: str) -> None:
    faction   = _registry.load(key)
    filenames = [p.image_file for p in faction.products]
    manifest  = ImagePipeline(img_dir=_IMG_DIR).fetch_all(filenames)
    WorksheetBuilder().write(faction, manifest)


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if args[0] == "--list":
        print("Available factions:")
        for key in _registry.keys():
            f = _registry.load(key)
            print(f"  {key:<30} ({len(f.products)} products)  ->  {f.output}")
        sys.exit(0)

    keys = list(_registry.keys()) if args[0] == "--all" else args

    unknown = [k for k in keys if k not in _registry]
    if unknown:
        print(f"Unknown faction(s): {', '.join(unknown)}")
        print("Run 'python build.py --list' to see available keys.")
        sys.exit(1)

    for key in keys:
        build_faction(key)

    print(f"\nAll done. Built {len(keys)} faction(s).")


if __name__ == "__main__":
    main()

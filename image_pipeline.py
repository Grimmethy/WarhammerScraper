import io
from pathlib import Path

import requests
from PIL import Image as PILImage

_IMG_BASE    = "https://www.warhammer.com/app/resources/catalog/product/920x950/"
_TIMEOUT     = 20
_HEADERS     = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}
_THUMB_W     = 100
_THUMB_H     = 100


class ImagePipeline:
    def __init__(
        self,
        img_dir: Path,
        thumb_w: int = _THUMB_W,
        thumb_h: int = _THUMB_H,
        timeout: int = _TIMEOUT,
        headers: dict | None = None,
    ):
        self.img_dir = img_dir
        self.thumb_w = thumb_w
        self.thumb_h = thumb_h
        self.timeout = timeout
        self.headers = headers or _HEADERS

    def fetch_all(self, filenames: list[str]) -> dict[str, io.BytesIO | None]:
        self.img_dir.mkdir(parents=True, exist_ok=True)
        n = len(filenames)
        manifest: dict[str, io.BytesIO | None] = {}
        for i, filename in enumerate(filenames, 1):
            local = self._download(filename)
            manifest[filename] = self._thumbnail(local) if local else None
            print(f"  [img {i:02d}/{n}] {filename}")
        return manifest

    def _download(self, filename: str) -> Path | None:
        dest = self.img_dir / filename
        if dest.exists():
            return dest
        try:
            r = requests.get(_IMG_BASE + filename, headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            dest.write_bytes(r.content)
            return dest
        except Exception as e:
            print(f"  [warn] download {filename}: {e}")
            return None

    def _thumbnail(self, src: Path) -> io.BytesIO | None:
        try:
            img = PILImage.open(src).convert("RGBA")
            img.thumbnail((self.thumb_w, self.thumb_h), PILImage.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return buf
        except Exception as e:
            print(f"  [warn] thumbnail {src.name}: {e}")
            return None

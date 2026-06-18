from dataclasses import dataclass


class FactionNotFoundError(Exception):
    pass


@dataclass(frozen=True)
class Product:
    name: str
    price: str
    slug: str
    image_file: str


@dataclass(frozen=True)
class Faction:
    title: str
    output: str
    products: tuple[Product, ...]


class FactionRegistry:
    def __init__(self, raw: dict) -> None:
        self._raw = raw

    def __contains__(self, key: object) -> bool:
        return key in self._raw

    def keys(self):
        return self._raw.keys()

    def load(self, key: str) -> Faction:
        if key not in self._raw:
            raise FactionNotFoundError(
                f"Unknown faction '{key}'. Run --list to see available keys."
            )
        entry = self._raw[key]
        products = []
        for i, item in enumerate(entry["products"]):
            if len(item) != 4:
                raise ValueError(
                    f"Faction '{key}' product [{i}] has {len(item)} fields, expected 4: {item!r}"
                )
            products.append(Product(*item))
        return Faction(
            title=entry["title"],
            output=entry["output"],
            products=tuple(products),
        )

inventory: dict[str, list[dict]] = {}


def add_item(name: str, quantity: int, expiry: str) -> None:
    """Добавляет новую партию продукта в хранилище."""
    inventory.setdefault(name, []).append({"quantity": quantity, "expiry": expiry})


def get_all() -> dict[str, list[dict]]:
    """Возвращает все запасы."""
    return inventory

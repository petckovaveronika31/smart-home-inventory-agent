"""Модуль для хранения состояния приложения."""

# Словарь, где ключ — название продукта, значение — словарь с данными
inventory = {}


def add_item(name: str, quantity: int, expiry_date: str):
    """Добавляет продукт или обновляет его количество."""
    if name in inventory:
        inventory[name]["quantity"] += quantity
        inventory[name]["expiry"] = expiry_date
    else:
        inventory[name] = {"quantity": quantity, "expiry": expiry_date}


def remove_item(name: str, quantity: int) -> bool:
    """Списывает продукт. Возвращает True, если успешно."""
    if name not in inventory:
        return False
    if inventory[name]["quantity"] < quantity:
        return False

    inventory[name]["quantity"] -= quantity
    if inventory[name]["quantity"] == 0:
        del inventory[name]
    return True


def get_inventory() -> dict:
    """Возвращает весь список продуктов."""
    return inventory

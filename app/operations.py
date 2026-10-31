"""Модуль с бизнес-логикой агента."""
from datetime import datetime

from app import storage


def parse_date(date_str: str):
    """Проверяет, что дата введена в формате ГГГГ-ММ-ДД."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def op_add(args: list) -> str:
    """Команда: add <название> <количество> <ГГГГ-ММ-ДД>"""
    if len(args) != 3:
        return "Ошибка: неверное количество аргументов. Используйте: add <название> <количество> <ГГГГ-ММ-ДД>"
    
    name, quantity_str, expiry_str = args
    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            return "Ошибка: количество должно быть больше нуля."
    except ValueError:
        return "Ошибка: количество должно быть целым числом."

    if not parse_date(expiry_str):
        return "Ошибка: неверный формат даты. Используйте ГГГГ-ММ-ДД."

    storage.add_item(name, quantity, expiry_str)
    return f"Успешно добавлено: {name} (x{quantity}), срок годности до {expiry_str}."

def op_list(args: list) -> str:
    """Команда: list"""
    if args:
        return "Ошибка: команда list не принимает аргументов."
    
    items = storage.get_inventory()
    if not items:
        return "Ваши запасы пусты. Добавьте продукты командой add."

    result = ["--- Ваши запасы ---"]
    today = datetime.now().date()

    for name, data in items.items():
        expiry = parse_date(data["expiry"])
        days_left = (expiry - today).days
        qty = data["quantity"]

        if days_left < 0:
            status = "ПРОСРОЧЕНО"
        elif days_left <= 3:
            status = f"Скоро истекает ({days_left} дн.)"
        else:
            status = "Свежий"
        result.append(f"- {name}: {qty} шт. | Срок: {data['expiry']} | Статус: {status}")

    return "\n".join(result)

def op_consume(args: list) -> str:
    """Команда: consume <название> <количество>"""
    if len(args) != 2:
        return "Ошибка: неверное количество аргументов. Используйте: consume <название> <количество>"
    
    name, quantity_str = args
    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            return "Ошибка: количество должно быть больше нуля."
    except ValueError:
        return "Ошибка: количество должно быть целым числом."

    success = storage.remove_item(name, quantity)
    if success:
        return f"Успешно списано: {name} (x{quantity})."
    else:
        return f"Ошибка: продукт '{name}' не найден в нужном количестве."
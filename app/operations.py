from datetime import datetime

from app import storage


def parse_date(date_str: str) -> datetime | None:
    """Парсит дату из строки формата ГГГГ-ММ-ДД."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def is_expired(expiry_str: str) -> bool:
    """Проверяет, истек ли срок годности (с точностью до дня)."""
    expiry_date = parse_date(expiry_str)
    if not expiry_date:
        return True

    # Отбрасываем время, сравниваем только даты
    today = datetime.now().date()
    return expiry_date.date() < today


def op_add(args: list) -> str:
    """Добавляет продукт (создает новую партию)."""
    if len(args) != 3:
        return "Ошибка: неверное количество аргументов. Используйте: add <название> <количество> <ГГГГ-ММ-ДД>"

    name, quantity_str, expiry_str = args

    name = name.strip()
    if not name:
        return "Ошибка: название не может быть пустым."

    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            return "Ошибка: количество должно быть больше нуля."
    except ValueError:
        return "Ошибка: количество должно быть целым числом."

    if not parse_date(expiry_str):
        return "Ошибка: неверный формат даты. Используйте ГГГГ-ММ-ДД."

    storage.add_item(name, quantity, expiry_str)
    return f"Добавлено: {name}, {quantity} шт., срок {expiry_str}."


def op_list(args: list) -> str:
    """Показывает все запасы с учетом партий."""
    if args:
        return "Ошибка: команда list не принимает аргументов."

    inventory = storage.get_all()
    if not inventory:
        return "Запасы пусты."

    result = []
    for name, batches in inventory.items():
        for batch in batches:
            status = "Просрочено" if is_expired(batch["expiry"]) else "Свежий"
            result.append(
                f"{name}: {batch['quantity']} шт., "
                f"срок {batch['expiry']}, статус {status}"
            )

    return "\n".join(result)


def op_consume(args: list) -> str:
    """Списывает продукт из запасов."""
    if len(args) != 2:
        return "Ошибка: неверное количество аргументов. Используйте: consume <название> <количество>"

    name, quantity_str = args
    name = name.strip()

    if not name:
        return "Ошибка: название не может быть пустым."

    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            return "Ошибка: количество должно быть больше нуля."
    except ValueError:
        return "Ошибка: количество должно быть целым числом."

    batches = storage.get_all().get(name)
    if not batches:
        return f"Ошибка: продукт '{name}' не найден."

    total = sum(b["quantity"] for b in batches)
    if quantity > total:
        return f"Ошибка: недостаточно '{name}'. В наличии {total} шт."

    remaining = quantity
    for batch in batches:
        if remaining == 0:
            break
        take = min(batch["quantity"], remaining)
        batch["quantity"] -= take
        remaining -= take

    # Удаляем пустые партии
    storage.get_all()[name] = [b for b in batches if b["quantity"] > 0]

    # Если все партии удалены, удаляем и сам продукт
    if not storage.get_all()[name]:
        del storage.get_all()[name]

    return f"Списано {quantity} шт. '{name}'."


def op_help(args: list) -> str:
    """Возвращает справку."""
    return (
        "Доступные команды:\n"
        "  add <название> <количество> <ГГГГ-ММ-ДД> - добавить продукт\n"
        "  list - показать все запасы\n"
        "  consume <название> <количество> - списать продукт\n"
        "  help - показать эту справку\n"
        "  exit - выйти из программы"
    )

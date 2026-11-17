"""Модуль хранения и восстановления запасов."""

import json
import os
from pathlib import Path

inventory: dict[str, list[dict]] = {}

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "inventory.json"


class StorageError(Exception):
    """Ошибка чтения или записи хранилища."""


def load_inventory() -> None:
    """Загружает запасы из JSON-файла."""
    global inventory

    if not DATA_FILE.exists():
        inventory = {}
        return

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise StorageError("Некорректный формат файла хранилища.")

        for name, batches in data.items():
            if not isinstance(name, str) or not isinstance(batches, list):
                raise StorageError("Некорректная структура запасов.")

            for batch in batches:
                if (
                    not isinstance(batch, dict)
                    or not isinstance(batch.get("quantity"), int)
                    or isinstance(batch.get("quantity"), bool)
                    or batch["quantity"] <= 0
                    or not isinstance(batch.get("expiry"), str)
                ):
                    raise StorageError("Некорректная партия продукта.")

        inventory = data

    except (OSError, json.JSONDecodeError) as error:
        raise StorageError(f"Не удалось загрузить запасы: {error}") from error


def save_inventory() -> None:
    """Сохраняет текущие запасы в JSON-файл."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        temp_file = DATA_FILE.with_suffix(".tmp")

        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(inventory, file, ensure_ascii=False, indent=4)

        os.replace(temp_file, DATA_FILE)

    except OSError as error:
        raise StorageError(f"Не удалось сохранить запасы: {error}") from error


def add_item(name: str, quantity: int, expiry: str) -> None:
    """Добавляет новую партию продукта в хранилище."""
    inventory.setdefault(name, []).append({"quantity": quantity, "expiry": expiry})

    save_inventory()


def get_all() -> dict[str, list[dict]]:
    """Возвращает все запасы."""
    return inventory

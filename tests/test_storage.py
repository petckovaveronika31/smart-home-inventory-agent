import json

import pytest

from app import storage


@pytest.fixture
def temporary_storage(tmp_path, monkeypatch):
    """Создаёт временное хранилище для каждого теста."""
    test_file = tmp_path / "inventory.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)
    storage.inventory = {}
    return test_file


def test_first_start_without_file(temporary_storage):
    """При первом запуске без файла запасы пустые."""
    storage.load_inventory()

    assert storage.get_all() == {}


def test_add_item_saves_data(temporary_storage):
    """Добавление продукта сохраняется в JSON."""
    storage.add_item("Молоко", 5, "2027-12-31")

    assert temporary_storage.exists()

    with temporary_storage.open(encoding="utf-8") as file:
        data = json.load(file)

    assert data == {"Молоко": [{"quantity": 5, "expiry": "2027-12-31"}]}


def test_load_inventory_restores_data(temporary_storage):
    """Загрузка восстанавливает ранее сохранённые данные."""
    expected = {"Молоко": [{"quantity": 5, "expiry": "2027-12-31"}]}

    temporary_storage.write_text(
        json.dumps(expected, ensure_ascii=False),
        encoding="utf-8",
    )

    storage.load_inventory()

    assert storage.get_all() == expected


def test_consume_result_is_saved(temporary_storage):
    """Результат списания сохраняется после изменения данных."""
    storage.add_item("Молоко", 5, "2027-12-31")

    storage.inventory["Молоко"][0]["quantity"] = 3
    storage.save_inventory()

    storage.inventory = {}
    storage.load_inventory()

    assert storage.get_all()["Молоко"][0]["quantity"] == 3


def test_corrupted_json_raises_storage_error(temporary_storage):
    """Повреждённый JSON вызывает понятную ошибку."""
    temporary_storage.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(storage.StorageError):
        storage.load_inventory()


def test_invalid_json_structure_raises_storage_error(temporary_storage):
    """Некорректная структура JSON вызывает ошибку."""
    temporary_storage.write_text('["Молоко"]', encoding="utf-8")

    with pytest.raises(storage.StorageError):
        storage.load_inventory()


def test_multiple_products_are_saved(temporary_storage):
    """Несколько продуктов сохраняются одновременно."""
    storage.add_item("Молоко", 5, "2027-12-31")
    storage.add_item("Хлеб", 3, "2027-12-25")

    storage.inventory = {}
    storage.load_inventory()

    assert storage.get_all()["Молоко"][0]["quantity"] == 5
    assert storage.get_all()["Хлеб"][0]["quantity"] == 3

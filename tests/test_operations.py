import pytest

from app import operations, storage


@pytest.fixture
def empty_inventory(tmp_path, monkeypatch):
    """Создаёт изолированное хранилище для тестов операций."""
    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        tmp_path / "inventory.json",
    )
    storage.inventory = {}


def test_add_product(empty_inventory):
    result = operations.op_add(["Молоко", "5", "2027-12-31"])

    assert "Добавлено" in result
    assert storage.get_all()["Молоко"][0]["quantity"] == 5


def test_add_invalid_quantity(empty_inventory):
    result = operations.op_add(["Молоко", "abc", "2027-12-31"])

    assert "целым числом" in result
    assert storage.get_all() == {}


def test_add_invalid_date(empty_inventory):
    result = operations.op_add(["Молоко", "5", "31-12-2027"])

    assert "формат даты" in result
    assert storage.get_all() == {}


def test_list_empty_inventory(empty_inventory):
    assert operations.op_list([]) == "Запасы пусты."


def test_consume_product(empty_inventory):
    storage.add_item("Молоко", 5, "2027-12-31")

    result = operations.op_consume(["Молоко", "2"])

    assert "Списано" in result
    assert storage.get_all()["Молоко"][0]["quantity"] == 3


def test_consume_all_product(empty_inventory):
    storage.add_item("Молоко", 5, "2027-12-31")

    operations.op_consume(["Молоко", "5"])

    assert "Молоко" not in storage.get_all()


def test_consume_insufficient_quantity(empty_inventory):
    storage.add_item("Молоко", 2, "2027-12-31")

    result = operations.op_consume(["Молоко", "5"])

    assert "недостаточно" in result
    assert storage.get_all()["Молоко"][0]["quantity"] == 2


def test_consume_missing_product(empty_inventory):
    result = operations.op_consume(["Молоко", "2"])

    assert "не найден" in result


def test_help_command():
    assert "Доступные команды" in operations.op_help([])


def test_add_without_arguments(empty_inventory):
    result = operations.op_add([])

    assert "неверное количество аргументов" in result


def test_add_empty_name(empty_inventory):
    result = operations.op_add(["", "5", "2027-12-31"])

    assert "название не может быть пустым" in result


def test_add_zero_quantity(empty_inventory):
    result = operations.op_add(["Молоко", "0", "2027-12-31"])

    assert "больше нуля" in result


def test_add_negative_quantity(empty_inventory):
    result = operations.op_add(["Молоко", "-5", "2027-12-31"])

    assert "больше нуля" in result


def test_list_with_arguments(empty_inventory):
    result = operations.op_list(["лишний"])

    assert "не принимает аргументов" in result


def test_list_expired_product(empty_inventory):
    storage.add_item("Молоко", 2, "2020-01-01")

    result = operations.op_list([])

    assert "Просрочено" in result


def test_consume_without_arguments(empty_inventory):
    result = operations.op_consume([])

    assert "неверное количество аргументов" in result


def test_consume_empty_name(empty_inventory):
    result = operations.op_consume(["", "2"])

    assert "название не может быть пустым" in result


def test_consume_invalid_quantity(empty_inventory):
    result = operations.op_consume(["Молоко", "abc"])

    assert "целым числом" in result


def test_consume_zero_quantity(empty_inventory):
    result = operations.op_consume(["Молоко", "0"])

    assert "больше нуля" in result


def test_consume_multiple_batches(empty_inventory):
    storage.add_item("Молоко", 3, "2027-12-31")
    storage.add_item("Молоко", 4, "2028-01-15")

    result = operations.op_consume(["Молоко", "5"])

    assert "Списано" in result
    assert storage.get_all()["Молоко"] == [{"quantity": 2, "expiry": "2028-01-15"}]


def test_invalid_expiry_date():
    assert operations.is_expired("неправильная-дата") is True

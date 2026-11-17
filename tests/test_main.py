from app import main, storage


def test_help_command(capsys, monkeypatch, tmp_path):
    """Команда help выводит справку."""
    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        tmp_path / "inventory.json",
    )
    monkeypatch.setattr("builtins.input", lambda _: "help")

    inputs = iter(["help", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.main()

    output = capsys.readouterr().out

    assert "Доступные команды" in output
    assert "До свидания!" in output


def test_unknown_command(capsys, monkeypatch, tmp_path):
    """Неизвестная команда обрабатывается без завершения программы."""
    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        tmp_path / "inventory.json",
    )

    inputs = iter(["unknown", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.main()

    output = capsys.readouterr().out

    assert "Неизвестная команда" in output
    assert "До свидания!" in output


def test_invalid_arguments(capsys, monkeypatch, tmp_path):
    """Некорректные аргументы обрабатываются."""
    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        tmp_path / "inventory.json",
    )

    inputs = iter(["add Молоко abc 2027-12-31", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.main()

    output = capsys.readouterr().out

    assert "целым числом" in output
    assert "До свидания!" in output


def test_corrupted_storage(capsys, monkeypatch, tmp_path):
    """При повреждённом хранилище выводится ошибка."""
    data_file = tmp_path / "inventory.json"
    data_file.write_text("{invalid json", encoding="utf-8")

    monkeypatch.setattr(storage, "DATA_FILE", data_file)

    main.main()

    output = capsys.readouterr().out

    assert "Ошибка хранилища" in output

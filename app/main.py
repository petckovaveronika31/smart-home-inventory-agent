"""Главный модуль приложения. Цикл ввода команд."""

import shlex
import sys

from app import operations

HELP_TEXT = """
Доступные команды:
  add <название> <кол-во> <дата>  - Добавить продукт (дата в формате ГГГГ-ММ-ДД)
  list                            - Показать все запасы и их статус
  consume <название> <кол-во>     - Списать (использовать) продукт
  help                            - Показать эту справку
  exit                            - Выйти из программы
"""

COMMANDS = {
    "add": operations.op_add,
    "list": operations.op_list,
    "consume": operations.op_consume,
}


def main():
    print("Добро пожаловать в ИИ-агент 'Умный помощник по домашним запасам'!")
    print("Введите 'help', чтобы увидеть список команд.")

    while True:
        try:
            raw_input = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы...")
            sys.exit(0)

        if not raw_input:
            continue

        try:
            parts = shlex.split(raw_input)
        except ValueError as e:
            print(f"Ошибка разбора команды: {e}")
            continue

        command = parts[0].lower()
        args = parts[1:]

        if command in ("exit", "quit"):
            print("До свидания!")
            break
        elif command == "help":
            print(HELP_TEXT)
        elif command in COMMANDS:
            result = COMMANDS[command](args)
            print(result)
        else:
            print(
                f"Неизвестная команда: '{command}'. Введите 'help' для списка команд."
            )


if __name__ == "__main__":
    main()

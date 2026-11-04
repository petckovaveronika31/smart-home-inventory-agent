# Умный помощник по домашним запасам

Консольный прототип ИИ-агента для учёта домашних запасов.

## Технологический стек

| Компонент | Значение |
|---|---|
| IDE / редактор | Visual Studio Code |
| Язык и версия | Python 3.12.x |
| Среда выполнения | Интерпретатор Python из venv |
| Менеджер зависимостей | pip + `requirements.txt` |
| Библиотеки | стандартная библиотека Python (`datetime`, `sys`) |
| Хранение данных | в памяти (словарь со списком партий), сбрасывается после перезапуска |
| Отладчик | Встроенный отладчик VS Code (F5) |
| Линтер | Ruff (`ruff check .`) |
| Форматтер | Ruff (`ruff format --check .`) |

## Подготовка окружения и запуск

Для запуска проекта выполните следующие команды в терминале:

```bash
git clone https://github.com/petckovaveronika31/smart-home-inventory-agent.git
cd smart-home-inventory-agent
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
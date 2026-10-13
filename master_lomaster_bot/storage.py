"""Работа с хранением заявок в файле requests.json (учебный вариант без БД)."""

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requests.json")


def load_requests() -> list[Any]:
    """Загружает список заявок из файла requests.json."""
    try:
        if not os.path.exists(STORAGE_FILE):
            save_requests([])
            return []
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            logger.warning("requests.json имеет некорректный формат, используется пустой список.")
            return []
        return data
    except json.JSONDecodeError:
        logger.warning("Не удалось разобрать requests.json. Используется пустой список.")
        return []
    except OSError as error:
        logger.error("Ошибка чтения requests.json: %s", error)
        return []


def save_requests(requests: list[Any]) -> None:
    """Сохраняет список заявок в файл requests.json."""
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            json.dump(requests, file, ensure_ascii=False, indent=4)
    except OSError as error:
        logger.error("Ошибка записи requests.json: %s", error)
        raise


def add_request(request: dict[str, Any]) -> None:
    """Добавляет новую заявку в файл, сохраняя уже существующие."""
    requests = load_requests()
    requests.append(request)
    save_requests(requests)

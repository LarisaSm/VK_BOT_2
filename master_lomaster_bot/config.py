import os

from dotenv import load_dotenv

# Загружаем переменные из файла .env в окружение
load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
MASTER_PHONE = os.getenv("MASTER_PHONE", "+79990000000")


def get_vk_token() -> str:
    """Возвращает токен VK. Если токен не указан — выводит понятную ошибку."""
    if not VK_TOKEN or VK_TOKEN == "your_vk_group_token_here":
        raise ValueError(
            "VK_TOKEN не указан. Создайте файл .env и добавьте токен сообщества VK."
        )
    return VK_TOKEN

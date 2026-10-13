"""Точка входа VK-бота «Мастер-Ломастер» (vkbottle, Long Poll API)."""

import logging
import sys

from vkbottle import Bot

from config import get_vk_token

# Настройка логирования: запуск, ошибки, создание заявок.
# Токен в логи не выводится.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("master_lomaster_bot")


def main() -> None:
    """Создаёт бота, подключает обработчики и запускает Long Poll."""
    try:
        token = get_vk_token()
    except ValueError as error:
        logger.error("%s", error)
        sys.exit(1)

    bot = Bot(token=token)

    # Импортируем обработчики здесь, чтобы ошибка токена срабатывала раньше
    from handlers import bl

    bot.labeler.load(bl)

    logger.info("Бот запускается. Подключение к VK Long Poll API...")
    bot.run_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Остановка бота пользователем.")
        sys.exit(0)
    except Exception:
        # Ошибка одного пользователя не должна ронять бота
        logger.exception("Критическая ошибка бота")
        sys.exit(1)

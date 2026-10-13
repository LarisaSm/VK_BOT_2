"""Обработчики сообщений VK-бота «Мастер-Ломастер».

Порядок регистрации важен: обработчики выполняются сверху вниз,
и первый совпавший (blocking=True) останавливает цепочку.
Поэтому конкретные команды идут первыми, а универсальный
обработчик (заявка + неизвестные команды) — самым последним.
"""

import logging
import re
from typing import Any

from vkbottle.bot import BotLabeler, Message

from config import MASTER_PHONE
from keyboards import (
    AFTER_REQUEST_KB,
    BACK_TO_MAIN_KB,
    CATEGORY_NAV_KB,
    MAIN_MENU_KB,
    PRICE_KB,
    REQUEST_FORM_KB,
    SERVICES_KB,
)
from services import CATEGORY_BUTTONS, format_category_text
from storage import add_request

logger = logging.getLogger(__name__)

bl = BotLabeler()

# Временное состояние пользователя для сценария заявки.
# Хранится в памяти процесса (учебный проект, Redis/БД не используем).
# Пример: {123456: {"step": "waiting_name", "task": "...", ...}}
user_states: dict[int, dict[str, Any]] = {}

# Команды, возвращающие пользователя в главное меню.
# Текстовый rule сравнивает точное совпадение с учётом регистра,
# поэтому перечисляем варианты из ТЗ явно.
START_COMMANDS = ["Начать", "начать", "Старт", "старт", "Меню", "меню", "menu", "start"]

# Варианты отмены заявки
CANCEL_COMMANDS = ["Отмена", "отмена", "ОТМЕНА", "❌ Отмена", "cancel"]


def is_phone_valid(text: str) -> bool:
    """Простая проверка номера телефона.

    Принимает варианты: +79991234567, 89991234567, +7 999 123-45-67.
    """
    digits = re.sub(r"\D", "", text)
    # Убираем код страны (8... или 7... при 11 цифрах), оставляем 10 цифр
    if len(digits) == 11 and digits[0] in ("8", "7"):
        digits = digits[1:]
    return len(digits) == 10


def normalize_phone(text: str) -> str:
    """Приводит номер к единому виду +7XXXXXXXXXX для сохранения."""
    digits = re.sub(r"\D", "", text)
    if len(digits) == 11 and digits[0] in ("8", "7"):
        digits = digits[1:]
    return "+7" + digits


async def send_main_menu(message: Message) -> None:
    """Отправляет приветствие и главное меню."""
    await message.answer(
        "Здравствуйте! 👋\n\n"
        "Вы обратились в «Мастер-Ломастер».\n\n"
        "Поможем с мелким ремонтом, сантехникой, электрикой, мебелью "
        "и другими домашними работами.\n\n"
        "Выберите нужный раздел:",
        keyboard=MAIN_MENU_KB,
    )


@bl.message(text=START_COMMANDS)
async def cmd_start(message: Message) -> None:
    """Команды Начать/Старт/Меню/menu/start — показывают главное меню."""
    user_states.pop(message.from_id, None)
    await send_main_menu(message)


@bl.message(text="🏠 Главное меню")
async def cmd_home(message: Message) -> None:
    """Кнопка «Главное меню» — всегда возвращает в основное меню."""
    user_states.pop(message.from_id, None)
    await send_main_menu(message)


@bl.message(text="🔧 Услуги")
async def cmd_services(message: Message) -> None:
    """Показывает список категорий услуг."""
    user_states.pop(message.from_id, None)
    await message.answer("Выберите категорию работ:", keyboard=SERVICES_KB)


@bl.message(text=list(CATEGORY_BUTTONS.keys()))
async def cmd_category(message: Message) -> None:
    """Показывает выбранную категорию услуг."""
    user_states.pop(message.from_id, None)
    key = CATEGORY_BUTTONS[message.text]
    await message.answer(format_category_text(key), keyboard=CATEGORY_NAV_KB)


@bl.message(text="⬅ К услугам")
async def cmd_back_to_services(message: Message) -> None:
    """Возвращает к списку категорий услуг."""
    user_states.pop(message.from_id, None)
    await message.answer("Выберите категорию работ:", keyboard=SERVICES_KB)


@bl.message(text="💰 Прайс")
async def cmd_price(message: Message) -> None:
    """Показывает краткий прайс."""
    user_states.pop(message.from_id, None)
    await message.answer(
        "💰 ПРИМЕРНЫЕ ЦЕНЫ\n\n"
        "🚰 Сантехника — от 1000 ₽\n"
        "⚡ Электрика — от 700 ₽\n"
        "🪛 Сборка мебели — от 1000 ₽\n"
        "🔨 Мелкий ремонт — от 700 ₽\n"
        "🖼 Монтаж и крепление — от 500 ₽\n\n"
        "Минимальная стоимость выезда мастера: 1500 ₽.\n\n"
        "Итоговая цена определяется после уточнения задачи.",
        keyboard=PRICE_KB,
    )


@bl.message(text="🔧 Посмотреть услуги")
async def cmd_price_to_services(message: Message) -> None:
    """Из прайса — к списку услуг."""
    user_states.pop(message.from_id, None)
    await message.answer("Выберите категорию работ:", keyboard=SERVICES_KB)


@bl.message(text="📞 Контакты")
async def cmd_contacts(message: Message) -> None:
    """Показывает контакты."""
    user_states.pop(message.from_id, None)
    await message.answer(
        "📞 МАСТЕР-ЛОМАСТЕР\n\n"
        f"Телефон:\n{MASTER_PHONE}\n\n"
        "Время работы:\nПн–Вс: 09:00–21:00\n\n"
        "Заявки через сообщения сообщества принимаются круглосуточно.",
        keyboard=BACK_TO_MAIN_KB,
    )


@bl.message(text="ℹ️ О нас")
async def cmd_about(message: Message) -> None:
    """Показывает информацию о сообществе."""
    user_states.pop(message.from_id, None)
    await message.answer(
        "🔧 «МАСТЕР-ЛОМАСТЕР»\n\n"
        "Поможем решить небольшие бытовые задачи, не нужно искать "
        "разных специалистов.\n\n"
        "Основные направления:\n"
        "🚰 сантехника\n"
        "⚡ электрика\n"
        "🪛 мебель\n"
        "🔨 мелкий ремонт\n"
        "🖼 монтаж и крепление\n\n"
        "Вы описываете задачу — мы уточняем детали и согласовываем "
        "стоимость и время выполнения.",
        keyboard=BACK_TO_MAIN_KB,
    )


@bl.message(text="📝 Оставить заявку")
async def cmd_request_start(message: Message) -> None:
    """Начинает пошаговый сценарий создания заявки (шаг 1)."""
    user_states[message.from_id] = {"step": "waiting_task"}
    await message.answer(
        "Опишите, пожалуйста, что необходимо сделать.\n\n"
        "Например:\n"
        "«Нужно заменить смеситель на кухне»\n"
        "или\n"
        "«Нужно собрать шкаф».",
        keyboard=REQUEST_FORM_KB,
    )


@bl.message(text=CANCEL_COMMANDS)
async def cmd_cancel(message: Message) -> None:
    """Отменяет создание заявки, если пользователь в процессе её заполнения."""
    if message.from_id in user_states:
        user_states.pop(message.from_id, None)
        await message.answer("Создание заявки отменено.", keyboard=MAIN_MENU_KB)
    else:
        # Если заявка не заполнялась — просто показываем главное меню
        await send_main_menu(message)


@bl.message()
async def fallback(message: Message) -> None:
    """Универсальный обработчик (самый последний).

    Если пользователь в процессе создания заявки — ведёт по шагам
    (задача -> имя -> телефон -> время). Иначе отвечает на неизвестную команду.
    """
    user_id = message.from_id
    state = user_states.get(user_id)
    text = (message.text or "").strip()

    # --- Нет состояния: неизвестная команда ---
    if state is None:
        await message.answer(
            "Не удалось распознать команду 🤔\n\n"
            "Пожалуйста, выберите нужный раздел с помощью кнопок меню.",
            keyboard=MAIN_MENU_KB,
        )
        return

    step = state.get("step")

    # --- Шаг 1: описание задачи ---
    if step == "waiting_task":
        if not text:
            await message.answer(
                "Пожалуйста, опишите задачу текстом.\n\n"
                "Например: «Нужно заменить смеситель».",
                keyboard=REQUEST_FORM_KB,
            )
            return
        state["task"] = text
        state["step"] = "waiting_name"
        await message.answer("Как к вам обращаться?", keyboard=REQUEST_FORM_KB)
        return

    # --- Шаг 2: имя ---
    if step == "waiting_name":
        if not text:
            await message.answer(
                "Пожалуйста, укажите ваше имя.", keyboard=REQUEST_FORM_KB
            )
            return
        state["name"] = text
        state["step"] = "waiting_phone"
        await message.answer(
            "Укажите номер телефона для связи.\n\nНапример:\n+7 999 123-45-67",
            keyboard=REQUEST_FORM_KB,
        )
        return

    # --- Шаг 3: телефон (с проверкой и повторным вводом) ---
    if step == "waiting_phone":
        if not is_phone_valid(text):
            await message.answer(
                "Похоже, номер телефона указан неверно.\n\n"
                "Попробуйте ещё раз.\n\nНапример:\n+7 999 123-45-67",
                keyboard=REQUEST_FORM_KB,
            )
            return
        state["phone"] = normalize_phone(text)
        state["step"] = "waiting_time"
        await message.answer(
            "Когда вам удобно принять мастера?\n\n"
            "Например:\n"
            "Сегодня после 18:00\n"
            "или\n"
            "Завтра с 10:00 до 14:00",
            keyboard=REQUEST_FORM_KB,
        )
        return

    # --- Шаг 4: удобное время -> сохраняем заявку ---
    if step == "waiting_time":
        if not text:
            await message.answer(
                "Пожалуйста, укажите удобное время для визита мастера.",
                keyboard=REQUEST_FORM_KB,
            )
            return
        state["preferred_time"] = text

        request = {
            "vk_user_id": user_id,
            "name": state["name"],
            "phone": state["phone"],
            "task": state["task"],
            "preferred_time": state["preferred_time"],
        }
        try:
            add_request(request)
        except Exception:
            logger.exception("Ошибка сохранения заявки от vk_user_id=%s", user_id)
            user_states.pop(user_id, None)
            await message.answer(
                "Не удалось сохранить заявку. Попробуйте позже.",
                keyboard=MAIN_MENU_KB,
            )
            return

        logger.info("Создана заявка: vk_user_id=%s, имя=%s", user_id, request["name"])
        user_states.pop(user_id, None)

        await message.answer(
            "✅ ЗАЯВКА СОЗДАНА\n\n"
            f"Имя: {request['name']}\n\n"
            f"Телефон: {request['phone']}\n\n"
            "Задача:\n"
            f"{request['task']}\n\n"
            "Удобное время:\n"
            f"{request['preferred_time']}\n\n"
            "Мы свяжемся с вами для уточнения деталей.\n\n"
            "Спасибо, что выбрали «Мастер-Ломастер»! 🔧",
            keyboard=AFTER_REQUEST_KB,
        )
        return

    # --- Неизвестное состояние (страховка) ---
    user_states.pop(user_id, None)
    await send_main_menu(message)

"""Клавиатуры VK для всех разделов бота."""

from vkbottle import Keyboard, Text

# Главное меню
MAIN_MENU_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("🔧 Услуги"))
    .add(Text("💰 Прайс"))
    .row()
    .add(Text("📝 Оставить заявку"))
    .add(Text("📞 Контакты"))
    .row()
    .add(Text("ℹ️ О нас"))
    .get_json()
)

# Список категорий услуг
SERVICES_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("🚰 Сантехника"))
    .add(Text("⚡ Электрика"))
    .row()
    .add(Text("🪛 Сборка и ремонт мебели"))
    .add(Text("🔨 Мелкий ремонт"))
    .row()
    .add(Text("🖼 Установка и крепление"))
    .row()
    .add(Text("⬅ Главное меню"))
    .get_json()
)

# Кнопки навигации внутри категории услуг
CATEGORY_NAV_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("📝 Оставить заявку"))
    .row()
    .add(Text("⬅ К услугам"))
    .add(Text("🏠 Главное меню"))
    .get_json()
)

# Прайс
PRICE_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("🔧 Посмотреть услуги"))
    .row()
    .add(Text("📝 Оставить заявку"))
    .add(Text("🏠 Главное меню"))
    .get_json()
)

# Простая клавиатура только с кнопкой «Главное меню» (Контакты, О нас)
BACK_TO_MAIN_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("🏠 Главное меню"))
    .get_json()
)

# Клавиатура на время заполнения заявки (шаги 1-4)
REQUEST_FORM_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("❌ Отмена"))
    .row()
    .add(Text("🏠 Главное меню"))
    .get_json()
)

# После подтверждения заявки
AFTER_REQUEST_KB = (
    Keyboard(one_time=False, inline=False)
    .add(Text("🏠 Главное меню"))
    .get_json()
)

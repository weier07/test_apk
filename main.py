from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

# --- ЦВЕТОВАЯ ПАЛИТРА В КИТАЙСКОМ СТИЛЕ ---
COLOR_BG = (0.12, 0.08, 0.08, 1)  # Темно-углистый / глубокий фон
COLOR_RED = (0.6, 0.1, 0.1, 1)  # Традиционный киноварно-красный
COLOR_GOLD = (0.85, 0.65, 0.2, 1)  # Золотой
COLOR_CARD = (0.18, 0.12, 0.12, 1)  # Темно-бордовый для карточек
COLOR_TEXT = (0.95, 0.9, 0.8, 1)  # Теплый кремовый текст

# --- БАЗА ДАННЫХ ЦИТАТ И ПОСЛОВИЦ ---
DATA = [
    {
        "id": 1,
        "text": "Путешествие в тысячу ли начинается с первого шага.",
        "author": "Лао-цзы",
        "category": "Пословица"
    },
    {
        "id": 2,
        "text": "Тот, кто указывает на твои недостатки, не всегда твой враг; тот, кто говорит о твоих достоинствах, не всегда твой друг.",
        "author": "Китайская мудрость",
        "category": "Пословица"
    },
    {
        "id": 3,
        "text": "В конце концов, в этом мире нет ничего вечного. Ни страданий, ни счастья.",
        "author": "«Благословение небожителей»",
        "category": "Новелла"
    },
    {
        "id": 4,
        "text": "Если ты не знаешь, ради чего жить, живи ради меня.",
        "author": "«Благословение небожителей»",
        "category": "Новелла"
    },
    {
        "id": 5,
        "text": "Лучшее время, чтобы посадить дерево, было 20 лет назад. Следующее лучшее время — сегодня.",
        "author": "Народное изречение",
        "category": "Пословица"
    },
    {
        "id": 6,
        "text": "Человек может умереть за того, кто его понимает.",
        "author": "«Магистр дьявольского культа»",
        "category": "Новелла"
    }
]

# Глобальное множество для хранения ID избранных цитат
FAVORITES = set()


def create_colored_bg(widget, color):
    """Вспомогательная функция для добавления цветного фона виджету."""
    with widget.canvas.before:
        Color(*color)
        widget.rect = Rectangle(size=widget.size, pos=widget.pos)
    widget.bind(size=lambda w, val: setattr(w.rect, 'size', val),
                pos=lambda w, val: setattr(w.rect, 'pos', val))


class ColoredBoxLayout(BoxLayout):
    """BoxLayout с возможностью задать фоновый цвет."""

    def __init__(self, bg_color=COLOR_BG, **kwargs):
        super().__init__(**kwargs)
        create_colored_bg(self, bg_color)


class MainScreen(Screen):
    """Главный экран приложения."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = ColoredBoxLayout(bg_color=COLOR_BG, orientation='vertical', padding=15, spacing=15)

        # Шапка главного экрана
        header = ColoredBoxLayout(bg_color=COLOR_RED, size_hint_y=0.12, padding=10)
        title = Label(
            text="中華名言\nКитаеведение & Цитаты",
            font_size='20sp',
            bold=True,
            color=COLOR_GOLD,
            halign='center'
        )
        header.add_widget(title)
        main_layout.add_widget(header)

        # Кнопка перехода в Избранное
        fav_btn = Button(
            text="★ Избранное",
            size_hint_y=0.08,
            background_normal='',
            background_color=COLOR_GOLD,
            color=(0, 0, 0, 1),
            bold=True
        )
        fav_btn.bind(on_press=self.go_to_favorites)
        main_layout.add_widget(fav_btn)

        # Прокручиваемый список цитат
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=15, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        scroll.add_widget(self.grid)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Обновление списка при каждом входе на экран."""
        self.build_list()

    def build_list(self):
        self.grid.clear_widgets()
        for item in DATA:
            card = self.create_quote_card(item)
            self.grid.add_widget(card)

    def create_quote_card(self, item):
        card = ColoredBoxLayout(
            bg_color=COLOR_CARD,
            orientation='vertical',
            size_hint_y=None,
            height=160,
            padding=10,
            spacing=5
        )

        cat_label = Label(
            text=f"[{item['category']}]",
            color=COLOR_GOLD,
            size_hint_y=0.2,
            halign='left'
        )
        cat_label.bind(size=cat_label.setter('text_size'))

        text_label = Label(
            text=f"«{item['text']}»",
            color=COLOR_TEXT,
            size_hint_y=0.5,
            valign='middle',
            halign='left'
        )
        text_label.bind(size=text_label.setter('text_size'))

        author_label = Label(
            text=f"— {item['author']}",
            color=COLOR_GOLD,
            size_hint_y=0.15,
            halign='right'
        )
        author_label.bind(size=author_label.setter('text_size'))

        # Кнопка добавления / удаления из Избранного
        is_fav = item['id'] in FAVORITES
        fav_btn = Button(
            text="♥ В избранном" if is_fav else "♡ В избранное",
            size_hint_y=0.15,
            background_normal='',
            background_color=COLOR_RED if is_fav else (0.3, 0.3, 0.3, 1),
            color=COLOR_TEXT
        )
        fav_btn.bind(on_press=lambda btn, q_id=item['id']: self.toggle_favorite(q_id, btn))

        card.add_widget(cat_label)
        card.add_widget(text_label)
        card.add_widget(author_label)
        card.add_widget(fav_btn)

        return card

    def toggle_favorite(self, quote_id, button):
        if quote_id in FAVORITES:
            FAVORITES.remove(quote_id)
            button.text = "♡ В избранное"
            button.background_color = (0.3, 0.3, 0.3, 1)
        else:
            FAVORITES.add(quote_id)
            button.text = "♥ В избранном"
            button.background_color = COLOR_RED

    def go_to_favorites(self, instance):
        self.manager.current = 'favorites'


class FavoritesScreen(Screen):
    """Экран избранных цитат."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = ColoredBoxLayout(bg_color=COLOR_BG, orientation='vertical', padding=15, spacing=15)

        # Верхняя панель с кнопкой «Назад»
        nav_bar = ColoredBoxLayout(bg_color=COLOR_RED, size_hint_y=0.1, padding=5, spacing=10)

        back_btn = Button(
            text="◀ Главная",
            size_hint_x=0.3,
            background_normal='',
            background_color=COLOR_GOLD,
            color=(0, 0, 0, 1),
            bold=True
        )
        back_btn.bind(on_press=self.go_home)

        title = Label(
            text="Избранное",
            font_size='18sp',
            bold=True,
            color=COLOR_TEXT
        )

        nav_bar.add_widget(back_btn)
        nav_bar.add_widget(title)
        main_layout.add_widget(nav_bar)

        # Список избранных элементов
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=15, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        scroll.add_widget(self.grid)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def on_enter(self):
        """Рендеринг сохраненных цитат при входе на экран."""
        self.grid.clear_widgets()
        fav_items = [item for item in DATA if item['id'] in FAVORITES]

        if not fav_items:
            empty_label = Label(
                text="У вас пока нет сохраненных цитат",
                color=COLOR_TEXT,
                size_hint_y=None,
                height=100
            )
            self.grid.add_widget(empty_label)
            return

        for item in fav_items:
            card = ColoredBoxLayout(
                bg_color=COLOR_CARD,
                orientation='vertical',
                size_hint_y=None,
                height=140,
                padding=10,
                spacing=5
            )

            text_label = Label(
                text=f"«{item['text']}»",
                color=COLOR_TEXT,
                size_hint_y=0.6,
                valign='middle',
                halign='left'
            )
            text_label.bind(size=text_label.setter('text_size'))

            author_label = Label(
                text=f"— {item['author']} [{item['category']}]",
                color=COLOR_GOLD,
                size_hint_y=0.2,
                halign='right'
            )
            author_label.bind(size=author_label.setter('text_size'))

            remove_btn = Button(
                text="Удалить из избранного",
                size_hint_y=0.2,
                background_normal='',
                background_color=(0.5, 0.1, 0.1, 1),
                color=COLOR_TEXT
            )
            remove_btn.bind(on_press=lambda btn, q_id=item['id']: self.remove_favorite(q_id))

            card.add_widget(text_label)
            card.add_widget(author_label)
            card.add_widget(remove_btn)

            self.grid.add_widget(card)

    def remove_favorite(self, quote_id):
        FAVORITES.remove(quote_id)
        self.on_enter()  # Перерисовываем список

    def go_home(self, instance):
        self.manager.current = 'main'


class ChineseQuotesApp(App):
    def build(self):
        self.title = "Китайские Пословицы и Цитаты"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FavoritesScreen(name='favorites'))
        return sm


if __name__ == '__main__':
    ChineseQuotesApp().run()

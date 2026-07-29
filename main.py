# импортируем класс App из модуля kivy.app
# используется для создания приложения
from kivy.app import App 
# подключаем инструмент дляя вывода надписи
from kivy.uix.label import Label
from kivy.uix.button import Button
# позволяет располагать элементы друг за другом
from kivy.uix.boxlayout import BoxLayout

class MyFirstApp(App): # создаёт объект приложения
    # позволяет автоматически вызывать, когда приложение запускается
    def build(self): # self - ссылка на текущий объект приложения
        # создаем контейнер для элементов приложения
        screen = BoxLayout(
            orientation="vertical", # расположение элементов
            padding=10, # оступ от краёв окна, иначе элементы будут почти вплотную к рамке окна
            spacing=20 # расстояние между элементами
        )
        # создаём заголовок 
        self.title_label =Label(
            text="Моё первое приложение",
            font_size=20 # размер шрифта
        )
        # создаем второй текст
        self.info_label = Label(
            text="Приложение создано для Python",
            font_size = 20
        )
        # создаем кнопку 
        self.start_button = Button(
            text="Нажми",
            font_size=22,
            size_hint=(1, 0.3) # размер кнопки (1 - занимает всю ширину окна, 0.3 - занимает 30% высоты относительно доступного пространства)

        )
        # связываем кнопку с функцией
        self.start_button.bind(on_press=self.button_clicked)

        # добавляем элементы на экран
        screen.add_widget(self.title_label)
        screen.add_widget(self.info_label)
        screen.add_widget(self.start_button)

        return screen

    def button_clicked(self, button):
        self.info_label.text = "Кнопка работает!"

MyFirstApp().run()

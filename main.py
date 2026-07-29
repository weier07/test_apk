from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MainApp(App):
    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20,
        )

        label = Label(text="Приложение собрано в APK")
        button = Button(text="Нажми меня")

        def change_text(instance):
            label.text = "Всё работает!"

        button.bind(on_press=change_text)

        layout.add_widget(label)
        layout.add_widget(button)
        return layout


MainApp().run()

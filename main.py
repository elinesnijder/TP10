from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import sqlite3


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        welcome_label = Label(text='Bem-vindo')
        start_button = Button(text='Começar')
        start_button.bind(on_press=self.go_to_order_screen)
        layout.add_widget(welcome_label)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def go_to_order_screen(self, instance):
        self.manager.current = 'order'


class OrderScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        hamburguers_label = Label(text='Escolha um Hambúrguer:')
        layout.add_widget(hamburguers_label)

        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome_hamburguer, preco FROM Hamburguers')
        hamburguers_data = cursor.fetchall()
        conn.close()

        for hamburguer in hamburguers_data:
            hamburguer_button = Button(text=f'{hamburguer[0]} - R${hamburguer[1]}',
                                       size_hint_y=None,
                                       height=40)
            hamburguer_button.bind(on_press=self.select_hamburguer)
            layout.add_widget(hamburguer_button)

        self.add_widget(layout)

    def select_hamburguer(self, instance):
        hamburguer_name = instance.text.split('-')[0].strip()
        self.manager.current = 'details' 
        self.manager.get_screen('details').load_hamburguer_details(hamburguer_name)


class HamburguerDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(HamburguerDetailsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.hamburguer_name_label = Label(text='Nome do Hambúrguer:')
        self.hamburguer_ingredients_label = Label(text='Ingredientes:')
        self.hamburguer_price_label = Label(text='Preço:')
        layout.add_widget(self.hamburguer_name_label)
        layout.add_widget(self.hamburguer_ingredients_label)
        layout.add_widget(self.hamburguer_price_label)
        self.add_widget(layout)

    def load_hamburguer_details(self, hamburguer_name):
        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ingredientes, preco FROM Hamburguers WHERE nome_hamburguer=?', (hamburguer_name,))
        hamburguer_data = cursor.fetchone()
        conn.close()

        if hamburguer_data:
            self.hamburguer_name_label.text = f'Nome do Hambúrguer: {hamburguer_name}'
            self.hamburguer_ingredients_label.text = f'Ingredientes: {hamburguer_data[0]}'
            self.hamburguer_price_label.text = f'Preço: R${hamburguer_data[1]}'
        else:
            self.hamburguer_name_label.text = 'Erro ao carregar detalhes do hambúrguer.'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(OrderScreen(name='order'))
        sm.add_widget(HamburguerDetailsScreen(name='details'))
        return sm


if __name__ == '__main__':
    MyApp().run()

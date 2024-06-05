from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
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

        # Conectar ao banco de dados e recuperar os hambúrgueres
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
        hamburguer_name = instance.text.split('-')[0].strip()  # Pega apenas o nome do hambúrguer
        self.manager.current = 'details'  # Muda para a tela de detalhes do hambúrguer
        # Passa o nome do hambúrguer para a próxima tela
        details_screen = self.manager.get_screen('details')
        details_screen.load_hamburguer_details(hamburguer_name)
        details_screen.previous_screen = self.name  # Armazena o nome da tela anterior


class HamburguerDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(HamburguerDetailsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.hamburguer_name_label = Label(text='Nome do Hambúrguer:')
        self.hamburguer_ingredients_label = Label(text='Ingredientes:')
        self.hamburguer_price_label = Label(text='Preço:')
        self.layout.add_widget(self.hamburguer_name_label)
        self.layout.add_widget(self.hamburguer_ingredients_label)
        self.layout.add_widget(self.hamburguer_price_label)

        # Botões para voltar e continuar
        self.back_button = Button(text='Voltar')
        self.continue_button = Button(text='Continuar')
        self.back_button.bind(on_press=self.go_back)
        self.continue_button.bind(on_press=self.continue_order)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.continue_button)

        self.add_widget(self.layout)

    def load_hamburguer_details(self, hamburguer_name):
        # Conectar ao banco de dados e recuperar os detalhes do hambúrguer
        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ingredientes, preco FROM Hamburguers WHERE nome_hamburguer=?', (hamburguer_name,))
        hamburguer_data = cursor.fetchone()
        conn.close()

        if hamburguer_data:
            self.hamburguer_name_label.text = f'Nome do Hambúrguer: {hamburguer_name}'
            self.hamburguer_ingredients_label.text = f'Ingredientes: {hamburguer_data[0]}'
            self.hamburguer_price_label.text = f'Preço: R${hamburguer_data[1]}'
            self.hamburguer_price = hamburguer_data[1]  # Armazena o preço do hambúrguer
        else:
            self.hamburguer_name_label.text = 'Erro ao carregar detalhes do hambúrguer.'

    def go_back(self, instance):
        if hasattr(self, 'previous_screen'):
            self.manager.current = self.previous_screen

    def continue_order(self, instance):
        # Adicionando a seleção do tamanho
        self.layout.clear_widgets()  # Limpa os widgets atuais
        size_label = Label(text='Selecione o tamanho do hambúrguer:')
        size_spinner = Spinner(text='Infantil', values=('Infantil', 'Normal', 'Duplo'))
        size_layout = GridLayout(cols=3)
        size_layout.add_widget(size_label)
        size_layout.add_widget(size_spinner)
        self.layout.add_widget(size_layout)

        # Botões para selecionar a quantidade
        quantity_label = Label(text='Selecione a quantidade:')
        self.quantity_label = Label(text='1')
        plus_button = Button(text='+')
        minus_button = Button(text='-')
        plus_button.bind(on_press=self.increment_quantity)
        minus_button.bind(on_press=self.decrement_quantity)
        quantity_layout = BoxLayout()
        quantity_layout.add_widget(quantity_label)
        quantity_layout.add_widget(minus_button)
        quantity_layout.add_widget(self.quantity_label)
        quantity_layout.add_widget(plus_button)
        self.layout.add_widget(quantity_layout)

        # Rótulo para mostrar o preço total
        self.total_price_label = Label(text=f'Preço total: R${self.hamburguer_price}')
        self.layout.add_widget(self.total_price_label)

        confirm_button = Button(text='Confirmar')
        confirm_button.bind(on_press=self.confirm_order)
        self.layout.add_widget(confirm_button)

    def increment_quantity(self, instance):
        quantity = int(self.quantity_label.text)
        quantity += 1
        self.quantity_label.text = str(quantity)
        self.update_total_price()

    def decrement_quantity(self, instance):
        quantity = int(self.quantity_label.text)
        if quantity > 1:
            quantity -= 1
            self.quantity_label.text = str(quantity)
            self.update_total_price()

    def update_total_price(self):
        quantity = int(self.quantity_label.text)
        total_price = self.hamburguer_price * quantity
        self.total_price_label.text = f'Preço total: R${total_price}'

    def confirm_order(self, instance):
        # Aqui você pode obter o tamanho selecionado, a quantidade e fazer o que for necessário, como adicionar ao pedido
        selected_size = self.layout.children[2].children[1].text  # O segundo widget do primeiro GridLayout é o Spinner
        quantity = int(self.quantity_label.text)
        total_price = self.hamburguer_price * quantity
        print(f'Tamanho selecionado: {selected_size}, Quantidade: {quantity}, Preço total: R${total_price}')


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(OrderScreen(name='order'))
        sm.add_widget(HamburguerDetailsScreen(name='details'))
        return sm


if __name__ == '__main__':
    MyApp().run()

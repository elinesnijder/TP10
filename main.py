from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
import sqlite3


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        welcome_label = Label(text='Bem-vindo')
        employee_auth_button = Button(text='Autenticação do Funcionário do Call Center')
        employee_auth_button.bind(on_press=self.go_to_employee_auth)
        main_system_button = Button(text='Acesso ao Sistema Principal')
        main_system_button.bind(on_press=self.go_to_main_system)
        layout.add_widget(welcome_label)
        layout.add_widget(employee_auth_button)
        layout.add_widget(main_system_button)
        self.add_widget(layout)

    def go_to_employee_auth(self, instance):
        # Limpa a tela atual
        self.clear_widgets()
        
        # Criação de elementos para a autenticação do funcionário
        auth_layout = BoxLayout(orientation='vertical')
        username_input = TextInput(hint_text='Nome de usuário')
        password_input = TextInput(hint_text='Senha', password=True)
        confirm_button = Button(text='Confirmar')
        
        # Função para lidar com a autenticação
        def authenticate(instance):
            # Verifica o nome de usuário e a senha
            if username_input.text == 'admin' and password_input.text == '123456':
                # Limpa a tela de autenticação e exibe as opções
                auth_layout.clear_widgets()
                options_label = Label(text='Selecione uma opção:')
                view_orders_button = Button(text='Ver Pedidos')
                view_customers_button = Button(text='Ver Clientes')
                view_hamburguers_button = Button(text='Ver Hamburguers')
                
                # Ações dos botões
                def view_orders(instance):
                    # Conectar ao banco de dados e recuperar os pedidos
                    conn = sqlite3.connect('hamburgueria.db')
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT p.id, c.nome, p.nome_hamburguer, p.quantidade, p.tamanho, p.valor_total 
                        FROM Pedidos p
                        JOIN Clientes c ON p.id_cliente = c.id
                    ''')
                    orders_data = cursor.fetchall()
                    conn.close()

                    # Adicionar informações dos pedidos ao layout
                    orders_layout = BoxLayout(orientation='vertical')
                    for order in orders_data:
                        order_label = Label(text=f'Pedido ID: {order[0]}, Cliente: {order[1]}, Hambúrguer: {order[2]}, Quantidade: {order[3]}, Tamanho: {order[4]}, Valor: R${order[5]}')
                        orders_layout.add_widget(order_label)

                    # Limpa a tela atual e adiciona o novo layout
                    self.clear_widgets()
                    self.add_widget(orders_layout)
                
                def view_customers(instance):
                    # Implemente a lógica para visualizar os clientes
                    conn = sqlite3.connect('hamburgueria.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT nome, morada, telefone FROM Clientes')
                    customers_data = cursor.fetchall()
                    conn.close()

                    # Adicionar informações dos clientes ao layout
                    for customer in customers_data:
                        customer_label = Label(text=f'Nome: {customer[0]}, Morada: {customer[1]}, Telefone: {customer[2]}')
                        instance.parent.add_widget(customer_label)  # Adiciona ao layout pai da instância (o layout da tela atual)

                
                def view_hamburguers(instance):
                   # Conectar ao banco de dados e recuperar os hambúrgueres
                    conn = sqlite3.connect('hamburgueria.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT nome_hamburguer, ingredientes, preco FROM Hamburguers')
                    hamburguers_data = cursor.fetchall()
                    conn.close()

                    # Adicionar informações dos hambúrgueres ao layout
                    hamburguers_layout = BoxLayout(orientation='vertical')
                    for hamburguer in hamburguers_data:
                        hamburguer_label = Label(text=f'Nome: {hamburguer[0]}, Ingredientes: {hamburguer[1]}, Preço: R${hamburguer[2]}')
                        hamburguers_layout.add_widget(hamburguer_label)

                    # Limpa a tela atual e adiciona o novo layout
                    self.clear_widgets()
                    self.add_widget(hamburguers_layout)
                
                # Associações de eventos
                view_orders_button.bind(on_press=view_orders)
                view_customers_button.bind(on_press=view_customers)
                view_hamburguers_button.bind(on_press=view_hamburguers)
                
                # Adiciona os elementos à tela
                auth_layout.add_widget(options_label)
                auth_layout.add_widget(view_orders_button)
                auth_layout.add_widget(view_customers_button)
                auth_layout.add_widget(view_hamburguers_button)
            
            else:
                # Exibe uma mensagem de erro se as credenciais forem inválidas
                invalid_label = Label(text='Credenciais inválidas. Tente novamente.')
                auth_layout.add_widget(invalid_label)

        # Associa o evento de clique do botão de confirmação com a função de autenticação
        confirm_button.bind(on_press=authenticate)
        
        # Adiciona os elementos à tela
        auth_layout.add_widget(username_input)
        auth_layout.add_widget(password_input)
        auth_layout.add_widget(confirm_button)
        self.add_widget(auth_layout)


    def go_to_main_system(self, instance):
        self.manager.current = 'order'  # Direciona para o sistema principal



class OrderScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.populate_hamburguers()

    def populate_hamburguers(self):
        self.layout.clear_widgets()
        hamburguers_label = Label(text='Escolha um Hambúrguer:')
        self.layout.add_widget(hamburguers_label)

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
            self.layout.add_widget(hamburguer_button)

        # Adiciona um botão para revisar o pedido
        review_button = Button(text='Revisar Pedido')
        review_button.bind(on_press=self.review_order)
        self.layout.add_widget(review_button)

    def select_hamburguer(self, instance):
        hamburguer_name = instance.text.split('-')[0].strip()  # Pega apenas o nome do hambúrguer
        self.manager.current = 'details'  # Muda para a tela de detalhes do hambúrguer
        # Passa o nome do hambúrguer para a próxima tela
        details_screen = self.manager.get_screen('details')
        details_screen.load_hamburguer_details(hamburguer_name)
        details_screen.previous_screen = self.name  # Armazena o nome da tela anterior

    def review_order(self, instance):
        self.manager.current = 'review'


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
        self.hamburguer_name = hamburguer_name
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
        type_label = Label(text=f'Tipo de Hambúrguer: {self.hamburguer_name}')
        self.layout.add_widget(type_label)

        size_label = Label(text='Selecione o tamanho do hambúrguer:')
        self.size_spinner = Spinner(text='Escolha o tamanho', values=('infantil', 'normal', 'duplo'))
        size_layout = GridLayout(cols=2)
        size_layout.add_widget(size_label)
        size_layout.add_widget(self.size_spinner)
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
        selected_size = self.size_spinner.text  # Obtém o tamanho selecionado do Spinner
        quantity = int(self.quantity_label.text)
        total_price = self.hamburguer_price * quantity
        order_screen = self.manager.get_screen('order')
        order_screen.layout.add_widget(Button(text=f'{self.hamburguer_name} - {selected_size} x{quantity} - R${total_price}'))
        review_screen = self.manager.get_screen('review')
        review_screen.add_order(f'{self.hamburguer_name} - {selected_size} x{quantity} - R${total_price}', total_price)
        self.manager.current = 'order'


class ReviewOrderScreen(Screen):
    def __init__(self, **kwargs):
        super(ReviewOrderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.orders_label = Label(text='Seu Pedido:')
        self.total_price_label = Label(text='Preço total do pedido: R$0')
        self.layout.add_widget(self.orders_label)
        self.layout.add_widget(self.total_price_label)
        self.add_widget(self.layout)
        self.orders = []
        self.total_price = 0

        # Campos para informações do cliente
        self.name_input = TextInput(hint_text='Nome')
        self.address_input = TextInput(hint_text='Morada')
        self.phone_input = TextInput(hint_text='Telemóvel')
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.address_input)
        self.layout.add_widget(self.phone_input)

        # Botões de confirmar e voltar
        self.buttons_layout = BoxLayout(size_hint_y=None, height=50)
        self.confirm_button = Button(text='Confirmar Pedido')
        self.back_button = Button(text='Voltar')
        self.confirm_button.bind(on_press=self.confirm_order)
        self.back_button.bind(on_press=self.go_back)
        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.confirm_button)
        self.layout.add_widget(self.buttons_layout)

    def add_order(self, order_text, price):
        self.orders.append(order_text)
        self.total_price += price
        self.orders_label.text += f'\n{order_text}'
        self.total_price_label.text = f'Preço total do pedido: R${self.total_price}'

    def confirm_order(self, instance):
    # Obtenha os dados do cliente
        name = self.name_input.text
        address = self.address_input.text
        phone = self.phone_input.text

        # Conectar ao banco de dados e salvar o pedido
        conn = sqlite3.connect('hamburgueria.db')
        cursor = conn.cursor()

        # Inserir dados do cliente
        cursor.execute('INSERT INTO Clientes (nome, morada, telefone) VALUES (?, ?, ?)', (name, address, phone))
        cliente_id = cursor.lastrowid  # Obtenha o ID do cliente recém-inserido
        print(f"Cliente registrado com ID {cliente_id}")

        # Preparar os dados dos pedidos
        for order in self.orders:
            nome_hamburguer = order.split(' - ')[0]
            quantidade = int(order.split(' x')[1].split(' - ')[0])
            tamanho = order.split(' - ')[1].lower()  # Converta para minúsculas para facilitar a comparação
            valor_total = float(order.split(' - ')[2][3:])

            # Verificar se o tamanho é válido
            if tamanho not in ('infantil', 'normal', 'duplo'):
                print(f"Tamanho de hambúrguer inválido: {tamanho}. Pedido não foi registrado.")
                continue  # Pule este pedido e passe para o próximo

            # Inserir dados do pedido
            cursor.execute('INSERT INTO Pedidos (id_cliente, nome_hamburguer, quantidade, tamanho, valor_total) VALUES (?, ?, ?, ?, ?)',
                        (cliente_id, nome_hamburguer, quantidade, tamanho, valor_total))
            pedido_id = cursor.lastrowid  # Obtenha o ID do pedido recém-inserido
            print(f"Pedido registrado com ID {pedido_id} para o cliente {cliente_id}")

        conn.commit()
        conn.close()


        # Limpar os pedidos e campos de entrada após a confirmação
        self.orders.clear()
        self.total_price = 0
        self.orders_label.text = 'Seu Pedido:'
        self.total_price_label.text = 'Preço total do pedido: R$0'
        self.name_input.text = ''
        self.address_input.text = ''
        self.phone_input.text = ''

        self.manager.current = 'welcome'

    def go_back(self, instance):
        self.manager.current = 'order'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(OrderScreen(name='order'))
        sm.add_widget(HamburguerDetailsScreen(name='details'))
        sm.add_widget(ReviewOrderScreen(name='review'))
        return sm


if __name__ == '__main__':
    MyApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import requests

class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.add_widget(Label(text='Nome do Cliente:'))
        self.nome_cliente = TextInput()
        self.add_widget(self.nome_cliente)
        
        self.add_widget(Label(text='Morada:'))
        self.morada = TextInput()
        self.add_widget(self.morada)
        
        self.add_widget(Label(text='Telefone:'))
        self.telefone = TextInput()
        self.add_widget(self.telefone)
        
        self.add_widget(Label(text='Hamburguer:'))
        self.spinner_hamburguer = Spinner()
        self.add_widget(self.spinner_hamburguer)
        
        self.add_widget(Label(text='Quantidade:'))
        self.quantidade = TextInput()
        self.add_widget(self.quantidade)
        
        self.add_widget(Label(text='Tamanho (infantil, normal, duplo):'))
        self.tamanho = TextInput()
        self.add_widget(self.tamanho)
        
        self.add_widget(Label(text='Total:'))
        self.valor_total = TextInput()
        self.add_widget(self.valor_total)
        
        self.submit_button = Button(text='Registrar Pedido')
        self.submit_button.bind(on_press=self.submit)
        self.add_widget(self.submit_button)
        
        self.populate_spinner()
        
    def populate_spinner(self):
        response = requests.get('http://127.0.0.1:5000/Hamburguers')
        if response.status_code == 200:
            hamburguers = [hamburguer[0] for hamburguer in response.json()]
            self.spinner_hamburguer.values = hamburguers
            
    def submit(self, instance):
        cliente_data = {
            'nome': self.nome_cliente.text,
            'morada': self.morada.text,
            'telefone': self.telefone.text,
        }
        response = requests.post('http://127.0.0.1:5000/Clientes', json=cliente_data)
        if response.status_code == 201:
            id_cliente = response.json().get('id_cliente')
            pedidos_data = {
                'id_cliente': id_cliente,
                'nome_hamburguer': self.spinner_hamburguer.text,
                'quantidade': int(self.quantidade.text),
                'tamanho': self.tamanho.text,
                'valor_total': float(self.valor_total.text)
            }
            response_pedido = requests.post('http://127.0.0.1:5000/pedidos', json=pedidos_data)
            if response_pedido.status_code == 201:
                print("Pedido registrado com sucesso!")
            else:
                print("Erro ao registrar pedido.")
        else:
            print("Erro ao registrar cliente.")
            
class MyApp(App):
    def build(self):
        return MyWidget()
    
if __name__ == '__main__':
    MyApp().run()

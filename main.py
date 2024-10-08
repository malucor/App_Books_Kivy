import pyrebase
import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu

Window.size = (360, 640)

firebase_config = {
    "apiKey": "API_KEY",
    "authDomain": "DOMINIO.firebaseapp.com",
    "databaseURL": "https://DOMINIO.firebaseio.com/",
    "projectId": "PROJECT_ID",
    "storageBucket": "BUCKET.appspot.com",
    "messagingSenderId": "SENDER_ID",
    "appId": "APP_ID",
    "measurementId": "MEASUREMENT_ID"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

KV = '''
ScreenManager:
    LoginScreen:
    HomeScreen:
    AddBookScreen:

<LoginScreen>:
    name: 'login'

    MDBoxLayout:

        orientation: 'vertical'
        padding: 20
        spacing: 10

        MDTextField:
            id: email
            hint_text: "Email"
            pos_hint: {'center_x': 0.5}

        MDTextField:
            id: password
            hint_text: "Senha"
            password: True
            pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: "Login"
            pos_hint: {'center_x': 0.5}
            on_release: app.login(email.text, password.text)

        MDRaisedButton:
            text: "Registrar"
            pos_hint: {'center_x': 0.5}
            on_release: app.register(email.text, password.text)

<HomeScreen>:
    name: 'home'

    MDBottomNavigation:

        MDBottomNavigationItem:
            name: 'screen1'
            text: 'Livros'
            icon: 'home'

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDLabel:
                    text: 'Livros Cadastrados'
                    halign: 'center'
                
                MDTextField:
                    id: search_field
                    hint_text: "Pesquisar livro"
                    icon_right: "magnify"
                    size_hint_y: None
                    height: dp(48)
                    on_text: app.search_books(self.text)

                ScrollView:
                    MDList:
                        id: book_list

                ScrollView:
                    MDList:
                        id: book_list

                MDRaisedButton:
                    text: '+ Adicionar Livro'
                    pos_hint: {'center_x': 0.5}
                    on_release: app.show_add_book_screen()

        MDBottomNavigationItem:
            name: 'screen2'
            text: 'Estatísticas'
            icon: 'chart-bar'

            MDBoxLayout:
                id: statistics_box
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDLabel:
                    text: 'Insights'
                    halign: 'center'
                
                MDRaisedButton:
                    text: 'Atualizar Gráfico'
                    pos_hint: {'center_x': 0.5}
                    on_release: app.show_statistics()

        MDBottomNavigationItem:
            name: 'screen3'
            text: 'Perfil'
            icon: 'account'

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDLabel:
                    id: user_email
                    text: 'Email:'
                    halign: 'center'

                MDRaisedButton:
                    text: "Trocar Senha"
                    pos_hint: {'center_x': 0.5}
                    on_release: app.change_password()

                MDRaisedButton:
                    text: "Excluir Conta"
                    pos_hint: {'center_x': 0.5}
                    on_release: app.delete_account()

                MDRaisedButton:
                    text: "Sair"
                    pos_hint: {'center_x': 0.5}
                    on_release: app.logout()

        MDBottomNavigationItem:
            name: 'screen4'
            text: 'Configurações'
            icon: 'cog'

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDCard:
                    orientation: "vertical"
                    padding: 0, 0, 0 , "36dp"
                    size_hint: .5, .5
                    style: "elevated"
                    pos_hint: {"center_x": .5, "center_y": .5}

                    MDLabel:
                        text: "Tema - {}".format(app.theme_cls.theme_style)
                        halign: "center"
                        valign: "center"
                        bold: True
                        font_style: "H6"

                    MDRaisedButton:
                        text: "Mudar Tema"
                        on_release: app.switch_theme_style()
                        pos_hint: {"center_x": .5}

<AddBookScreen>:
    name: 'add_book'

    MDIconButton:
        icon: "arrow-left"
        pos_hint: {"center_x": 0.1, "center_y": 0.95}
        on_release: app.cancel_book()

    MDIconButton:
        icon: "trash-can"
        pos_hint: {"center_x": 0.9, "center_y": 0.95}
        on_release: app.delete_book()

    MDBoxLayout:
        orientation: 'vertical'
        spacing: "10dp"
        padding: "20dp"

        MDTextField:
            id: book_name
            hint_text: "Nome do Livro"
            pos_hint: {'center_x': 0.5}

        MDTextField:
            id: book_author
            hint_text: "Autor"
            pos_hint: {'center_x': 0.5}

        MDTextField:
            id: book_pages
            hint_text: "Quantidade de Páginas"
            pos_hint: {'center_x': 0.5}
            input_filter: 'int'

        MDRaisedButton:
            id: book_status_button
            text: "Selecione o Status"
            pos_hint: {'center_x': 0.5}
            on_release: app.open_status_menu()

        MDRaisedButton:
            text: 'Salvar'
            pos_hint: {'center_x': 0.5}
            on_release: app.save_book(book_name.text, book_author.text, book_pages.text)
    '''

class LoginScreen(MDScreen):
    pass

class HomeScreen(MDScreen):
    pass

class AddBookScreen(MDScreen):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.current_book_index = None
        self.selected_status = None
        return Builder.load_string(KV)
    
    def login(self, email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            token = user['idToken']
            self.load_books(user['localId'], token)
            self.root.get_screen('home').ids.user_email.text = f"Email: {user['email']}"
            self.root.current = 'home'
        except Exception as e:
            self.show_error_dialog(f"Login falhou: {e}")

    def register(self, email, password):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("Usuário registrado com sucesso!")
            self.root.current = 'home'
        except Exception as e:
            self.show_error_dialog(f"Registro falhou: {e}")
    
    def show_error_dialog(self, message):
        if not hasattr(self, 'error_dialog') or not self.error_dialog:
            self.error_dialog = MDDialog(
                title="Erro",
                text=message,
                size_hint=(0.8, 0.4),
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.close_error_dialog
                    )
                ]
            )
        self.error_dialog.text = message
        self.error_dialog.open()

    def close_error_dialog(self, instance):
        self.error_dialog.dismiss()

    def load_books(self, user_id, token):
        try:
            books = db.child("users").child(user_id).child("books").get(token)
            book_list = self.root.get_screen('home').ids.book_list
            book_list.clear_widgets()
            if books.each():
                for index, book in enumerate(books.each()):
                    book_item = OneLineListItem(text=book.val(), on_release=lambda x=index: self.show_add_book_screen(x))
                    book_list.add_widget(book_item)
        except Exception as e:
            print(f"Falha ao carregar livros: {e}")

    def change_password(self):
        user = auth.current_user
        if user:
            email = user['email']
            try:
                auth.send_password_reset_email(email)
                print(f"E-mail de redefinição de senha enviado para {email}")
            except Exception as e:
                print(f"Erro ao enviar e-mail de redefinição: {e}")
    
    def delete_account(self):
        user = auth.current_user
        if user:
            try:
                token = user['idToken']
                auth.delete_user_account(token)
                db.child("users").child(user['localId']).remove(token=token)
                print("Conta excluída com sucesso")
                self.root.current = 'login'
            except Exception as e:
                print(f"Erro ao excluir conta: {e}")
    
    def logout(self):
        auth.current_user = None
        print("Usuário deslogado")
        self.root.current = 'login'

    def show_add_book_screen(self, book_index=None):
        self.current_book_index = book_index
        if book_index is not None:
            if isinstance(book_index, int):
                book_list = self.root.get_screen('home').ids.book_list.children
                if 0 <= book_index < len(book_list):
                    book = book_list[len(book_list) - 1 - book_index]
                    book_data = book.text.split(" - ")
                    self.root.get_screen('add_book').ids.book_name.text = book_data[0]
                    self.root.get_screen('add_book').ids.book_author.text = book_data[1]
                    self.root.get_screen('add_book').ids.book_pages.text = book_data[2] if len(book_data) > 2 else ""
                    self.selected_status = book_data[3] if len(book_data) > 3 else None
                    self.root.get_screen('add_book').ids.book_status_button.text = self.selected_status or "Selecione o Status"
                else:
                    print(f"Índice {book_index} está fora do intervalo.")
            else:
                print(f"book_index não é um inteiro válido: {book_index}")
        else:
            self.root.get_screen('add_book').ids.book_name.text = ""
            self.root.get_screen('add_book').ids.book_author.text = ""
            self.root.get_screen('add_book').ids.book_pages.text = ""
            self.selected_status = None
            self.root.get_screen('add_book').ids.book_status_button.text = "Selecione o Status"
        self.root.current = 'add_book'

    def save_book(self, name, author, pages):
        user = auth.current_user
        if user and self.selected_status:
            try:
                token = user['idToken']
                book_data = f"{name} - {author} - {pages} páginas - {self.selected_status}"
                db.child("users").child(user['localId']).child("books").push(book_data, token=token)
                self.load_books(user['localId'], token)
                self.root.current = 'home'
            except Exception as e:
                print(f"Erro ao salvar livro: {e}")
        else:
            print("Preencha todos os campos")

    def cancel_book(self):
        self.clear_add_book_screen()
        self.root.current = 'home'

    def delete_book(self):
        if self.current_book_index is not None:
            self.root.get_screen('home').ids.book_list.remove_widget(
                self.root.get_screen('home').ids.book_list.children[self.current_book_index]
            )
            self.clear_add_book_screen()
            self.root.current = 'home'
            self.current_book_index = None

    def clear_add_book_screen(self):
        self.root.get_screen('add_book').ids.book_name.text = ""
        self.root.get_screen('add_book').ids.book_author.text = ""
        self.root.get_screen('add_book').ids.book_pages.text = ""
        self.selected_status = None
        self.root.get_screen('add_book').ids.book_status_button.text = "Selecione o Status"

    def open_status_menu(self):
        menu_items = [
            {"text": "Lido", "viewclass": "OneLineListItem", "on_release": lambda x="Lido": self.set_status(x)},
            {"text": "Não Lido", "viewclass": "OneLineListItem", "on_release": lambda x="Não Lido": self.set_status(x)},
            {"text": "Lendo", "viewclass": "OneLineListItem", "on_release": lambda x="Lendo": self.set_status(x)},
            {"text": "Abandonado", "viewclass": "OneLineListItem",
             "on_release": lambda x="Abandonado": self.set_status(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.get_screen('add_book').ids.book_status_button,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def set_status(self, status):
        self.selected_status = status
        self.root.get_screen('add_book').ids.book_status_button.text = status
        self.menu.dismiss()
    
    def search_books(self, search_text):
        book_list = self.root.get_screen('home').ids.book_list
        all_books = book_list.children[:]
        book_list.clear_widgets()
        if search_text == "":
            for book in reversed(all_books):
                book_list.add_widget(book)
        else:
            search_text = search_text.lower()
            for book in reversed(all_books):
                if search_text in book.text.lower():
                    book_list.add_widget(book)
    
    def create_pie_chart(self):
        user = auth.current_user
        if user:
            try:
                token = user['idToken']
                books = db.child("users").child(user['localId']).child("books").get(token)
                status_list = []
                if books.each():
                    for book in books.each():
                        status = book.val().split(" - ")[3]
                        status_list.append(status)
                status_df = pd.DataFrame(status_list, columns=['SITUAÇÃO'])
                contagem = status_df['SITUAÇÃO'].value_counts()
                plt.figure()
                plt.pie(contagem, autopct='%1.1f%%')
                plt.axis('equal')
                legenda = ['{}: {}'.format(situacao, valor) for situacao, valor in zip(contagem.index, contagem.values)]
                plt.legend(legenda, loc='center left', bbox_to_anchor=(0, 0))
                return FigureCanvasKivyAgg(plt.gcf())
            except Exception as e:
                print(f"Erro ao criar gráfico: {e}")

    def show_statistics(self):
        pie_chart = self.create_pie_chart()
        statistics_screen = self.root.get_screen('home').ids.statistics_box
        statistics_screen.add_widget(pie_chart)

    def switch_theme_style(self):
        self.theme_cls.primary_palette = (
            "Purple" if self.theme_cls.primary_palette == "Blue" else "Blue"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

if __name__ == '__main__':
    MainApp().run()

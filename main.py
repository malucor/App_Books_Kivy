from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
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

KV = '''
ScreenManager:
    HomeScreen:
    AddBookScreen:

<HomeScreen>:
    name: 'home'

    MDBottomNavigation:

        MDBottomNavigationItem:
            name: 'screen1'
            text: 'Home'
            icon: 'home'

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDLabel:
                    text: 'Livros Cadastrados'
                    halign: 'center'

                ScrollView:
                    MDList:
                        id: book_list

                MDRaisedButton:
                    text: '+ Adicionar Livro'
                    pos_hint: {'center_x': 0.5}
                    on_release: app.show_add_book_screen()

        MDBottomNavigationItem:
            name: 'screen2'
            text: 'Data'
            icon: 'chart-bar'

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDLabel:
                    text: 'Insights'
                    halign: 'center'
        
        MDBottomNavigationItem:
            name: 'screen3'
            text: 'Account'
            icon: 'account'

            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"
                padding: "20dp"

                MDLabel:
                    text: 'Perfil'
                    halign: 'center'

        MDBottomNavigationItem:
            name: 'screen4'
            text: 'Settings'
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
                        text: "Theme style - {}".format(app.theme_cls.theme_style)
                        halign: "center"
                        valign: "center"
                        bold: True
                        font_style: "H6"

                    MDRaisedButton:
                        text: "Set theme"
                        on_release: app.switch_theme_style()
                        pos_hint: {"center_x": .5}

<AddBookScreen>:
    name: 'add_book'

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
            on_release: app.save_book()
'''

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

    def show_add_book_screen(self, book_index=None):
        self.current_book_index = book_index
        if book_index is not None:
            book = self.root.get_screen('home').ids.book_list.children[book_index]
            book_data = book.text.split(" - ")
            self.root.get_screen('add_book').ids.book_name.text = book_data[0]
            self.root.get_screen('add_book').ids.book_author.text = book_data[1]
            self.selected_status = book_data[2] if len(book_data) > 2 else None
            self.root.get_screen('add_book').ids.book_status_button.text = self.selected_status or "Selecione o Status"
        else:
            self.root.get_screen('add_book').ids.book_name.text = ""
            self.root.get_screen('add_book').ids.book_author.text = ""
            self.root.get_screen('add_book').ids.book_pages.text = ""
            self.selected_status = None
            self.root.get_screen('add_book').ids.book_status_button.text = "Selecione o Status"
        self.root.current = 'add_book'

    def save_book(self):
        book_name = self.root.get_screen('add_book').ids.book_name.text
        book_author = self.root.get_screen('add_book').ids.book_author.text
        book_pages = self.root.get_screen('add_book').ids.book_pages.text

        if book_name and book_author and book_pages and self.selected_status:
            book_text = f"{book_name} - {book_author} - {self.selected_status}"
            if self.current_book_index is not None:
                # Atualizar livro existente
                book = self.root.get_screen('home').ids.book_list.children[self.current_book_index]
                book.text = book_text
            else:
                # Adicionar novo livro
                book_item = OneLineListItem(text=book_text, on_release=lambda x: self.show_add_book_screen(self.root.get_screen('home').ids.book_list.children.index(x)))
                self.root.get_screen('home').ids.book_list.add_widget(book_item)

            self.root.current = 'home'
            self.current_book_index = None

    def open_status_menu(self):
        menu_items = [
            {"text": "Lido", "viewclass": "OneLineListItem", "on_release": lambda x="Lido": self.set_status(x)},
            {"text": "Não Lido", "viewclass": "OneLineListItem", "on_release": lambda x="Não Lido": self.set_status(x)},
            {"text": "Lendo", "viewclass": "OneLineListItem", "on_release": lambda x="Lendo": self.set_status(x)},
            {"text": "Abandonado", "viewclass": "OneLineListItem", "on_release": lambda x="Abandonado": self.set_status(x)},
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

    def switch_theme_style(self):
        self.theme_cls.primary_palette = (
            "Purple" if self.theme_cls.primary_palette == "Blue" else "Blue"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

if __name__ == '__main__':
    MainApp().run()

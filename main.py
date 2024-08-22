from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.core.window import Window

Window.size = (360, 640)

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.bg_dark

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
                    text: 'Página Inicial'
                    halign: 'center'
                
                MDRaisedButton:
                    text: 'Clique Aqui'
                    pos_hint: {'center_x': 0.5}

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
                        font_style: "H6"  # ou outro estilo como "Body1", "Subtitle1"

                    MDRaisedButton:
                        text: "Set theme"
                        on_release: app.switch_theme_style()
                        pos_hint: {"center_x": .5}
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)
    
    def switch_theme_style(self):
        self.theme_cls.primary_palette = (
            "Orange" if self.theme_cls.primary_palette == "Red" else "Red"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

if __name__ == '__main__':
    MainApp().run()

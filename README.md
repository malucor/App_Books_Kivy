# App_Books_Kivy
- Aplicação no framework Kivy de Python para o usuário organizar e ter um controle das suas leituras. App desenvolvido durante a discplina de Projeto Interdisplinar em Sistema de Informação I, oferecida no curso de Sistema de Informação, no período 2024.1 da UFRPE.

- Nesse projeto, foi utilizado o Google Firebase commo ferramenta para autenticar os usuários e guardar os dados de cada na nuvem, de maneira que as informações não são perdidas ao fechar a aplicação e também garante a possibilidade do usuário fazer o login em outro dispositivo.

-------

## Configurando o Google Firebase
Com a sua conta Google, acesse o [Firebase](https://firebase.google.com/?hl=pt) e crie um novo projeto. Com ele criado, será necessário algumas informações para conseguir conectar o projeto ao firebase:

  `"apiKey": "API_KEY",` <br>
  `"authDomain": "DOMINIO.firebaseapp.com",` <br>
  `"databaseURL": "https://DOMINIO.firebaseio.com/",` <br>
  `"projectId": "PROJECT_ID",` <br>
  `"storageBucket": "BUCKET.appspot.com",` <br>
  `"messagingSenderId": "SENDER_ID",` <br>
  `"appId": "APP_ID",` <br>
  `"measurementId": "MEASUREMENT_ID"` <br>

No ambiente do códido, instale a biblioteca `pyrebase` através do comenado `pip install pyrebase4`

-------

## Bibliotecas Necessárias

- Pyrebase (`pip install pyrebase4`)
- Kivy (`pip install kivy`)
- KivyMD (`pip install kivymd`)

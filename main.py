from customtkinter import *
import subprocess
from login_db import *

class Login(CTk):
    def __init__(self):
        super().__init__()
        self.loginDB = LoginDB()
        self.layout_config() # Configura a janela principal

        self.label_titulo = CTkLabel(self, text="Escola XYZ:", font=('Arial', 30, 'bold'))
        self.label_titulo.pack(padx=10, pady=(50,30))

        self.label_username = CTkLabel(self, text="Usuário:")
        self.label_username.pack(padx=10, pady=5)

        self.entry_username = CTkEntry(self, width=220)
        self.entry_username.pack(padx=10, pady=5)

        self.label_password = CTkLabel(self, text="Senha:")
        self.label_password.pack(padx=10, pady=5)

        self.entry_password = CTkEntry(self, show="*", width=220)
        self.entry_password.pack(padx=10, pady=5)

        self.btn_login = CTkButton(self, text="Login", command=self.efetuar_login)
        self.btn_login.pack(padx=10, pady=20)

    def layout_config(self):
        self.title('Escola XYZ')
        self.geometry('300x520')
        self.resizable(width=False, height=False)

        set_appearance_mode('dark')
        set_default_color_theme('blue')

    def efetuar_login(self):
        usuario = self.entry_username.get()
        senha = self.entry_password.get()
        senhaHash = self.loginDB.create_pass(senha)
        dados_user = self.loginDB.ver_user(usuario)
        print(dados_user)
        userDB = dados_user[0][0]
        senhaDB = dados_user[0][1]
        print(dados_user)

        # Lógica de verificação de usuário e senha (simulação)
        if usuario == userDB and senhaHash == senhaDB:
            print("Login bem sucedido!")
            self.destroy()  # Fecha a janela de login
            # Se o login for bem sucedido, execute o arquivo dashboard.py
            subprocess.run(["python", "app.py"])  # Substitua "dashboard.py" pelo nome do seu arquivo

        else:
            print("Credenciais inválidas. Tente novamente.")

if __name__ == "__main__":
    app = Login()
    app.mainloop()
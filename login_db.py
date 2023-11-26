from hashlib import *
import sqlite3

class LoginDB:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def create_pass(self, password):
        self.password_user = sha256(password.encode()).hexdigest()
        return self.password_user 
    def create_user(self, username, passwaord):
        user = username
        password = self.create_pass(passwaord)
        self.cursor.execute('INSERT INTO user_login VALUES (?,?)',(user, password))
        print(f'Usuario:{user} com a senha: {password} Criado')
    def ver_user(self,nome):
        self.cursor.execute('SELECT * FROM user_login WHERE user = ?', (nome,))
        result = self.cursor.fetchall()
        return result
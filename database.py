import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    # Tabela Sistemas
    def criar_tabela(self):
        self.cursor.execute('CREATE TABLE sistemas (cod_sistema, nome_sistema)')
        self.conn.commit()

    def buscar_id(self, id):
        self.cursor.execute('SELECT cod_sistema FROM sistemas WHERE cod_sistema = ?', (id,))
        result = self.cursor.fetchone()
        return result

    def buscar_nome_sistema(self, nome):
        self.cursor.execute('SELECT nome_sistema FROM sistemas WHERE nome_sistema = ?', (nome,))
        result = self.cursor.fetchone()
        return result

    def criar_sistema(self, id, nome):
        self.cursor.execute('INSERT INTO sistemas VALUES (?,?)', (id, nome))
        self.conn.commit()

    def buscar_sistema_por_nome(self, nome):
        self.cursor.execute('SELECT * FROM sistemas WHERE nome_sistema = ?', (nome,))
        result = self.cursor.fetchone()
        return result

    def ver_sistemas(self):
        self.cursor.execute('SELECT cod_sistema, nome_sistema FROM sistemas')
        result = self.cursor.fetchall()
        return result

    def ver_sistema_por_id(self, id):
        self.cursor.execute('SELECT nome_sistema FROM sistemas WHERE cod_sistema = ?', (id,))
        result = self.cursor.fetchall()
        return result

    def editar_sistemas(self, new_name, new_cod, name):
        self.cursor.execute("UPDATE sistemas SET nome_sistema=?, cod_sistema=? WHERE nome_sistema=?",
                            (new_name, new_cod, name))
        self.conn.commit()

    def deletar_sistema(self, nome):
        self.cursor.execute("DELETE FROM sistemas WHERE nome_sistema=?", (nome,))
        self.conn.commit()

    def criar_perfil(self, sistema, nome, description):
        self.cursor.execute('INSERT INTO perfis VALUES (?,?,?)', (sistema, nome, description,))
        self.conn.commit()

    def ver_perfis(self):
        self.cursor.execute('SELECT id_sistema, nome_perfil, descricao_perfil FROM perfis')
        result = self.cursor.fetchall()
        return result

    def ver_perfis_por_sistema(self, id_sistema):
        self.cursor.execute('SELECT * FROM perfis WHERE id_sistema = ?', (id_sistema,))
        result = self.cursor.fetchall()
        return result

    def criar_matriz(self, sistema1, perfil1, sistema2, perfil2):
        self.cursor.execute('INSERT INTO matriz VALUES (?,?,?,?)', (sistema1, perfil1, sistema2, perfil2))
        self.conn.commit()

    def ver_matrizes(self):
        self.cursor.execute('SELECT id_sistema1, perfil1, id_sistema2, perfil2 FROM matriz')
        result = self.cursor.fetchall()
        return result

    def criar_usuario(self, sistema, perfil, nome, cpf):
        self.cursor.execute('INSERT INTO users VALUES (?,?,?,?)', (sistema, perfil, nome, cpf))
        self.conn.commit()
        print("usuario Cadastrado")

    def ver_usuarios(self):
        self.cursor.execute('SELECT id_sistema, perfil, nome, cpf FROM users')
        result = self.cursor.fetchall()
        return result

    def ver_usuario_por_cpf(self, cpf):
        self.cursor.execute('SELECT * FROM users WHERE cpf=?', (cpf,))
        result = self.cursor.fetchall()
        return result

    def ver_sistema_e_perfil_users(self, cpf):
        self.cursor.execute('SELECT id_sistema, perfil FROM users WHERE cpf = ?', (cpf,))
        result = self.cursor.fetchall()
        return result


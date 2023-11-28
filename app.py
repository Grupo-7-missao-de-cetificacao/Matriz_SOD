from customtkinter import *
from tkinter import messagebox, ttk, Toplevel
import random
from database import Database


# Classe principal da aplicação
class App(CTk):
    def __init__(self):
        super().__init__()
        self.systemsdb = Database()
        self.layout_config()  # Configura a janela principal
        self.frames = {}  # Dicionário para armazenar os quadros da aplicação
        self.menu_buttons = {}  # Dicionário para armazenar os botões do menu lateral
        self.menu_lateral()  # Cria o menu lateral
        self.frameAtivo = None  # Armazena o quadro ativo

        self.nome_entry = None
        self.codigo_entry = None

        self.matriz()  # Cria o quadro da seção "home"
        self.perfil()  # Cria o quadro da seção "perfil"
        self.sistema()  # Cria o quadro da seção "sistema"
        self.usuario()  # Cria o quadro da seção "usuário"
        self.sobre()  # Cria o quadro da seção "sobre"

        self.show_matriz_frame()  # Exibe o quadro "home" por padrão

        self.update_data_tableMatriz()  # Inicializar a tabela com dados existentes
        self.update_data_tablePerfil()  # Inicializar a tabela com dados existentes
        self.update_data_tableSistema()  # Inicializar a tabela com dados existentes
        self.update_data_tableUsuario()  # Inicializar a tabela com dados existentes
        self.dados_combo_sistemas()
        self.dados_combo_perfil()

    # Configurações da janela principal

    def layout_config(self):
        self.title('Escola XYZ')
        self.geometry('850x520')
        self.resizable(width=False, height=False)

        set_appearance_mode('dark')
        set_default_color_theme('blue')

        # Definir estilos personalizados para o Treeview
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        style.configure('Treeview', font=('Arial', 10))
        style.layout('Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

    # Cria o menu lateral
    def menu_lateral(self):
        frameMenu = CTkFrame(self, width=150, height=500, corner_radius=0)
        frameMenu.place(x=0, y=0)

        btn_nomes = ['matriz', 'perfil', 'sistema', 'usuario', 'sobre']

        for i, btn_nome in enumerate(btn_nomes):
            # Cria os botões do menu
            button = CTkButton(frameMenu, text=btn_nome.capitalize(), font=('Arial', 15, 'bold'),
                               fg_color='transparent', bg_color='transparent', corner_radius=0, width=150, height=50,
                               anchor='w', border_spacing=10,
                               command=lambda b=btn_nome: self.show_frame(b))
            button.place(x=0, y=i * 50)
            self.menu_buttons[btn_nome] = button

    # Mostra o quadro especificado
    def show_frame(self, frame_nome):
        btn_corAtiva = '#3498db'
        btn_corInativa = 'transparent'

        if self.frameAtivo:
            self.frameAtivo.place_forget()

        frame = self.frames[frame_nome]
        frame.place(x=160, y=0)
        self.frameAtivo = frame

        for button_name, button in self.menu_buttons.items():
            if button_name == frame_nome:
                button.configure(fg_color=btn_corAtiva)
            else:
                button.configure(fg_color=btn_corInativa)

    # Exibe o quadro "home"
    def show_matriz_frame(self):
        self.show_frame('matriz')

    # Exibe o quadro "perfil"
    def show_perfil_frame(self):
        self.show_frame('perfil')

    # Exibe o quadro "sistema"
    def show_sistema_frame(self):
        self.show_frame('sistema')

    # Exibe o quadro "usuário"
    def show_usuario_frame(self):
        self.show_frame('usuario')

    # Exibe o quadro "sobre"
    def show_sobre_frame(self):
        self.show_frame('sobre')

    # Gera um código aleatório e insere na entrada de texto
    def gerar_codigo(self):
        # Crie uma conexão com o banco de dados SQLite
        num = random.randint(1000, 9999)
        sistema_bd = self.systemsdb.buscar_id(num, )

        while sistema_bd is not None:
            print(f"O número {num} já existe no banco de dados.")
            num = random.randint(1000, 9999)
            sistema_bd = self.systemsdb.buscar_id(num, )
        print(f"O número {num} é único e será inserido no banco de dados.")

        self.entry_codigoSistema.delete(0, 'end')
        self.entry_codigoSistema.insert(0, str(num))

    # Cria o quadro da seção "sistema"
    def sistema(self):
        frameSistema = CTkFrame(
            self, fg_color='transparent', width=660, height=500, corner_radius=0)
        self.frames['sistema'] = frameSistema

        labelTitulo_frame = CTkLabel(
            frameSistema, text='S I S T E M A', font=('Arial', 20))
        labelTitulo_frame.place(x=10, y=10)

        label_nome = CTkLabel(frameSistema, text='Nome:')
        label_nome.place(x=10, y=60)
        self.entry_nomeSistema = CTkEntry(frameSistema, width=210)
        self.entry_nomeSistema.place(x=70, y=60)
        result = self.entry_nomeSistema.get()

        label_codigo = CTkLabel(frameSistema, text='Código:')
        label_codigo.place(x=10, y=100)
        self.entry_codigoSistema = CTkEntry(frameSistema, width=150)
        self.entry_codigoSistema.place(x=70, y=100)

        button_gerarCodigo = CTkButton(
            frameSistema, text='Gerar', width=50, command=self.gerar_codigo)
        button_gerarCodigo.place(x=230, y=100)

        button_criarSistema = CTkButton(
            frameSistema, text='Criar Cadastro', command=self.cadastrar_sistema)
        button_criarSistema.place(x=10, y=150)

        # Cria uma tabela para exibir dados
        self.data_tableSistema = ttk.Treeview(frameSistema, columns=(
            'Código', 'Nome', 'Ações'), show='headings')
        self.data_tableSistema.heading('#1', text='Código')
        self.data_tableSistema.heading('#2', text='Nome')
        self.data_tableSistema.column('#1', width=150)
        self.data_tableSistema.column('#2', width=300)

        # Remover a coluna de índice padrão
        self.data_tableSistema['show'] = 'headings'

        self.data_tableSistema.place(x=10, y=300)

        label_filtro = CTkLabel(frameSistema, text='Filtro:')
        label_filtro.place(x=10, y=250)

        # Adicione a entrada de texto e o botão de filtro
        self.filtroSistema_entry = CTkEntry(frameSistema, width=300)
        self.filtroSistema_entry.place(x=70, y=250)

        self.filtroSistema_entry.bind(
            '<KeyRelease>', self.filtrar_tabelaSistema)

    # Criar novo cadastro no banco de dados

    def cadastrar_sistema(self):
        sistemaNome = self.entry_nomeSistema.get().lower().replace(" ",
                                                                   "")  # Converte para letras minúsculas e elimina espaços
        sistemaCodigo = self.entry_codigoSistema.get()

        if sistemaNome and sistemaCodigo:
            # Verifique se o nome já existe no banco de dados
            nome_existente = self.systemsdb.buscar_nome_sistema(sistemaNome, )
            # Verifique se o código já existe no banco de dados
            codigo_existente = self.systemsdb.buscar_id(sistemaCodigo, )
            # Mensagem de erro padrão
            mensagem = 'Ocorreu algum erro. Tente novamente.'

            if nome_existente:
                mensagem = f'Nome "{sistemaNome}" já está em uso. Tente outro nome.'

            if codigo_existente:
                mensagem = f'Código "{sistemaCodigo}" já está em uso. Tente outro código.\n\n Se desejar, utilize o gerador automatico de código, clicando no botão "Gerar".'

            if nome_existente and codigo_existente:
                mensagem = f'Nome e código já estão em uso. Tente novamente.\n\n Se desejar, utilize o gerador automatico de código, clicando no botão "Gerar".'

            if not (nome_existente or codigo_existente):
                resposta = messagebox.askquestion(
                    'Confirmação', 'Confirmar o cadastro?')
                if resposta == 'yes':
                    # Inserir dados na tabela:
                    self.systemsdb.criar_sistema(sistemaCodigo, sistemaNome)

                    print(
                        f'Cadastro criado - Nome: {sistemaNome}, Código: {sistemaCodigo}')
                    self.entry_nomeSistema.delete(0, 'end')
                    self.entry_codigoSistema.delete(0, 'end')
                    self.entry_nomeSistema.focus_set()
                    # Atualizar a tabela quando uma nova entrada é criada
                    self.update_data_tableMatriz()
                    self.update_data_tablePerfil()
                    self.update_data_tableSistema()
                    self.update_data_tableUsuario()
                    self.update_combo_sistemas()
                    return

            # Exiba uma mensagem de erro com informações sobre as duplicatas
            messagebox.showerror("Erro", mensagem)
        else:
            print(Exception)
            print('Erro', 'Por favor, preencha todos os campos.')
            # Exibe um alerta de erro
            messagebox.showerror(
                'Erro', 'Por favor, preencha todos os campos.')

    # Cria o quadro da seção "perfil"
    def perfil(self):
        framePerfil = CTkFrame(self, fg_color='transparent',
                               width=660, height=500, corner_radius=0)
        self.frames['perfil'] = framePerfil

        labelTitulo_frame = CTkLabel(
            framePerfil, text='P E R F I L', font=('Arial', 20))
        labelTitulo_frame.place(x=10, y=10)

        label_nomeSistema = CTkLabel(framePerfil, text='Sistema:')
        label_nomeSistema.place(x=10, y=60)
        self.comboBox_nomeSistema_perfil = CTkComboBox(
            framePerfil, width=200)
        self.comboBox_nomeSistema_perfil.place(x=70, y=60)

        label_nome = CTkLabel(framePerfil, text='Nome:')
        label_nome.place(x=10, y=100)
        self.nomePerfil_entry = CTkEntry(framePerfil, width=200)
        self.nomePerfil_entry.place(x=70, y=100)

        label_descricao = CTkLabel(framePerfil, text='Descrição:')
        label_descricao.place(x=300, y=60)
        self.descricao_entry = CTkTextbox(framePerfil, width=280, height=70, fg_color='#343638', border_width=2,
                                          border_color='#565b5e')
        self.descricao_entry.place(x=380, y=60)

        criar_button = CTkButton(
            framePerfil, text='Criar Cadastro', command=self.cadastrar_perfil)
        criar_button.place(x=10, y=150)

        # Cria uma tabela para exibir dados
        self.data_tablePerfil = ttk.Treeview(framePerfil, columns=(
            'Código', 'Nome', 'Descrição', 'Ações'), show='headings')
        self.data_tablePerfil.heading('#1', text='Código')
        self.data_tablePerfil.heading('#2', text='Nome')
        self.data_tablePerfil.heading('#3', text='Descrição')

        self.data_tablePerfil.column('#1', width=100)
        self.data_tablePerfil.column('#2', width=100)
        self.data_tablePerfil.column('#3', minwidth=300)

        # Remover a coluna de índice padrão
        self.data_tablePerfil['show'] = 'headings'

        self.data_tablePerfil.place(x=10, y=300)

        label_filtro = CTkLabel(framePerfil, text='Filtro:')
        label_filtro.place(x=10, y=250)

        # Adicione a entrada de texto e o botão de filtro
        self.filtroPerfil_entry = CTkEntry(framePerfil, width=300)
        self.filtroPerfil_entry.place(x=70, y=250)

        self.filtroPerfil_entry.bind('<KeyRelease>', self.filtrar_tabelaPerfil)

    def cadastrar_perfil(self):
        try:
            sistema_escolhido = self.comboBox_nomeSistema_perfil.get()
            # verificar o nome no banco e buscar o codigo
            if sistema_escolhido:
                buscar_id = self.systemsdb.buscar_sistema_por_nome(
                    sistema_escolhido)
                id_sistema = buscar_id[0]
            nome_perfil = self.nomePerfil_entry.get().lower()
            description = self.descricao_entry.get("1.0", 'end-1c')
            resposta = messagebox.askquestion(
                'Confirmação', 'Confirmar o cadastro?')
            if resposta == 'yes':
                # Inserir dados na tabela:
                self.systemsdb.criar_perfil(
                    id_sistema, nome_perfil, description)

                print(
                    f'Cadastro criado - Sistema: {sistema_escolhido}, Nome Perfil: {nome_perfil}, Descrição: {description}')
                self.nomePerfil_entry.delete(0, 'end')
                self.descricao_entry.delete('1.0', 'end')
                self.nomePerfil_entry.focus_set()
                # Atualizar a tabela quando uma nova entrada é criada
                self.update_data_tableMatriz()
                self.update_data_tablePerfil()
                self.update_data_tableSistema()
                self.update_data_tableUsuario()
                self.update_combo_perfil()
                return

        except Exception as e:
            print(e)

    def criar_matriz(self):
        # entrada dos dados
        sistema1 = self.comboBox_nomeSistema_matriz.get()
        perfil1 = self.comboBox_perfil_matriz.get()
        sistema2 = self.comboBox_nomeSistema_matriz2.get()
        perfil2 = self.comboBox_perfil_matriz2.get()

        def buscar_ids(nome_sistema):
            verificar_id = self.systemsdb.buscar_sistema_por_nome(nome_sistema)
            id_sistema = verificar_id[0]
            return id_sistema

        # criação de tupla para verificação
        id_sistema1 = buscar_ids(sistema1)
        id_sistema2 = buscar_ids(sistema2)
        tupla_dados = (id_sistema1, perfil1, id_sistema2, perfil2)
        dados_banco = self.systemsdb.ver_matrizes()
        # verificações
        if perfil1 == perfil2:
            raise Exception('Os perfis não podem ser iguais')

        for dados in dados_banco:
            if dados == tupla_dados:
                raise Exception('Matriz já está cadastrada')

        resposta = messagebox.askquestion(
            'Confirmação', 'Confirmar o cadastro?')
        if resposta == 'yes':
            # Inserir dados na tabela:
            self.systemsdb.criar_matriz(
                id_sistema1, perfil1, id_sistema2, perfil2)
            print(
                f'matriz cadastrada - Sistema1: {id_sistema1}, Nome Perfil: {perfil1}, Sistema2: {id_sistema2}, Perfil2: {perfil2}')
            # Atualizar a tabela quando uma nova entrada é criada
            self.update_data_tableMatriz()
            self.update_data_tablePerfil()
            self.update_data_tableSistema()
            self.update_data_tableUsuario()

    # Cria o quadro da seção "home"
    def matriz(self):
        frameMatriz = CTkFrame(self, fg_color='transparent',
                               width=660, height=500, corner_radius=0)
        self.frames['matriz'] = frameMatriz

        labelTitulo_frame = CTkLabel(
            frameMatriz, text='M A T R I Z   S O D', font=('Arial', 20))
        labelTitulo_frame.place(x=10, y=10)

        label_nomeSistema = CTkLabel(frameMatriz, text='Sistema:')
        label_nomeSistema.place(x=10, y=60)
        self.comboBox_nomeSistema_matriz = CTkComboBox(
            frameMatriz, width=200)
        self.comboBox_nomeSistema_matriz.place(x=120, y=60)

        label_nomePerfil = CTkLabel(frameMatriz, text='Perfil:')
        label_nomePerfil.place(x=10, y=100)
        self.comboBox_perfil_matriz = CTkComboBox(
            frameMatriz, width=200)
        self.comboBox_perfil_matriz.place(x=120, y=100)

        label_linha = CTkLabel(frameMatriz, text='_' *
                               55, text_color='#565b5e')
        label_linha.place(x=10, y=145)

        label_nome = CTkLabel(frameMatriz, text='Sistema Conflito:')
        label_nome.place(x=10, y=200)
        self.comboBox_nomeSistema_matriz2 = CTkComboBox(
            frameMatriz, width=200)
        self.comboBox_nomeSistema_matriz2.place(x=120, y=200)

        label_cpf = CTkLabel(frameMatriz, text='Perfil Conflito:')
        label_cpf.place(x=10, y=240)
        self.comboBox_perfil_matriz2 = CTkComboBox(
            frameMatriz, width=200)
        self.comboBox_perfil_matriz2.place(x=120, y=240)

        criar_button = CTkButton(
            frameMatriz, text='Criar Cadastro', command=self.criar_matriz)
        criar_button.place(x=10, y=300)

        # Cria uma tabela para exibir dados
        self.data_tableMatriz = ttk.Treeview(frameMatriz, columns=(
            'Código 1', 'Perfil 1', 'Código 2', 'Perfil 2'), show='headings')
        self.data_tableMatriz.heading('#1', text='Sistema 1')
        self.data_tableMatriz.heading('#2', text='Perfil 1')
        self.data_tableMatriz.heading('#3', text='Sistema 2')
        self.data_tableMatriz.heading('#4', text='Perfil 2')
        # Definir a altura (height)
        self.data_tableMatriz["height"] = 18

        self.data_tableMatriz.column('#1', width=55)
        self.data_tableMatriz.column('#2', width=100)
        self.data_tableMatriz.column('#3', width=55)
        self.data_tableMatriz.column('#4', width=100)

        # Remover a coluna de índice padrão
        self.data_tableMatriz['show'] = 'headings'

        self.data_tableMatriz.place(x=360, y=110)

        filtroMatriz_label = CTkLabel(frameMatriz, text='Filtro:')
        filtroMatriz_label.place(x=360, y=60)

        # Adicione a entrada de texto e o botão de filtro
        self.filtroMatriz_entry = CTkEntry(frameMatriz, width=240)
        self.filtroMatriz_entry.place(x=420, y=60)

        self.filtroMatriz_entry.bind('<KeyRelease>', self.filtrar_tabelaMatriz)

    # Cria o quadro da seção "usuário"
    def usuario(self):
        frameUsuario = CTkFrame(
            self, fg_color='transparent', width=750, height=500, corner_radius=0)
        self.frames['usuario'] = frameUsuario

        labelTitulo_frame = CTkLabel(
            frameUsuario, text='U S U Á R I O', font=('Arial', 20))
        labelTitulo_frame.place(x=10, y=10)

        label_nomeSistema = CTkLabel(frameUsuario, text='Sistema:')
        label_nomeSistema.place(x=10, y=60)
        self.comboBox_nomeSistema_usuario = CTkComboBox(
            frameUsuario, width=200)
        self.comboBox_nomeSistema_usuario.place(x=70, y=60)

        label_nomePerfil = CTkLabel(frameUsuario, text='Perfil:')
        label_nomePerfil.place(x=10, y=100)
        self.comboBox_perfil_usuario = CTkComboBox(
            frameUsuario, width=200)
        self.comboBox_perfil_usuario.place(x=70, y=100)

        label_nome = CTkLabel(frameUsuario, text='Nome:')
        label_nome.place(x=300, y=60)
        self.entry_nomeUsuario = CTkEntry(frameUsuario, width=200)
        self.entry_nomeUsuario.place(x=360, y=60)

        label_cpf = CTkLabel(frameUsuario, text='CPF:')
        label_cpf.place(x=300, y=100)
        self.entry_cpf = CTkEntry(frameUsuario, width=200)
        self.entry_cpf.place(x=360, y=100)

        criar_button = CTkButton(
            frameUsuario, text='Criar Usuário', command=self.criar_usuario)
        criar_button.place(x=10, y=150)

        # Cria uma tabela para exibir dados
        self.data_tableUsuario = ttk.Treeview(
            frameUsuario, columns=('Código', 'Perfil', 'Nome', 'CPF', 'Ações'), show='headings')
        self.data_tableUsuario.heading('#1', text='Código')
        self.data_tableUsuario.heading('#2', text='Perfil')
        self.data_tableUsuario.heading('#3', text='Nome')
        self.data_tableUsuario.heading('#4', text='CPF')

        self.data_tableUsuario.column('#1', width=100)
        self.data_tableUsuario.column('#2', width=100)
        self.data_tableUsuario.column('#3', width=100)
        self.data_tableUsuario.column('#4', width=100)

        # Remover a coluna de índice padrão
        self.data_tableUsuario['show'] = 'headings'

        self.data_tableUsuario.place(x=10, y=300)

        label_filtroUser = CTkLabel(frameUsuario, text='Filtro:')
        label_filtroUser.place(x=10, y=250)

        # Adicione a entrada de texto e o botão de filtro
        self.filtroUsuario_entry = CTkEntry(frameUsuario, width=300)
        self.filtroUsuario_entry.place(x=70, y=250)

        self.filtroUsuario_entry.bind(
            '<KeyRelease>', self.filtrar_tabelaUsuario)

    def criar_usuario(self):
        sistema_escolhido1 = self.comboBox_nomeSistema_usuario.get()
        # verificar o nome no banco e buscar o codigo
        if sistema_escolhido1:
            buscar_id = self.systemsdb.buscar_sistema_por_nome(
                sistema_escolhido1)
            id_sistema = buscar_id[0]

        perfil_escolhido = self.comboBox_perfil_usuario.get()
        nome_user = self.entry_nomeUsuario.get().lower()
        cpf = self.entry_cpf.get()
        dados_user = self.systemsdb.ver_sistema_e_perfil_users(cpf, )
        dados_usuario = dados_user
        usuarios = self.systemsdb.ver_usuario_por_cpf(cpf, )
        if usuarios:
            dados_tupla = (
                dados_usuario[0][0], dados_usuario[0][1], id_sistema, perfil_escolhido)
            dados_banco = self.systemsdb.ver_matrizes()
            for dados in dados_banco:
                print(dados)
                print(dados_tupla)
                if dados == dados_tupla:
                    nome_sistema = self.systemsdb.ver_sistema_por_id(
                        dados_banco[0][0])
                    print(nome_user[0].upper())
                    print(nome_user[1:])
                    mensagem = f"{nome_user[0].upper() + nome_user[1:]}, não pode ser cadastrado ao {sistema_escolhido1} com o perfil de usuario {perfil_escolhido}, pois o mesmo já está cadastrado com  os seguintes dados \n\nSISTEMA: {nome_sistema[0][0]}\nPERFIL: {dados_banco[0][1]}\n\nO acesso pode gerar um conflito de interesse então não podera ser cadastrado para este perfil"
                    resposta = messagebox.showerror("CONFLITO", mensagem)
                    raise Exception('erro')
        resposta = messagebox.askquestion(
            'Confirmação', 'Confirmar o cadastro?')
        if resposta == 'yes':
            self.systemsdb.criar_usuario(
                id_sistema, perfil_escolhido, nome_user, cpf)
            print(
                f'Usuario Cadastrado - Nome: {nome_user}, CPF: {cpf}, Nome Perfil: {perfil_escolhido}, Sistema: {id_sistema}')
            self.entry_nomeUsuario.delete(0, 'end')
            self.entry_cpf.delete(0, 'end')
            self.entry_nomeUsuario.focus_set()
            # Atualizar a tabela quando uma nova entrada é criada
            self.update_data_tableMatriz()
            self.update_data_tablePerfil()
            self.update_data_tableSistema()
            self.update_data_tableUsuario()

    # Cria o quadro da seção "sobre"
    def sobre(self):
        frameSobre = CTkFrame(self, fg_color='transparent',
                              width=660, height=500, corner_radius=0)
        self.frames['sobre'] = frameSobre

        labelTitulo_frame = CTkLabel(
            frameSobre, text='S O B R E', font=('Arial', 20))
        labelTitulo_frame.place(x=10, y=10)

        label_subTitulo = CTkLabel(
            frameSobre, text='informações do Projeto:', font=('Arial', 18))
        label_subTitulo.place(x=10, y=60)

        label_textoSimples = CTkLabel(frameSobre, text='Curso:')
        label_textoSimples.place(x=10, y=100)
        label_textoSimples = CTkLabel(
            frameSobre, text='Desenvolvimento Full Stack')
        label_textoSimples.place(x=80, y=100)

        label_textoSimples = CTkLabel(frameSobre, text='Semestre:')
        label_textoSimples.place(x=10, y=125)
        label_textoSimples = CTkLabel(frameSobre, text='2023.3')
        label_textoSimples.place(x=80, y=125)

        label_textoSimples = CTkLabel(frameSobre, text='Objetivo:')
        label_textoSimples.place(x=10, y=150)
        label_textoSimples = CTkLabel(frameSobre, text='Missão Certificação')
        label_textoSimples.place(x=80, y=150)

        label_textoSimples = CTkLabel(frameSobre, text='Disciplina:')
        label_textoSimples.place(x=10, y=175)
        label_textoSimples = CTkLabel(
            frameSobre, text='Projetando uma Aplicação Desktop')
        label_textoSimples.place(x=80, y=175)

        label_textoSimples = CTkLabel(frameSobre, text='Professor:')
        label_textoSimples.place(x=10, y=200)
        label_textoSimples = CTkLabel(
            frameSobre, text='Andre Luiz Avelino Sobral')
        label_textoSimples.place(x=80, y=200)

        label_subTitulo = CTkLabel(
            frameSobre, text='Equipe:', font=('Arial', 18))
        label_subTitulo.place(x=10, y=250)

        label_textoSimples = CTkLabel(frameSobre, text='Nome:')
        label_textoSimples.place(x=10, y=300)
        label_textoSimples = CTkLabel(
            frameSobre, text='Cristian Viery Guimarães Souza')
        label_textoSimples.place(x=80, y=300)
        label_textoSimples = CTkLabel(frameSobre, text='Matricula:')
        label_textoSimples.place(x=10, y=320)
        label_textoSimples = CTkLabel(frameSobre, text='202307134406')
        label_textoSimples.place(x=80, y=320)

        label_textoSimples = CTkLabel(frameSobre, text='Nome:')
        label_textoSimples.place(x=10, y=350)
        label_textoSimples = CTkLabel(
            frameSobre, text='Douglas Camilo Peres Navas')
        label_textoSimples.place(x=80, y=350)
        label_textoSimples = CTkLabel(frameSobre, text='Matricula:')
        label_textoSimples.place(x=10, y=370)
        label_textoSimples = CTkLabel(frameSobre, text='202308577794')
        label_textoSimples.place(x=80, y=370)

        label_textoSimples = CTkLabel(frameSobre, text='Nome:')
        label_textoSimples.place(x=10, y=400)
        label_textoSimples = CTkLabel(frameSobre, text='Fellype Pinto Coelho')
        label_textoSimples.place(x=80, y=400)
        label_textoSimples = CTkLabel(frameSobre, text='Matricula:')
        label_textoSimples.place(x=10, y=420)
        label_textoSimples = CTkLabel(frameSobre, text='202307137588')
        label_textoSimples.place(x=80, y=420)

        label_textoSimples = CTkLabel(frameSobre, text='Nome:')
        label_textoSimples.place(x=300, y=300)
        label_textoSimples = CTkLabel(
            frameSobre, text='Giovanna Alves Miranda Cunha')
        label_textoSimples.place(x=370, y=300)
        label_textoSimples = CTkLabel(frameSobre, text='Matricula:')
        label_textoSimples.place(x=300, y=320)
        label_textoSimples = CTkLabel(frameSobre, text='202307107701')
        label_textoSimples.place(x=370, y=320)

        label_textoSimples = CTkLabel(frameSobre, text='Nome:')
        label_textoSimples.place(x=300, y=350)
        label_textoSimples = CTkLabel(frameSobre, text='Leandro Rodrigues')
        label_textoSimples.place(x=370, y=350)
        label_textoSimples = CTkLabel(frameSobre, text='Matricula:')
        label_textoSimples.place(x=300, y=370)
        label_textoSimples = CTkLabel(frameSobre, text='202307184641')
        label_textoSimples.place(x=370, y=370)

        label_textoSimples = CTkLabel(frameSobre, text='Nome:')
        label_textoSimples.place(x=300, y=400)
        label_textoSimples = CTkLabel(frameSobre, text='Silas Barbosa Camelo')
        label_textoSimples.place(x=370, y=400)
        label_textoSimples = CTkLabel(frameSobre, text='Matricula:')
        label_textoSimples.place(x=300, y=420)
        label_textoSimples = CTkLabel(frameSobre, text='202307521027')
        label_textoSimples.place(x=370, y=420)

    # Adicione um método para atualizar a tabela com dados do banco de dados
    def update_data_tableSistema(self):
        # Limpar dados existentes na tabela
        for item in self.data_tableSistema.get_children():
            self.data_tableSistema.delete(item)

        # Buscar dados do banco de dados e preencher a tabela
        data = self.systemsdb.ver_sistemas()

        for coluna in data:
            self.data_tableSistema.insert(
                '', 'end', values=(coluna[0], coluna[1]))

    def update_data_tablePerfil(self):
        # Limpar dados existentes na tabela
        for item in self.data_tablePerfil.get_children():
            self.data_tablePerfil.delete(item)

        # Buscar dados do banco de dados e preencher a tabela
        data = self.systemsdb.ver_perfis()

        for coluna in data:
            id_sistema = coluna[0]
            nomeSistemaDb = self.systemsdb.ver_sistema_por_id(id_sistema)
            self.data_tablePerfil.insert('', 'end', values=(
                nomeSistemaDb, coluna[1], coluna[2]))

    def update_data_tableMatriz(self):
        # Limpar dados existentes na tabela
        for item in self.data_tableMatriz.get_children():
            self.data_tableMatriz.delete(item)

        # Buscar dados do banco de dados e preencher a tabela
        data = self.systemsdb.ver_matrizes()

        for coluna in data:
            id_sistema1 = coluna[0]
            id_sistema2 = coluna[2]
            nomeSistema1Db = self.systemsdb.ver_sistema_por_id(id_sistema1)
            nomeSistema2Db = self.systemsdb.ver_sistema_por_id(id_sistema2)
            self.data_tableMatriz.insert('', 'end', values=(
                nomeSistema1Db, coluna[1], nomeSistema2Db, coluna[3]))

    def update_data_tableUsuario(self):
        # Limpar dados existentes na tabela
        for item in self.data_tableUsuario.get_children():
            self.data_tableUsuario.delete(item)

        # Buscar dados do banco de dados e preencher a tabela
        data = self.systemsdb.ver_usuarios()

        for coluna in data:
            id_sistema = coluna[0]
            nomeSistemaDb = self.systemsdb.ver_sistema_por_id(id_sistema)
            self.data_tableUsuario.insert('', 'end', values=(
                nomeSistemaDb, coluna[1], coluna[2], coluna[3]))

    # Função para filtrar a tabela com base no critério de pesquisa
    def filtrar_tabelaSistema(self, event):
        criterio = self.filtroSistema_entry.get().lower().replace(" ", "")

        for item in self.data_tableSistema.get_children():
            self.data_tableSistema.delete(item)

        data = self.systemsdb.ver_sistemas()
        for coluna in data:
            if criterio in coluna[0].lower() or criterio in coluna[1].lower():
                self.data_tableSistema.insert(
                    '', 'end', values=(coluna[0], coluna[1]))

    def filtrar_tabelaPerfil(self, event):
        criterio = self.filtroPerfil_entry.get().lower().replace(" ", "")

        for item in self.data_tablePerfil.get_children():
            self.data_tablePerfil.delete(item)

        data = self.systemsdb.ver_perfis()
        for coluna in data:
            if criterio in coluna[0].lower() or criterio in coluna[1].lower() or criterio in coluna[2].lower():
                self.data_tablePerfil.insert(
                    '', 'end', values=(coluna[0], coluna[1], coluna[2]))

    def filtrar_tabelaUsuario(self, event):
        criterio = self.filtroUsuario_entry.get().lower().replace(" ", "")

        for item in self.data_tableUsuario.get_children():
            self.data_tableUsuario.delete(item)

        data = self.systemsdb.ver_usuarios()
        for coluna in data:
            if criterio in coluna[0].lower() or criterio in coluna[1].lower() or criterio in coluna[2].lower() or criterio in coluna[3].lower():
                self.data_tableUsuario.insert('', 'end', values=(
                    coluna[0], coluna[1], coluna[2], coluna[3]))

    def filtrar_tabelaMatriz(self, event):
        criterio = self.filtroMatriz_entry.get().lower().replace(" ", "")

        for item in self.data_tableMatriz.get_children():
            self.data_tableMatriz.delete(item)

        data = self.systemsdb.ver_matrizes()
        for coluna in data:
            if criterio in coluna[0].lower() or criterio in coluna[1].lower() or criterio in coluna[2].lower() or criterio in coluna[3].lower():
                self.data_tableMatriz.insert('', 'end', values=(
                    coluna[0], coluna[1], coluna[2], coluna[3]))

    def dados_combo_sistemas(self):
        dados_sistema = self.systemsdb.ver_sistemas()
        combo_sistema_values = []
        for dados in dados_sistema:
            combo_sistema_values.append(dados[1])
        self.comboBox_nomeSistema_perfil.set("Sistemas:")
        self.comboBox_nomeSistema_perfil.configure(values=combo_sistema_values)
        self.comboBox_nomeSistema_matriz.set('Sistemas:')
        self.comboBox_nomeSistema_matriz.configure(values=combo_sistema_values)
        self.comboBox_nomeSistema_matriz2.set('Sistema Conflito:')
        self.comboBox_nomeSistema_matriz2.configure(
            values=combo_sistema_values)
        self.comboBox_nomeSistema_usuario.set('Sistemas:')
        self.comboBox_nomeSistema_usuario.configure(
            values=combo_sistema_values)

    def update_combo_sistemas(self):
        dados_sistema = self.systemsdb.ver_sistemas()
        combo_sistema_values = []
        for dados in dados_sistema:
            combo_sistema_values.append(dados[1])
        self.comboBox_nomeSistema_perfil.configure(values=combo_sistema_values)
        self.comboBox_nomeSistema_matriz.configure(values=combo_sistema_values)
        self.comboBox_nomeSistema_matriz2.configure(
            values=combo_sistema_values)
        self.comboBox_nomeSistema_usuario.configure(
            values=combo_sistema_values)

    def dados_combo_perfil(self):
        dados_perfil_db = self.systemsdb.ver_perfis()
        dados_combo_perfil = []
        for dados in dados_perfil_db:
            dados_combo_perfil.append(dados[1])
        self.comboBox_perfil_matriz.set("Perfil:")
        self.comboBox_perfil_matriz.configure(values=dados_combo_perfil)
        self.comboBox_perfil_matriz2.set("Perfil Conflito")
        self.comboBox_perfil_matriz2.configure(values=dados_combo_perfil)
        self.comboBox_perfil_usuario.set('Perfil:')
        self.comboBox_perfil_usuario.configure(values=dados_combo_perfil)

    def update_combo_perfil(self):
        dados_perfil_db = self.systemsdb.ver_perfis()
        dados_combo_perfil = []
        for dados in dados_perfil_db:
            dados_combo_perfil.append(dados[1])
        self.comboBox_perfil_matriz.configure(values=dados_combo_perfil)
        self.comboBox_perfil_matriz2.configure(values=dados_combo_perfil)
        self.comboBox_perfil_usuario.configure(values=dados_combo_perfil)


# Executa a aplicação
if __name__ == '__main__':
    app = App()
    app.mainloop()

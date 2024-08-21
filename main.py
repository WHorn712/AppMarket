import datetime
import tkinter as tk
from tkinter import messagebox
import pyodbc
from PIL import Image, ImageTk



def convert_for_phone_number(number):
    new_number = ""
    for i in number:
        if i != "(" and i != ")" and i != " " and i != "-":
            new_number += i
    two_firts = number[1:3]
    number_aux = new_number[2:]
    number2 = two_firts + " " + number_aux
    return number2



def conectar_banco_de_dados():
    try:
        server = 'DESKTOP-VDQPO57\SQLEXPRESS'
        database = 'AppMercado'
        username = 'sa'
        password = 'Sunwar17tzu!234'
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        connection = connection_string
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        return None

conn = conectar_banco_de_dados()

def buscar_usuario_por_nome(username):
    try:
        conn = conectar_banco_de_dados()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute("SELECT * FROM Usuarios WHERE Username = ?", (username,))

        # Buscar o resultado
        usuario = cursor.fetchone()

        # Fechar a conexão
        cursor.close()
        conn.close()

        # Verificar se o usuário foi encontrado
        if usuario == None:
            return False
        else:
            return usuario.Senha
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None


# Função para formatar o CPF
def format_cpf(event):
    text = cpf_entry.get().replace(".", "").replace("-", "")
    new_text = ""

    if event.keysym == "BackSpace":
        return

    if len(text) > 11:
        text = text[:11]

    for i in range(len(text)):
        if not text[i].isdigit():
            continue
        if i in [2, 5]:
            new_text += text[i] + "."
        elif i == 8:
            new_text += text[i] + "-"
        else:
            new_text += text[i]

    cpf_entry.delete(0, tk.END)
    cpf_entry.insert(0, new_text)

# Função para formatar a data de nascimento
def format_date(event):
    text = dob_entry.get().replace("/", "")
    new_text = ""

    if event.keysym == "BackSpace":
        return

    # Limitar a quantidade de dígitos a 8
    if len(text) > 8:
        text = text[:8]

    for i in range(len(text)):
        if not text[i].isdigit():
            continue
        if i in [1, 3]:
            new_text += text[i] + "/"
        else:
            new_text += text[i]

    dob_entry.delete(0, tk.END)
    dob_entry.insert(0, new_text)

# Função para formatar o número de celular
def format_phone(event):
    text = phone_entry.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
    new_text = ""

    if event.keysym == "BackSpace":
        return

    if len(text) > 11:
        text = text[:11]

    for i in range(len(text)):
        if not text[i].isdigit():
            continue
        if i == 0:
            new_text += "(" + text[i]
        elif i == 1:
            new_text += text[i] + ") "
        elif i == 2:
            new_text += text[i] + " "
        elif i == 6:
            new_text += text[i] + "-"
        else:
            new_text += text[i]

    phone_entry.delete(0, tk.END)
    phone_entry.insert(0, new_text)

# Função para formatar a sigla do estado
def format_state(event):
    text = state_entry.get().upper()
    new_text = ""

    if event.keysym == "BackSpace":
        return

    if len(text) > 2:
        text = text[:2]

    for i in range(len(text)):
        if not text[i].isalpha():
            continue
        new_text += text[i]

    state_entry.delete(0, tk.END)
    state_entry.insert(0, new_text)

# Função para validar a entrada do número da rua
def validate_number_input(event):
    text = street_number_entry.get()
    if not text.isdigit():
        street_number_entry.delete(0, tk.END)
        street_number_entry.insert(0, ''.join(filter(str.isdigit, text)))

username_entry_for_db = ""
email_entry_for_db = ""
city_entry_for_db = ""
street_entry_for_db = ""
complement_entry_for_db = ""


def convert_string_for_date(data):
    dia = int(data[0:2])
    mes = int(data[3:5])
    ano = int(data[6:10])
    date = datetime.datetime(day=dia, month=mes, year=ano)
    return date.strftime('%Y-%m-%d %H:%M:%S')

# Função para inserir dados no banco de dados
def insert_data(dados):
    conn = conectar_banco_de_dados()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Usuarios (NomeCompleto, Username, Senha, CPF, DataNascimento, Email, NumeroCelular, Cidade, 
        Estado, Rua, Numero, Complemento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
    dados.get("nome completo"),
    dados.get("user"),
    dados.get("senha"),
    dados.get("cpf"),
    dados.get("data de nascimento"),
    dados.get("email"),
    dados.get("número de telefone"),
    dados.get("cidade"),
    dados.get("estado"),
    dados.get("rua"),
    dados.get("numero do endereço"),
    dados.get("complemento")
    ))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")

def open_account_adress(caw, dados):
    caw.withdraw()

    new_windown_adress = tk.Toplevel(caw)
    new_windown_adress.title("Cadastrar Endereço")
    new_windown_adress.geometry("400x600")
    new_windown_adress.configure(bg='#457b9d')

    def back_to_caw():
        new_windown_adress.destroy()
        caw.deiconify()

    def cadastrar():
        dados_aux = {"cidade": city_entry.get(),
                     "estado": state_entry.get(),
                     "rua": street_entry.get(),
                     "numero do endereço": street_number_entry.get(),
                     "complemento": complement_entry.get()}
        dados.update(dados_aux)
        resultado = validar_dados_endereco(dados)
        validacao = resultado[0]
        informacao = resultado[1]
        if validacao == False:
            aviso_cadastro2.configure(fg='red')
            aviso_cadastro2.configure(text=informacao)
            aviso_cadastro2.grid(columnspan=2, sticky='e')
        else:
            aviso_cadastro2.configure(fg='#457b9d')
            dados.pop("senha2")
            data = dados.get("data de nascimento")
            date = convert_string_for_date(data)
            num_adress = int(dados.get("numero do endereço"))
            telefone = convert_for_phone_number(dados.get("número de telefone"))
            news_dados = {"data de nascimento": date,
                          "numero do endereço": num_adress,
                          "número de telefone": telefone}
            dados.pop("data de nascimento")
            dados.pop("numero do endereço")
            dados.pop("número de telefone")
            dados.update(news_dados)
            insert_data(dados)



    # Label para Endereço
    phone_label = tk.Label(new_windown_adress, text="ENDEREÇO:", font=label_font, bg='#457b9d', fg='white')
    phone_label.grid(row=0, column=0, padx=0, pady=9, columnspan=2)

    # Label e Entry para Cidade
    city_label = tk.Label(new_windown_adress, text="Cidade:", font=label_font, bg='#457b9d', fg='white')
    city_label.grid(row=1, column=0, padx=10, pady=9, sticky='e')
    city_entry = tk.Entry(new_windown_adress, font=entry_font, width=22)
    city_entry.grid(row=1, column=1, padx=10, pady=9)
    city_entry_for_db = city_entry

    # Label e Entry para Sigla do Estado
    state_label = tk.Label(new_windown_adress, text="Estado:", font=label_font, bg='#457b9d', fg='white')
    state_label.grid(row=2, column=0, padx=10, pady=9, sticky='e')
    global state_entry
    state_entry = tk.Entry(new_windown_adress, font=entry_font, width=5)
    state_entry.grid(row=2, column=1, padx=10, pady=9, sticky='w')
    state_entry.bind("<KeyRelease>", format_state)

    # Label e Entry para Rua
    street_label = tk.Label(new_windown_adress, text="Rua:", font=label_font, bg='#457b9d', fg='white')
    street_label.grid(row=3, column=0, padx=10, pady=9, sticky='e')
    street_entry = tk.Entry(new_windown_adress, font=entry_font, width=22)
    street_entry.grid(row=3, column=1, padx=10, pady=9)
    street_entry_for_db = street_entry

    # Label e Entry para Número da Rua
    street_number_label = tk.Label(new_windown_adress, text="Número:", font=label_font, bg='#457b9d', fg='white')
    street_number_label.grid(row=4, column=0, padx=10, pady=9, sticky='e')
    global street_number_entry
    street_number_entry = tk.Entry(new_windown_adress, font=entry_font, width=10)
    street_number_entry.grid(row=4, column=1, padx=10, pady=9, sticky='w')
    street_number_entry.bind("<KeyRelease>", validate_number_input)

    # Label e Entry para Complemento
    complement_label = tk.Label(new_windown_adress, text="Complemento:", font=label_font, bg='#457b9d',
                                    fg='white')
    complement_label.grid(row=5, column=0, padx=10, pady=9, sticky='e')
    complement_entry = tk.Entry(new_windown_adress, font=entry_font, width=22)
    complement_entry.grid(row=5, column=1, padx=10, pady=9)
    complement_entry_for_db = complement_entry

    # Aviso caso o conta não seja encontrado
    aviso_cadastro2 = tk.Label(new_windown_adress, text="asdasd", font=label_font, bg='#457b9d',
                                  fg='#457b9d')
    aviso_cadastro2.grid(row=6, column=0, columnspan=2)

    # Botão de cadastrar
    back_button = tk.Button(new_windown_adress, text="Cadastrar", font=button_font, command=cadastrar,
                            bg='#455874',
                            fg='white')
    back_button.grid(row=7, column=0, pady=0, padx=20, sticky='e')


    # Botão de voltar
    back_button = tk.Button(new_windown_adress, text="Voltar", font=button_font, command=back_to_caw,
                            bg='#455874',
                            fg='white')
    back_button.grid(row=7, column=1, pady=0, padx=20, sticky='e')



# Função para abrir a tela de criar conta
def open_create_account(tela):
    # Esconde a janela principal
    tela.withdraw()

    # Cria a nova janela para criar conta
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Criar Conta")
    create_account_window.geometry("400x600")
    create_account_window.configure(bg='#457b9d')

    # Função para cadastrar
    def cadastrar():
        dados = {"user" : user_entry.get(),
                 "nome completo" : username_entry.get(),
                 "senha" : password_entry.get(),
                 "senha2" : password2_entry.get(),
                 "cpf" : cpf_entry.get(),
                 "data de nascimento" : dob_entry.get(),
                 "email" : email_entry.get(),
                 "número de telefone" : phone_entry.get()}
        resultado = validar_dados(dados)
        validacao = resultado[0]
        informacao = resultado[1]
        if validacao == False:
            aviso_cadastro.configure(fg='red')
            aviso_cadastro.configure(text=informacao)
            aviso_cadastro.grid(columnspan=2)
        else:
            aviso_cadastro.configure(fg='#457b9d')
            open_account_adress(create_account_window, dados)

    # Função para voltar à tela principal
    def back_to_main():
        create_account_window.destroy()
        tela.deiconify()

    # Frame para organizar os labels e entradas
    #form_frame = tk.Frame(create_account_window, bg='#457b9d')
    #form_frame.pack(pady=20)

    # Label e Entry para username
    user_label = tk.Label(create_account_window, text="User:", font=label_font, bg='#457b9d',
                              fg='white')
    user_label.grid(row=0, column=0, padx=10, pady=9, sticky='e')
    user_entry = tk.Entry(create_account_window, font=entry_font, width=22)
    user_entry.grid(row=0, column=1, padx=10, pady=9)
    username_entry_for_db = user_entry

    # Label e Entry para Nome Completo
    username_label = tk.Label(create_account_window, text="Nome Completo:", font=label_font, bg='#457b9d', fg='white')
    username_label.grid(row=1, column=0, padx=10, pady=9, sticky='e')
    username_entry = tk.Entry(create_account_window, font=entry_font, width=22)
    username_entry.grid(row=1, column=1, padx=10, pady=9)
    username_entry_for_db = username_entry

    # Label e Entry para Senha
    password_label = tk.Label(create_account_window, text="Senha:", font=label_font, bg='#457b9d', fg='white')
    password_label.grid(row=2, column=0, padx=10, pady=9, sticky='e')
    password_entry = tk.Entry(create_account_window, font=entry_font, width=22, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=9)
    username_entry_for_db = username_entry

    # Label e Entry para Senha
    password2_label = tk.Label(create_account_window, text="Confirmar Senha:", font=label_font, bg='#457b9d', fg='white')
    password2_label.grid(row=3, column=0, padx=10, pady=9, sticky='e')
    password2_entry = tk.Entry(create_account_window, font=entry_font, width=22, show="*")
    password2_entry.grid(row=3, column=1, padx=10, pady=9)
    username_entry_for_db = username_entry

    # Label e Entry para CPF
    cpf_label = tk.Label(create_account_window, text="CPF:", font=label_font, bg='#457b9d', fg='white')
    cpf_label.grid(row=4, column=0, padx=10, pady=9, sticky='e')
    global cpf_entry
    cpf_entry = tk.Entry(create_account_window, font=entry_font, width=15)
    cpf_entry.grid(row=4, column=1, padx=10, pady=9, sticky='w')
    cpf_entry.bind("<KeyRelease>", format_cpf)

    # Label e Entry para Data de Nascimento
    dob_label = tk.Label(create_account_window, text="Data de Nascimento:", font=label_font, bg='#457b9d', fg='white')
    dob_label.grid(row=5, column=0, padx=10, pady=9, sticky='w')
    global dob_entry
    dob_entry = tk.Entry(create_account_window, font=entry_font, width=15)
    dob_entry.grid(row=5, column=1, padx=10, pady=9, sticky='w')
    dob_entry.bind("<KeyRelease>", format_date)

    # Label e Entry para E-mail
    email_label = tk.Label(create_account_window, text="E-mail:", font=label_font, bg='#457b9d', fg='white')
    email_label.grid(row=6, column=0, padx=10, pady=9, sticky='e')
    email_entry = tk.Entry(create_account_window, font=entry_font, width=22)
    email_entry.grid(row=6, column=1, padx=10, pady=9)
    email_entry_for_db = email_entry

    # Label e Entry para Número de Celular
    phone_label = tk.Label(create_account_window, text="Número de Celular:", font=label_font, bg='#457b9d', fg='white')
    phone_label.grid(row=7, column=0, padx=10, pady=9, sticky='e')
    global phone_entry
    phone_entry = tk.Entry(create_account_window, font=entry_font, width=15)
    phone_entry.grid(row=7, column=1, padx=10, pady=9, sticky='w')
    phone_entry.bind("<KeyRelease>", format_phone)

    # Aviso caso a conta não seja encontrado
    aviso_cadastro = tk.Label(create_account_window, text="", font=label_font, bg='#457b9d',
                              fg='#457b9d')
    aviso_cadastro.grid(row=8)

    # Botão de cadastrar
    register_button = tk.Button(create_account_window, text="Próximo", font=button_font, command=cadastrar,
                                bg='#455874', fg='white')
    register_button.grid(row=9, column=0, pady=20, sticky='e')

    # Botão de voltar
    back_button = tk.Button(create_account_window, text="Voltar", font=button_font, command=back_to_main, bg='#455874',
                            fg='white')
    back_button.grid(row=9, column=1, pady=0, padx=20, sticky='e')





# Função para validar todos os dados informados pelo usuário
def validar_dados(dados):
    validacao_username = validar_username(dados.get("user"))
    validacao_nome = validar_nome_completo(dados.get("nome completo"))
    validacao_cpf = validar_cpf(dados.get("cpf"))
    validacao_senha = validar_senha(dados.get("senha"), dados.get("senha2"))
    validacao_data = validar_data_nascimento(dados.get("data de nascimento"))
    validacao_email = validar_email(dados.get("email"))
    validacao_numero_telefone = validar_numero_celular(dados.get("número de telefone"))

    if validacao_username[0] == False:
        return [False, validacao_username[1]]
    elif validacao_nome[0] == False:
        return [False, validacao_nome[1]]
    elif validacao_cpf[0] == False:
        return [False, validacao_cpf[1]]
    elif validacao_senha[0] == False:
        return [False, validacao_senha[1]]
    elif validacao_data[0] == False:
        return [False, validacao_data[1]]
    elif validacao_email[0] == False:
        return [False, validacao_email[1]]
    elif validacao_numero_telefone[0] == False:
        return [False, validacao_numero_telefone[1]]
    else:
        return [True, ""]

def validar_dados_endereco(dados):
    validacao_cidade = validar_cidade(dados.get("cidade"))
    validacao_estado = validar_estado(dados.get("estado"))
    validacao_rua = validar_rua(dados.get("rua"))
    validacao_numero = validar_numero_endereco(dados.get("numero do endereço"))
    validacao_complemento = validar_complemento(dados.get("complemento"))

    if validacao_cidade[0] == False:
        return [False, validacao_cidade[1]]
    elif validacao_estado[0] == False:
        return [False, validacao_estado[1]]
    elif validacao_rua[0] == False:
        return [False, validacao_rua[1]]
    elif validacao_numero[0] == False:
        return [False, validacao_numero[1]]
    elif validacao_complemento[0] == False:
        return [False, validacao_complemento[1]]
    else:
        return [True, ""]




# Função para validar user
def validar_username(username):
    if type(username) == str:
        if buscar_usuario_por_nome(username) != False:
            return [False, "USUÁRIO JÁ EXISTENTE"]
        elif len(username) <= 4:
            return [False, "USER PRECISA TER MAIS DE 4 DÍGITOS"]
        else:
            return [True, ""]
    else:
        return [False, ""]

# Função para validar o campo de Nome Completo para adicionar no banco de dados
def validar_nome_completo(nome):
    if type(nome) == str:
        if any(char.isdigit() for char in nome):
            return [False, "NOME NÃO PODER TER NÚMEROS"]
        elif len(nome) < 4:
            return [False, "NOME PRECISA TER MAIS QUE 3 DÍGITOS"]
        else:
            return [True, ""]
    else:
        return [False, ""]

# Função para validar o campo de CPF para adicionar no banco de dados
def validar_cpf(cpf):
    new_cpf = ''
    for c in cpf:
        if c.isnumeric():
            new_cpf += c
    cpf = new_cpf
    if len(cpf) != 11:
        return [False, "CPF INCORRETO. NECESSITA 11 DÍGITOS"]
    else:
        return [True, ""]

def validar_senha(senha, confirmar_senha):
    if len(senha) < 6:
        return [False, "SENHA PRECISA TER MAIS QUE 6 DÍGITOS"]
    elif senha != confirmar_senha:
        return [False, "SENHAS NÃO CORRESPONDEM"]
    else:
        return [True, ""]

def validar_data_nascimento(data):
    new_data = ''
    for c in data:
        if c.isnumeric():
            new_data += c
    data = new_data
    if len(data) != 8:
        return [False, "FORMATO DA DATA INCORRETO"]
    ano = data[4:8]
    ano = int(ano)
    mes = int(data[2:4])
    dia = int(data[0:2])
    if len(data) != 8:
        return [False, "FORMATO DA DATA INCORRETO"]
    elif ano < 1910 or ano > 2020:
        return [False, "IDADE INCORRETA"]
    elif mes < 1 or mes >12 or dia < 1 or dia > 31:
        return [False, "FORMATO DA DATA INCORRETO"]
    else:
        ultimo_dia = 30
        if mes in (1, 3, 5, 7, 8, 10, 12) and dia <= 31:
            return [True, ""]
        elif mes == 2:
            # verifica se é ano bissexto
            if (ano % 4 == 0) and (ano % 100 != 0 or ano % 400 == 0):
                if dia <= 29:
                    return [True, ""]
            else:
                if dia <= 29:
                    return [True, ""]
        else:
            if dia <= 30:
                return [True, ""]
        return [False, "DATA INEXISTENTE"]

def validar_email(email):
    if "@" not in email:
        return [False, "EMAIL INVÁLIDO"]
    a, b = email.split("@")
    size_b = len(b)
    if len(a) < 3 or len(b) < 6:
        return [False, "EMAIL INVÁLIDO"]
    elif b[size_b-4:size_b] == ".com":
        return [True, ""]
    elif b[size_b-7:size_b] == ".com.br":
        return [True, ""]
    else:
        return [False, "EMAIL INVÁLIDO"]

def validar_numero_celular(numero):
    new_telefone = ''
    for c in numero:
        if c.isnumeric():
            new_telefone += c
    numero = new_telefone
    if len(numero) != 11:
        return [False, "NÚMERO DE TELEFONE INCORRETO"]
    else:
        return [True, ""]

def validar_cidade(cidade):
    for c in cidade:
        if c.isnumeric():
            return [False, "NO CAMPO CIDADE NÃO É PERMITIDO NÚMEROS"]
    if len(cidade) <= 3:
        return [False, "CIDADE PRECISA TER MAIS QUE 3 LETRAS"]
    else:
        return [True, ""]

def validar_estado(estado):
    if len(estado) <= 1:
        return [False, "DIGITE A SIGLA DO ESTADO"]
    else:
        return [True, ""]

def validar_rua(rua):
    if len(rua) <= 2:
        return [False, "RUA PRECISA TER MAIS QUE 2 DÍGITOS"]
    else:
        return [True, ""]

def validar_numero_endereco(numero):
    if len(numero) <= 2:
        return [False, "NÚMERO PRECISA TER MAIS QUE 2 DÍGITOS"]
    elif len(numero) >= 6:
        return [False, "NÚMERO NÃO PODE TER MAIS QUE 5 DÍGITOS"]
    else:
        return [True, ""]

def validar_complemento(complemento):
    if len(complemento) <= 4:
        return [False, "NO MÍNIMO 5 DÍGITOS EM COMPLEMENTO"]
    else:
        return [True, ""]

def open_login():
    root.withdraw()

    # Configurações da janela de login
    tela_login = tk.Toplevel(root)
    tela_login.title("Tela de Login")
    tela_login.geometry("400x600")
    tela_login.configure(bg='#457b9d')

    # Função para abrir uma nova janela ao clicar no botão de login
    def open_new_window():
        if len(login_entry.get()) == 0:
            aviso.configure(text="DIGITE SEU LOGIN")
            aviso.configure(fg='#FFFFFF')
        elif len(password_entry.get()) == 0:
            aviso.configure(text="DIGITE SUA SENHA")
            aviso.configure(fg='#FFFFFF')
        else:
            login = login_entry.get()
            p = password_entry.get()
            busca = buscar_usuario_por_nome(login)
            if busca == False:
                # USUÁRIO NÃO EXISTE
                aviso.configure(text="CONTA NÃO ENCONTRADA. CADASTRE-SE")
                aviso.configure(fg='#FFFFFF')
            elif busca == None:
                # ERRO AO CONECTAR COM BANCO DE DADOS
                print("erro")
            else:
                if p == busca:
                    aviso.configure(fg='#457b9d')
                    tela_login.destroy()
                    root.deiconify()
                else:
                    aviso.configure(text="SENHA INCORRETA")
                    aviso.configure(fg='#FFFFFF')



    # Label e Entry para Login Helvetica
    login_label = tk.Label(tela_login, text="Login:", font=label_font, bg='#457b9d', fg='white')
    login_label.pack(pady=(20, 5))
    login_entry = tk.Entry(tela_login, font=entry_font)
    login_entry.pack(pady=(0, 10))

    # Label e Entry para Senha
    password_label = tk.Label(tela_login, text="Senha:", font=label_font, bg='#457b9d', fg='white')
    password_label.pack(pady=(10, 5))
    password_entry = tk.Entry(tela_login, font=entry_font, show='*')
    password_entry.pack(pady=(0, 20))

    # Aviso caso o conta não seja encontrado
    aviso = tk.Label(tela_login, text="CONTA NÃO ENCONTRADA. CADASTRE-SE", font=label_font, bg='#457b9d', fg='#457b9d')
    aviso.pack(pady=1)

    # Botão de Login
    login_button = tk.Button(tela_login, text="Login", font=button_font, command=open_new_window, bg='#455874', fg='white')
    login_button.pack(pady=20)

    # Link para criar conta
    create_account_link = tk.Label(tela_login, text="Criar conta", font=link_font, bg='#457b9d', fg='white', cursor="hand2")
    create_account_link.pack(pady=10)
    create_account_link.bind("<Button-1>", lambda e: open_create_account(tela_login))

# Função para abrir a subtela
def open_subwindow():
    root.withdraw()

    # Configurações da janela de login
    subtela = tk.Toplevel(root)
    subtela.title("Tela de Informações")
    subtela.geometry("400x600")
    subtela.configure(bg='#457b9d')

    def close_subtela():
        subtela.destroy()
        root.deiconify()



    # Botão de Sair
    close_button = tk.Button(subtela, text="X", font=button_font, command=close_subtela, bg='#455874',
                             fg='white', height=1, width=2)
    close_button.grid(column=1, row=0, padx=1, pady=10)

    # Botão de Dados do usuário
    data_button = tk.Button(subtela, text="DADOS", font=button_font, command=close_subtela, bg='#455874',
                             fg='white')
    data_button.grid(column=0, row=1, padx=100, pady=15)

    # Botão de Suporte
    data_button = tk.Button(subtela, text="SUPORTE", font=button_font, command=close_subtela, bg='#455874',
                            fg='white')
    data_button.grid(column=0, row=2, padx=100, pady=15)

    # Botão de Financeiro
    data_button = tk.Button(subtela, text="FINANCEIRO", font=button_font, command=close_subtela, bg='#455874',
                            fg='white')
    data_button.grid(column=0, row=3, padx=100, pady=15)

    # Botão de sair ou cadastrar
    data_button = tk.Button(subtela, text="SAIR OU CADASTRAR", font=button_font, command=close_subtela, bg='#455874',
                            fg='white')
    data_button.grid(column=0, row=4, padx=100, pady=15)




# Configurações da janela principal
root = tk.Tk()
root.title("Página principal")
root.geometry("400x600")
root.configure(bg='#457b9d')

# Configurações de estilo
label_font = ("Bahnschrift SemiBold", 12)
entry_font = ("Bahnschrift SemiBold", 12)
button_font = ("Bahnschrift SemiBold", 12, "bold")
link_font = ("Bahnschrift SemiBold", 10, "underline")

# Botão de Login
login_button = tk.Button(root, text="Login", font=button_font, command=open_login, bg='#455874', fg='white')
login_button.grid(row=0, column=0, padx=155, pady=20)

# Botão de informações do usuário
info_button = tk.Button(root, text="...", font=button_font, command=open_subwindow, bg='#455874', fg='white')
info_button.grid(row=0, column=1)




# Iniciar o loop principal da interface gráfica
root.mainloop()
from dateutil.parser import parse
from email.mime.base import MIMEBase
import os
from io import BytesIO
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_mail import Mail, Message
from config import email, senha
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import uuid
import glob

app = Flask(__name__)

saved_files = []
user_files = []

# Definir uma variável de contador global
#contador = 0

# Função para incrementar o contador
# def incrementar_contador():
   #contador += 1
    #return contador


# diretório raiz do aplicativo
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# caminho para a pasta de uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# configurando a pasta de uploads no app Flask
app.config['UPLOAD_FOLDER'] = 'X:\\INFORMATICA\\21- FORMULARIO\\FormularioStik_Vendas\\uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg',
                      'jpeg', 'gif', 'txt'}  # extensões permitidas
app.config['SECRET_KEY'] = 'supersecretkey'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


mail_settings = {
    "MAIL_SERVER": 'smtp.stik.com.br',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}

app.config.update(mail_settings)

mail = Mail(app)

def limpar_pasta_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file_name in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erro ao excluir arquivo {file_path}: {e}")

class Ficha:
    def __init__(self, dat, tipo, vendedor, razao_social, nome_fantasia, cnpj, inscricao_estadual, endereco, bairro, complemento, cep, cidade,
                 estado, contato, tel_contato, email_cliente, email_assis_comercial, email_gest_financeiro, email_gest_comercial,
                 referencia_comercial, contato_referencia, tel_referencia, valor_pedido, pagamento, prazo_estimado, parecer):
        self.dat = dat
        self.tipo = tipo
        self.vendedor = vendedor
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj
        self.inscricao_estadual = inscricao_estadual
        self.endereco = endereco
        self.bairro = bairro
        self.complemento = complemento
        self.cep = cep
        self.cidade = cidade
        self.estado = estado
        self.contato = contato
        self.tel_contato = tel_contato
        self.email_cliente = email_cliente
        self.email_assis_comercial = email_assis_comercial
        self.email_gest_financeiro = email_gest_financeiro
        self.email_gest_comercial = email_gest_comercial
        self.referencia_comercial = referencia_comercial
        self.contato_referencia = contato_referencia
        self.tel_referencia = tel_referencia
        self.valor_pedido = valor_pedido
        self.pagamento = pagamento
        self.prazo_estimado = prazo_estimado
        self.parecer = parecer


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_list = request.form.get('file_list')
        print(f"Print 1: {file_list}")
        # Faça o que precisar com a lista de arquivos aqui
        return 'Arquivos recebidos: ' + file_list
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file_upload')
    filename = secure_filename(file.filename)
    # adiciona o caminho completo do arquivo
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    saved_files.append(file_path)  # armazena o caminho completo na lista
    print(f'2-valor de saved_files: {saved_files}')
    files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    print(f'6-Lista de arquivos salvos: {files}')
    return 'Arquivo recebido com sucesso!'


print(
    f'Valor de saved_files: {saved_files} e valor de user_files: {user_files}')


@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        file = request.files.get('file_upload')

        if file:
            filename = secure_filename(file.filename)
            # adiciona o caminho completo do arquivo
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # armazena o caminho completo na lista
            saved_files.append(file_path)
            print(f'Lista de caminhos salvos saved_files: {saved_files}')
            # adiciona o arquivo à lista de arquivos enviados pelo usuário
            user_files.append(file)
            print(f'Lista de arquivos salvos user_files: {user_files}')
            # files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
            # print(f'3-Lista de arquivos salvos: {file}')

        for file in user_files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # file.save(file_path)
            saved_files.append(file_path)

        formFicha = Ficha(
            request.form["dat"],
            request.form["tipo"],
            request.form["vendedor"],
            request.form["razao_social"],
            request.form["nome_fantasia"],
            request.form["cnpj"],
            request.form["inscricao_estadual"],
            request.form["endereco"],
            request.form["bairro"],
            request.form["complemento"],
            request.form["cep"],
            request.form["cidade"],
            request.form["estado"],
            request.form["contato"],
            request.form["tel_contato"],
            request.form["email_cliente"],
            request.form["email_assis_comercial"],
            request.form["email_gest_financeiro"],
            request.form["email_gest_comercial"],
            request.form["referencia_comercial"],
            request.form["contato_referencia"],
            request.form["tel_referencia"],
            request.form["valor_pedido"],
            request.form["pagamento"],
            request.form["prazo_estimado"],
            request.form["parecer"],
        )

        data_form = formFicha.dat
        data_obj = parse(data_form)
        data_formatada = data_obj.strftime('%d/%m/%Y')

        # Verificar o valor do campo 'formFicha.tipo' e definir o tipo correspondente
        if formFicha.tipo == 'novo':
            tipo = 'Novo'
        elif formFicha.tipo == 'atualização':
            tipo = 'Atualização'
        else:
            tipo = 'Renovação'

        #numero_ficha = incrementar_contador()

        # cria a mensagem de e-mail
        msg = Message(
            #subject=f'Ficha de Cadastro: {"Novo" if formFicha.tipo == "Novo" else "Atualização" if formFicha.tipo == "atualizacao" else "Renovação"} - {formFicha.vendedor}',
            # Atualizar o elemento subject com o valor do contador
            subject = f'Ficha de Cadastro: {tipo} - {formFicha.razao_social}',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[request.form["email_assis_comercial"],
                        request.form["email_gest_financeiro"], request.form["email_gest_comercial"]],
            html=f'''
                            <table style="border-collapse: collapse; width: 50%; font-family: Arial, Helvetica, sans-serif;">
                        
                            <tr>
                                <th style="padding: 8px;  width: 18%; text-align: left; border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Data:</th>
                                <td style="padding: 8px; width: 20%; text-align: left; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{data_formatada}</td>
                            </tr>

                            <tr>    
                                <th style="padding: 8px; width: 18%; text-align: left; border-bottom: 2px solid #444444; border-right: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Tipo:</th>
                                <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{tipo}</td>        
                            </tr> 

                                <tr>
                                    <th th style="padding: 8px; width: 18%;  text-align: left; border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Vendedor:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.vendedor}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px;  width: 18%; text-align: left; border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Razão Social:</th>
                                    <td style= "padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.razao_social}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left; border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Nome Fantasia:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.nome_fantasia}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">CNPJ:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.cnpj}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px;  width: 18%; text-align: left; border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Inscrição Estadual:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.inscricao_estadual}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px;  width: 18%; text-align: left; border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Endereço:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.endereco}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Bairro:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.bairro}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Complemento:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.complemento}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px;  width: 18%; text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">CEP:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.cep}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Cidade:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.cidade}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Estado:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.estado}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Contato:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.contato}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Telefone Contato:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.tel_contato}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Email Cliente:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.email_cliente}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Email Assistente Comercial:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.email_assis_comercial}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Email Gestor Financeiro:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.email_gest_financeiro}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Email Gestor Comercial:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.email_gest_comercial}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Referência Comercial:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.referencia_comercial}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Contato Comercial:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.contato_referencia}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Telefone Comercial:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.tel_referencia}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Valor Pedido:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.valor_pedido}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Pagamento:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.pagamento}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Prazo Estimado:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.prazo_estimado}</td>
                                </tr>

                                <tr>
                                    <th style="padding: 8px; width: 18%;  text-align: left;  border-right: 2px solid #444444; border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">Parecer:</th>
                                    <td style="padding: 8px; width: 20%; text-align: left;  border-bottom: 2px solid #444444; background-color: #F0F0F0; color: #002B5B;">{formFicha.parecer}</td>
                                </tr>

                        </table>
                                    '''
        )
        print(f'4-valor de saved_files: {saved_files}')

        # Anexa todos os arquivos da lista ao email
        if user_files:
            for file in user_files:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                saved_files.append(file_path)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        msg.attach(file.filename, file.mimetype, f.read())
                else:
                    print(f"Arquivo não encontrado: {file_path}")

        print(f'5-valor de saved_files: {saved_files}')

        # envia email
        mail.send(msg)
        # limpa a pasta de uploads
        limpar_pasta_uploads()
       
      
        flash('Mesagem enviada com sucesso!')
        return redirect('/')
    else:
        flash('Extensão de arquivo não permitida!')
        return redirect('/')
    
    
if __name__ == '__main__':
    app.run(debug=True)

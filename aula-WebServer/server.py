import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
# biblioteca para conectar ao banco mysql (tem que instalar com pip install mysql-connector-python)
import mysql.connector

# conecta no banco de dados, usando usuário root e senha senai
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai",
    database="SERVIDORFILMES"  
)

# essa lista é usada para armazenar os filmes quando não estamos usando o banco
filmes_cadastrados = []

# função que carrega os filmes do arquivo data.json (caso o banco não esteja sendo usado)
def load_filmes():
    global filmes_cadastrados
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            try:
                filmes_cadastrados = json.load(f)
            except json.JSONDecodeError:
                filmes_cadastrados = []
                
def save_filmes():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(filmes_cadastrados, f, ensure_ascii=False, indent=4)

load_filmes()


# classe que trata as requisições do servidor http
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r')

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))  # wfile é o que vai ser enviado para o cliente
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)

    def account_user(self, login, senha):
        loga = "heloisamilitaosouza@hotmail.com"
        password = 123456

        if login == loga and senha == password:
            return json.dumps({"status": "success", "message": "Usuário Logado"})
        else:
            return json.dumps({"status": "error", "message": "Usuário inexistente!"})
        
        
    def insertFilme(self, nome, produtora, orcamento, duracao, ano, poster):
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO SERVIDORFILMES.filme (titulo, id_produtora, orcamento, duracao, ano, poster) VALUES (%s, %s, %s, %s, %s, %s)",(nome, produtora, duracao, ano, poster)) 
        cursor.execute("SELECT id_filme FROM SERVIDORFILMES.filme WHERE titulo = %s",(nome,))    
        resultado = cursor.fetchall()
        cursor.execute("SELECT * FROM SERVIDORFILMES.filme WHERE id_filme = %s, {resultado[0][0]},")   
        resultado = cursor.fetchall()
        print(resultado)
        cursor.close()
        return resultado
        
    

    def do_GET(self):
        if self.path == "/loginzin":
            try:
                with open(os.path.join(os.getcwd(), "login.html"), "r") as login:
                    content = login.read()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")    
        elif self.path == "/cadastro":
            try:
                with open(os.path.join(os.getcwd(), "cadastro.html"), "r") as cadastro:
                    content = cadastro.read()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        elif(self.path == "/lista"):
            try:
                with open(os.path.join(os.getcwd(), "lista.html"), encoding='utf-8') as listaFilmes:
                    content = listaFilmes.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('UTF-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
                pass

        elif self.path == "/listarfilmes":
            try:
                cursor = mydb.cursor(dictionary=True)
                query = """
                SELECT 
                    f.id,
                    f.titulo,
                    f.ano,
                    f.tempo_duracao,
                    f.poster,
                    GROUP_CONCAT(DISTINCT g.nome) AS generos,
                    GROUP_CONCAT(DISTINCT p.nome) AS produtoras,
                    GROUP_CONCAT(DISTINCT CONCAT(d.nome, ' ', d.sobrenome)) AS diretores
                FROM filme f
                LEFT JOIN filme_genero fg ON f.id = fg.filme_id
                LEFT JOIN genero g ON fg.genero_id = g.id
                LEFT JOIN filme_produtora fp ON f.id = fp.filme_id
                LEFT JOIN produtora p ON fp.produtora_id = p.id
                LEFT JOIN filme_diretor fd ON f.id = fd.filme_id
                LEFT JOIN diretor d ON fd.filme_diretor = d.id
                GROUP BY f.id
                ORDER BY f.ano DESC;
                """
                cursor.execute(query)
                filmes = cursor.fetchall()

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(filmes, ensure_ascii=False, indent=4).encode("utf-8"))

            except mysql.connector.Error as err:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"erro": str(err)}).encode("utf-8"))

        else:
            super().do_GET()


    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email', [""])[0]
            password = int(form_data.get('senha', [""])[0])
            logou = self.account_user(login, password)


            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(logou.encode('utf-8'))

        elif self.path == '/send_cadastro':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            nome = form_data.get('nome',[""])[0]
            produtora = form_data.get('produtora',[""])[0]
            orcamento = int(form_data.get('orcamento',[""])[0])
            duracao = form_data.get('duracao',[""])[0]
            ano = form_data.get('ano',[""])[0]
            poster = form_data.get('capa',[""])[0]

            resp = self.insertFilme(nome, produtora, orcamento, duracao, ano, poster)

            
            # nome = form_data.get('nome',[""])[0]
            # atores = form_data.get('atores', [""])[0]
            # diretor = form_data.get('diretor', [""])[0]
            # ano = form_data.get('ano', [""])[0]
            # genero = form_data.get('genero', [""])[0]
            # produtora = form_data.get('produtora', [""])[0]
            # sinopse = form_data.get('sinopse', [""])[0]

            # filme = {
            #     "id": len(filmes_cadastrados),
            #     "nome": nome,
            #     "atores": atores,
            #     "diretor": diretor,
            #     "ano": ano,
            #     "genero": genero,
            #     "produtora": produtora,
            #     "sinopse": sinopse
            # }
            
            # filmes_cadastrados.append(filme)
            
            # save_filmes()

            # print("Data Form: ")
            # print("Nome do Filme: ", form_data.get('nome', [''])[0])
            # print("Atores: ", form_data.get('atores', [''])[0])
            # print("Diretor: ", form_data.get('diretor', [''])[0])
            # print("Ano: ", form_data.get('ano', [''])[0])
            # print("Genero: ", form_data.get('genero', [''])[0])
            # print("Produtora: ", form_data.get('produtora', [''])[0])
            # print("Sinopse: ", form_data.get('sinopse', [''])[0])

            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write("Filme cadastrado com sucess !".encode('utf-8'))
            
        elif self.path == '/editarfilme':
           
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            filme_id = int(form_data.get('id', [None])[0])
            
    
            if filme_id is None or filme_id >= len(filmes_cadastrados):
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Filme não encontrado'}).encode('utf-8'))
                return

            filme = filmes_cadastrados[filme_id]

            for campo in ['nome', 'atores', 'diretor', 'ano', 'genero', 'produtora', 'sinopse']:
                valor = form_data.get(campo, [None])[0]
                if valor:
                    filme[campo] = valor

            save_filmes()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Filme editado com sucesso'}).encode('utf-8'))


        elif self.path == '/deletarfilme':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            try:
                filme_id = int(form_data.get('id', [None])[0])
            except (ValueError, TypeError):
                filme_id = None

            if filme_id is None or filme_id >= len(filmes_cadastrados):
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Filme não encontrado'}).encode('utf-8'))
                return

            filmes_cadastrados.pop(filme_id)

            # Reatribui os IDs
            for i, filme in enumerate(filmes_cadastrados):
                filme["id"] = i

            save_filmes()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Filme deletado com sucesso'}).encode('utf-8'))


        else:
            super(MyHandler, self).do_POST()


def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server Running http://localhost:8000")
    httpd.serve_forever()

main()

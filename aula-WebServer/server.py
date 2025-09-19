# from http.server import SimpleHTTPRequestHandler, HTTPServer

# #definidondo a porta
# port = 8000

# #definindo o gerenciador/manipulador de requisições
# handler = SimpleHTTPRequestHandler
# #crando a instancia servidor
# server = HTTPServer(('localhost', port), handler)
# #imprimindo mensagem de OK :)
# print(f"Server Running in http://localhost:{port}")

# server.serve_forever()
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


filmes_cadastrados = []

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), 'r')

            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8')) #wfile é o que vai ser enviado para o cliente
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)
    
    def account_user (self ,login,senha):
        loga = "heloisamilitaosouza@hotmail.com"
        password = 123456

        if login == loga and senha == password:
            return "Uusário Logado"
        else:
            return "Usuário inexistente!"
        
    def do_GET(self):
        if self.path == "/loginzin":
            try:
                with open(os.path.join(os.getcwd(),"login.html"), "r") as login:
                    content = login.read()

                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")    
        elif self.path == "/cadastro":
            try:
                with open(os.path.join(os.getcwd(),"cadastro.html"), "r") as login:
                    content = login.read()

                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")   
        elif self.path == "/lista":
            html = """
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Lista de Filmes</title>
            </head>
            <body>
                <h1>Filmes Cadastrados</h1>
                <ul>
            """

            for filme in filmes_cadastrados:
                html += f"""
                    <li>
                        <strong>{filme['nome']}</strong> ({filme['ano']})<br>
                        Diretor: {filme['diretor']}<br>
                        Atores: {filme['atores']}<br>
                        Gênero: {filme['genero']}<br>
                        Produtora: {filme['produtora']}<br>
                        Sinopse: {filme['sinopse']}<br>
                        <hr>
                    </li>
                """

            html += """
                </ul>
                <a href="/cadastro">Cadastrar novo filme</a>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

            try:
                with open(os.path.join(os.getcwd(),"lista.html"), "r") as login:
                    content = login.read()

                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")            
        else:
            super().do_GET()    

    def do_POST(self):
        if self.path == '/send_login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email',[""])[0]
            password = int(form_data.get('senha',[""])[0])
            logou = self.account_user(login,password)

            print("Data form:")
            print("E-mail: ", form_data.get('email',[""])[0])
            print("Senha: ", form_data.get('senha',[""])[0])

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(logou.encode('utf-8'))

        elif self.path == '/send_cadastro':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            filme = {
                "nome": form_data.get('nome', [""])[0],
                "atores": form_data.get('atores', [""])[0],
                "diretor": form_data.get('diretor', [""])[0],
                "ano": form_data.get('ano', [""])[0],
                "genero": form_data.get('genero', [""])[0],
                "produtora": form_data.get('produtora', [""])[0],
                "sinopse": form_data.get('sinopse', [""])[0],
            }

            filmes_cadastrados.append(filme)

            print("Filme cadastrado:", filme)


            self.send_response(303)  
            self.send_header('Location', '/lista')
            self.end_headers()


        else:
            super(MyHandle, self).do_POST()

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running http://localhost:8000")
    httpd.serve_forever()
main()    
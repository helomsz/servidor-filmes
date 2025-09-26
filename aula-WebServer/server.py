import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


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
        
        elif (self.path == "/get_lista"):
            
            arquivo = "data.json"

            if os.path.exists(arquivo):
                with open(arquivo, encoding="utf-8") as listagem:
                    try:
                        filmes = json.load(listagem)
                    except json.JSONDecodeError:
                        filmes = []
            else:
                filmes = []

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(filmes).encode("utf-8"))

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

            jsum = {
                "nome": form_data.get('nomeFilme', [""])[0],
                "atores":form_data.get('atores', [""])[0],
                "diretor": form_data.get('diretor', [""])[0],
                "ano": str(form_data.get('anoFilme', ["0"])[0]),
                "generos": form_data.get('genero', [""])[0],
                "sinopse": form_data.get('sinopse', [""])[0],
                "produtora": form_data.get('produtora', [""])[0]
            }

            arquivo = "data.json"
            if os.path.exists(arquivo):
                with open(arquivo,  "r", encoding="utf-8") as lista:
                    try:
                        filmes = json.load(lista)
                    except json.JSONDecodeError:
                        filmes = []
                filmes.append(jsum)
            else:
                filmes = [jsum]

            with open(arquivo, "w", encoding="utf-8") as lista:
                json.dump(filmes, lista, indent=4, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(str(jsum).encode('utf-8'))

        else:
            super(MyHandler, self).do_POST()

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server Running http://localhost:8000")
    httpd.serve_forever()

main()

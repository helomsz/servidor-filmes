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

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index2.html'), 'r')

            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8')) #wfile é o que vai ser enviado para o cliente
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)
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

def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running http://localhost:8000")
    httpd.serve_forever()
main()    
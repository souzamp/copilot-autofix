import sqlite3
import os
import subprocess
from flask import Flask, request, make_response
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Função de autenticação (implementação simplificada)
@auth.get_password
def get_password(username):
    # Aqui você pode implementar a lógica real para verificar as credenciais
    users_db_path = 'usuarios.db'
    
    conn = sqlite3.connect(users_db_path)
    cursor = conn.cursor()
    query = "SELECT password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None

def autenticar_usuario(username, password):
    # Usamos a função de autenticação HTTPBasicAuth para verificar as credenciais
    return auth.authenticate(username, password)

@app.route("/ping")
@auth.login_required
def ping():
    ip = request.args.get("ip", "")
    
    if not ping_valido(ip):
        return "Invalid IP address"
    
    output = subprocess.getoutput(f"ping -c 1 {ip}")
    return f"<pre>{output}</pre>"

@app.route("/debug")
@auth.login_required
def debug():
    # Não exponhamos a SECRET_KEY
    return "Debug endpoint is protected."

@app.route("/comente")
@auth.login_required
def comente():
    comentario = request.args.get("comentario", "")
    return f"<h1>Comentário recebido:</h1><p>{comentario}</p>"

# Função para validar endereços IP
def ping_valido(ip):
    # Verifique se é um endereço IP válido (implementação simplificada)
    try:
        parts = ip.split('.')
        if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) < 256 for part in parts):
            return True
    except ValueError:
        pass
    return False

if __name__ == '__main__':
    app.run(debug=True)

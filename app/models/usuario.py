import json
import os

class Usuario:
    __arquivo_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usuarios.json')

    @classmethod
    def __garantir_admin(cls):
        
        if not os.path.exists(cls.__arquivo_db):
            admin_padrao = [{"username": "admin", "password": "123"}]
            with open(cls.__arquivo_db, 'w', encoding='utf-8') as f:
                json.dump(admin_padrao, f)

    @classmethod
    def autenticar(cls, username, password_input):
        cls.__garantir_admin()
        
        with open(cls.__arquivo_db, 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
        
        
        for u in usuarios:
            if u['username'] == username and u['password'] == password_input:
                return True
        return False
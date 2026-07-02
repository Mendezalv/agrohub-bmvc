import json
import os
import uuid

class Animal:
    
    __arquivo_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rebanho.json')

    def __init__(self, especie, peso, status, id_animal=None):
        
        self.__id = id_animal if id_animal else str(uuid.uuid4())[:8]
        self.__especie = self.__validar_texto(especie, "Espécie")
        self.__peso = self.__validar_peso(peso)
        self.__status = self.__validar_texto(status, "Status")

    
    def __validar_peso(self, peso):
        try:
            peso_float = float(peso)
            if peso_float <= 0:
                return "0" 
            return str(peso_float) 
        except (ValueError, TypeError):
            return "Inválido"

    def __validar_texto(self, texto, campo):
        if not texto or str(texto).strip() == "":
            return f"{campo} Não Informado"
        return str(texto).strip()
    
    @classmethod
    def atualizar(cls, animal_id, especie, peso, status):
        animais = cls.ler_todos()
        for a in animais:
            if a['id'] == animal_id:
                
                temp = cls(especie, peso, status, id_animal=animal_id)
                a['especie'] = temp.especie
                a['peso'] = temp.peso
                a['status'] = temp.status
                break
                
        with open(cls.__arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(animais, f, indent=4)

    
    @property
    def id(self): return self.__id
    @property
    def especie(self): return self.__especie
    @property
    def peso(self): return self.__peso
    @property
    def status(self): return self.__status

    def to_dict(self):
        return {'id': self.id, 'especie': self.especie, 'peso': self.peso, 'status': self.status}

    
    @classmethod
    def __garantir_arquivo(cls):
        if not os.path.exists(cls.__arquivo_db):
            with open(cls.__arquivo_db, 'w', encoding='utf-8') as f:
                json.dump([], f)

    @classmethod
    def ler_todos(cls):
        cls.__garantir_arquivo()
        with open(cls.__arquivo_db, 'r', encoding='utf-8') as f:
            return json.load(f)

    def salvar(self):
        animais = self.ler_todos()
        animais.append(self.to_dict())
        with open(self.__arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(animais, f, indent=4)

    @classmethod
    def deletar(cls, animal_id):
        animais = cls.ler_todos()
        animais = [a for a in animais if a['id'] != animal_id]
        with open(cls.__arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(animais, f, indent=4)
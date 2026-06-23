import json
import os
import uuid

class Animal:
    arquivo_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rebanho.json')

    @classmethod
    def _garantir_arquivo(cls):
        if not os.path.exists(cls.arquivo_db):
            with open(cls.arquivo_db, 'w', encoding='utf-8') as f:
                json.dump([], f)

    @classmethod
    def ler_todos(cls):
        cls._garantir_arquivo()
        with open(cls.arquivo_db, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def criar(cls, especie, peso, status):
        animais = cls.ler_todos()
        novo_animal = {
            'id': str(uuid.uuid4())[:8],
            'especie': especie,
            'peso': peso,
            'status': status
        }
        animais.append(novo_animal)
        with open(cls.arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(animais, f, indent=4)
        return novo_animal

    @classmethod
    def deletar(cls, animal_id):
        animais = cls.ler_todos()
        animais = [a for a in animais if a['id'] != animal_id]
        with open(cls.arquivo_db, 'w', encoding='utf-8') as f:
            json.dump(animais, f, indent=4)
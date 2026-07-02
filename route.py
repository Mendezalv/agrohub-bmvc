from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
from app.models.animal import Animal
from app.models.usuario import Usuario  

app = Bottle()
ctl = Application()


SECRET = 'agrohub_seguro_fga'

def checar_acesso():
   
    sessao = request.get_cookie('sessao', secret=SECRET)
    if not sessao:
        redirect('/login')


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='/bmeta/app/static')

@app.route('/')
def index():
    return static_file('index.html', root='/bmeta/app/views/html')


@app.route('/login')
def get_login():
    return template('app/views/html/login.html')

@app.route('/login', method='POST')
def post_login():
    usuario = request.forms.get('username')
    senha = request.forms.get('password')
    
    
    if Usuario.autenticar(usuario, senha):
        
        response.set_cookie('sessao', 'logado', secret=SECRET, path='/')
        redirect('/rebanho')
    else:
        
        redirect('/login?erro=1')

@app.route('/logout')
def logout():
    
    response.delete_cookie('sessao', path='/')
    redirect('/login')


@app.route('/rebanho')
def listar_rebanho():
    checar_acesso() 
    animais = Animal.ler_todos()
    return template('app/views/html/rebanho.html', animais=animais)

@app.route('/rebanho/adicionar', method='POST')
def adicionar_animal():
    checar_acesso()
    especie = request.forms.get('especie').encode('iso-8859-1').decode('utf-8')
    peso = request.forms.get('peso')
    status = request.forms.get('status').encode('iso-8859-1').decode('utf-8')
    
    
    novo_animal = Animal(especie, peso, status)
    novo_animal.salvar()
    
    redirect('/rebanho')

@app.route('/rebanho/editar/<animal_id>')
def editar_animal(animal_id):
    checar_acesso()
    animais = Animal.ler_todos()
    
    animal_alvo = None
    for a in animais:
        if a['id'] == animal_id:
            animal_alvo = a
            break
            
    if not animal_alvo:
        redirect('/rebanho')
        
    return template('app/views/html/editar.html', animal=animal_alvo)

@app.route('/rebanho/editar/<animal_id>', method='POST')
def post_editar_animal(animal_id):
    checar_acesso()
    especie = request.forms.get('especie').encode('iso-8859-1').decode('utf-8')
    peso = request.forms.get('peso')
    status = request.forms.get('status').encode('iso-8859-1').decode('utf-8')
    
    Animal.atualizar(animal_id, especie, peso, status)
    redirect('/rebanho')

@app.route('/rebanho/deletar/<animal_id>')
def deletar_animal(animal_id):
    checar_acesso()
    Animal.deletar(animal_id)
    redirect('/rebanho')

if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=8080, debug=True)
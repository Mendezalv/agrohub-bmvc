from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
from app.models.animal import Animal

app = Bottle()
ctl = Application()

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='/bmeta/app/static')

@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')

@app.route('/')
def index():
    return static_file('index.html', root='/bmeta/app/views/html')

@app.route('/rebanho')
def listar_rebanho():
    animais = Animal.ler_todos()
    return template('app/views/html/rebanho.html', animais=animais)

@app.route('/rebanho/adicionar', method='POST')
def adicionar_animal():
    # Forçando a conversão para o padrão UTF-8 correto
    especie = request.forms.get('especie').encode('iso-8859-1').decode('utf-8')
    peso = request.forms.get('peso')
    status = request.forms.get('status').encode('iso-8859-1').decode('utf-8')
    
    Animal.criar(especie, peso, status)
    redirect('/rebanho')

@app.route('/rebanho/deletar/<animal_id>')
def deletar_animal(animal_id):
    Animal.deletar(animal_id)
    redirect('/rebanho')

if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=8080, debug=True)
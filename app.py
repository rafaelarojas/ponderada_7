from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
import pydobot
import time

app = Flask(__name__)
db = TinyDB('logs.json')

robo = pydobot.Dobot(port='COM3', verbose=False)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para controlar o robô
@app.route('/controleRobo', methods=['GET', 'POST'])
def controle_robo():
    if request.method == 'GET':
        return render_template('controle_robo.html')
    elif request.method == 'POST':
        # Obtendo os dados do formulário
        x = int(request.form['x'])
        y = int(request.form['y'])
        z = int(request.form['z'])


        xi, yi, zi, _,_,_,_,_ = robo.pose()
        
        robo.move_to(xi+x, yi, zi, 0, wait=True)
        time.sleep(0.5)
        robo.move_to(xi+x, yi+y, zi, 0, wait=True)
        time.sleep(0.5)
        robo.move_to(xi+x, yi+y, zi+z, 0, wait=True)
        time.sleep(0.5)
        
        # Salvando os movimentos na base de dados
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        db.insert({'x': x, 'y': y, 'z': z, 'timestamp': timestamp})

# Rota para obter os logs
@app.route('/logs', methods=['GET'])
def obter_logs():
    logs = db.all()
    return render_template('logs.html', logs=logs)

    # Rota para atualizar um registro de log
@app.route('/logs/update/<int:log_id>', methods=['POST'])
def atualizar_log(log_id):
    if request.method == 'POST':
        # Obtendo os dados atualizados do formulário
        x = int(request.form['x'])
        y = int(request.form['y'])
        z = int(request.form['z'])

        # Atualizando o registro na base de dados
        db.update({'x': x, 'y': y, 'z': z}, doc_ids=[log_id])

        return 'Registro atualizado com sucesso!'

# Rota para excluir um registro de log
@app.route('/logs/delete/<int:log_id>', methods=['POST'])
def excluir_log(log_id):
    if request.method == 'POST':
        # Excluindo o registro da base de dados
        db.remove(doc_ids=[log_id])

        return 'Registro excluído com sucesso!'

if __name__ == '__main__':
    app.run()

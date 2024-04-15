from flask import Flask, request, jsonify
from models.snack import Snack
from database import db
from datetime import datetime

#- Deve ser possível editar uma refeição, podendo alterar todos os dados acima
#- Deve ser possível apagar uma refeição
#- Deve ser possível listar todas as refeições de um usuário
#- Deve ser possível visualizar uma única refeição
#- As informações devem ser salvas em um banco de dados 🆗

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/snack', methods=['POST'])
def create_snack():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    hours_str = data.get('hours')  # Recebe a string de hora
    diet = data.get('diet')

    if name and description and hours_str and diet:
        try:
            hours = datetime.strptime(hours_str, '%Y-%m-%d %H:%M:%S')  # Converte a string de hora para um objeto DateTime
        except ValueError:
            return jsonify({"message": "Formato de hora inválido. Use o formato 'YYYY-MM-DD HH:MM:SS'"}), 400
        
        snack = Snack(name=name, description=description, hours=hours, diet=diet)
        db.session.add(snack)
        db.session.commit()
        return jsonify({"message": "Refeição criada com sucesso"}), 201
    
    return jsonify({"message": "Dados inválidos"}), 400





@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()

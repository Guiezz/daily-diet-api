from flask import Flask, request, jsonify
from models.snack import Snack
from database import db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/snack', methods=['POST']) # Rota para criar uma refeição
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

@app.route('/snack/<int:id>', methods=['PUT'])  # Rota para atualizar uma refeição
def update_snack(id):
    data = request.json
    name = data.get('name')         # Recebe o nome da refeição
    description = data.get('description')   # Recebe a descrição da refeição
    hours_str = data.get('hours')       # Recebe a string de hora
    diet = data.get('diet')         # Recebe a dieta da refeição

    if name or description or hours_str or diet:     # Verifica se pelo menos um campo foi preenchido
        snack = Snack.query.get(id)  # Busca a refeição pelo id
        if snack:  # Verifica se a refeição foi encontrada
            # Atualiza os dados da refeição apenas se os campos forem fornecidos
            if name:
                snack.name = name
            if description:
                snack.description = description
            if hours_str:
                try:
                    hours = datetime.strptime(hours_str, '%Y-%m-%d %H:%M:%S') # Converte a string de hora para um objeto DateTime
                    snack.hours = hours
                except ValueError:
                    return jsonify({"message": "Formato de hora inválido. Use o formato 'YYYY-MM-DD HH:MM:SS'"}), 400 # Retorna uma mensagem de erro caso a conversão falhe
            if diet:
                snack.diet = diet

            db.session.commit()
            return jsonify({"message": "Refeição atualizada com sucesso"}), 200
        
        return jsonify({"message": "Refeição não encontrada"}), 404

    return jsonify({"message": "Nenhum dado fornecido para atualização"}), 400

@app.route('/snack/<int:id>', methods=['DELETE'])  # Rota para deletar uma refeição
def delete_snack(id):
    snack = Snack.query.get(id)     # Busca a refeição pelo id

    if snack:
        db.session.delete(snack)    # Deleta a refeição
        db.session.commit()
        return jsonify({"message": "Refeição deletada com sucesso"}), 200
    
    return jsonify({"message": "Refeição não encontrada"}), 404

@app.route('/snack/<int:id>', methods=['GET'])  # Rota para visualizar uma refeição
def get_snack(id):
    snack = Snack.query.get(id)   # Busca a refeição pelo id

    if snack:
        return jsonify({"name": snack.name, "description": snack.description, "hours": snack.hours, "diet": snack.diet}), 200
    
    return jsonify({"message": "Refeição não encontrada"}), 404

@app.route('/snacks', methods=['GET'])  # Rota para listar todas as refeições
def get_snacks():
    snacks = Snack.query.all()  # Busca todas as refeições

    if snacks:
        snacks_list = []
        for snack in snacks:
            # Converte o objeto datetime para uma string no formato 'YYYY-MM-DD HH:MM:SS'
            hours_str = snack.hours.strftime('%Y-%m-%d %H:%M:%S')
            snacks_list.append({"name": snack.name, "description": snack.description, "hours": hours_str, "diet": snack.diet})
        return jsonify(snacks_list), 200
    
    return jsonify({"message": "Nenhuma refeição encontrada"}), 404




if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, jsonify, url_for
from models import db, Companhia, ModeloAeronave, Voo, Companhia, ModeloAeronave
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o cadastro de voos
@app.route('/cadastro_voos')
def cadastro_voos():
    # Busca todas as companhias aéreas para preencher o dropdown
    companhias = Companhia.query.all()
    return render_template('cadastro_voos.html', companhias=companhias)

# Rota para processar o formulário de cadastro de voos
@app.route('/cadastrar_voo', methods=['POST'])
def cadastrar_voo():
    data = request.form

    # Cria um novo voo com os dados do formulário
    novo_voo = Voo(
        numero_voo=data['numero_voo'],
        companhia_id=data['companhia'],
        modelo_aeronave_id=data['modelo_aeronave'],
        tipo_voo=data['tipo_voo'],
        tipo_aeronave=data['tipo_aeronave'],
        qtd_voos=data['qtd_voos'],
        horario_voo=data['horario_voo'],
        qtd_passageiros=data['qtd_passageiros'],
        nota_obj=data.get('nota_obj'),  # Pode ser None se não for preenchido
        nota_pontualidade=data.get('nota_pontualidade'),
        nota_servicos=data.get('nota_servicos'),
        nota_patio=data.get('nota_patio'),
        data_insercao=datetime.utcnow()  # Data de inserção automática
    )

    # Salva o novo voo no banco de dados
    db.session.add(novo_voo)
    db.session.commit()

    return "Voo cadastrado com sucesso!"

# Rota para obter modelos de aeronave com base na companhia selecionada
@app.route('/modelos_aeronave/<int:companhia_id>')
def modelos_aeronave(companhia_id):
    modelos = ModeloAeronave.query.filter_by(companhia_id=companhia_id).all()
    return jsonify([{'id': modelo.id, 'nome': modelo.nome} for modelo in modelos])

# Rota para obter a capacidade de um modelo de aeronave
@app.route('/capacidade_aeronave/<int:modelo_id>')
def capacidade_aeronave(modelo_id):
    modelo = ModeloAeronave.query.get(modelo_id)
    return jsonify(modelo.capacidade)

# Rota para a lista de voos
@app.route('/lista_voos')
def lista_voos():
    # Obtém o filtro de companhia aérea (se existir)
    companhia_filtro = request.args.get('companhia')
    pagina = request.args.get('pagina', 1, type=int)  # Página atual (padrão: 1)
    por_pagina = 10  # Número de voos por página

    # Consulta os voos com ou sem filtro
    if companhia_filtro:
        voos = Voo.query.filter_by(companhia_id=companhia_filtro).paginate(page=pagina, per_page=por_pagina)
    else:
        voos = Voo.query.paginate(page=pagina, per_page=por_pagina)

    # Obtém todas as companhias para o dropdown de filtro
    companhias = Companhia.query.all()

    return render_template('lista_voos.html', voos=voos, companhias=companhias, companhia_filtro=companhia_filtro)

# Rota para a lista de companhias aéreas
@app.route('/companhias')
def companhias():
    companhias = Companhia.query.all()
    return render_template('companhias.html', companhias=companhias)

# Rota para o dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/adicionar_voo', methods=['GET', 'POST'])
def adicionar_voo():
    if request.method == 'POST':
        # Captura os dados do formulário
        novo_voo = Voo(
            numero_voo=request.form['numero_voo'],
            companhia_id=request.form['companhia'],
            modelo_aeronave_id=request.form['modelo_aeronave'],
            tipo_voo=request.form['tipo_voo'],
            tipo_aeronave=request.form['tipo_aeronave'],
            qtd_voos=request.form['qtd_voos'],
            horario_voo=request.form['horario_voo'],
            qtd_passageiros=request.form['qtd_passageiros'],
            nota_obj=request.form.get('nota_obj'),
            nota_pontualidade=request.form.get('nota_pontualidade'),
            nota_servicos=request.form.get('nota_servicos'),
            nota_patio=request.form.get('nota_patio')
        )
        db.session.add(novo_voo)
        db.session.commit()
        return redirect(url_for('lista_voos'))

    companhias = Companhia.query.all()
    return render_template('adicionar_voo.html', companhias=companhias)


@app.route('/editar_voo/<int:id>', methods=['GET', 'POST'])
def editar_voo(id):
    voo = Voo.query.get_or_404(id)

    if request.method == 'POST':
        # Atualiza os dados do voo
        voo.numero_voo = request.form['numero_voo']
        voo.companhia_id = request.form['companhia']
        voo.modelo_aeronave_id = request.form['modelo_aeronave']
        voo.tipo_voo = request.form['tipo_voo']
        voo.tipo_aeronave = request.form['tipo_aeronave']
        voo.qtd_voos = request.form['qtd_voos']
        voo.horario_voo = request.form['horario_voo']
        voo.qtd_passageiros = request.form['qtd_passageiros']
        voo.nota_obj = request.form.get('nota_obj')
        voo.nota_pontualidade = request.form.get('nota_pontualidade')
        voo.nota_servicos = request.form.get('nota_servicos')
        voo.nota_patio = request.form.get('nota_patio')

        db.session.commit()
        return redirect(url_for('lista_voos'))

    companhias = Companhia.query.all()
    return render_template('editar_voo.html', voo=voo, companhias=companhias)

@app.route('/excluir_voo/<int:id>', methods=['POST'])
def excluir_voo(id):
    voo = Voo.query.get_or_404(id)
    db.session.delete(voo)
    db.session.commit()
    return redirect(url_for('lista_voos'))

@app.route('/companhias')
def lista_companhias():
    companhias = Companhia.query.all()
    return render_template('companhias.html', companhias=companhias)

@app.route('/companhia/<int:id>')
def detalhes_companhia(id):
    companhia = Companhia.query.get_or_404(id)

    # Calcula as médias das notas
    voos = companhia.voos
    total_voos = len(voos)

    media_obj = sum(voo.nota_obj for voo in voos if voo.nota_obj is not None) / total_voos if total_voos > 0 else 0
    media_pontualidade = sum(voo.nota_pontualidade for voo in voos if voo.nota_pontualidade is not None) / total_voos if total_voos > 0 else 0
    media_servicos = sum(voo.nota_servicos for voo in voos if voo.nota_servicos is not None) / total_voos if total_voos > 0 else 0
    media_patio = sum(voo.nota_patio for voo in voos if voo.nota_patio is not None) / total_voos if total_voos > 0 else 0
    media_passageiros = sum(voo.qtd_passageiros for voo in voos) / total_voos if total_voos > 0 else 0

    # Modelos de aeronaves utilizados pela companhia
    modelos = companhia.modelos

    return render_template('detalhes_companhia.html', 
                           companhia=companhia, 
                           media_obj=media_obj, 
                           media_pontualidade=media_pontualidade, 
                           media_servicos=media_servicos, 
                           media_patio=media_patio, 
                           modelos=modelos)
    
# Executa a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem
    app.run(debug=True)
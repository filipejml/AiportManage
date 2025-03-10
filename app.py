from flask import Flask, render_template, request, jsonify, url_for, redirect
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

    # Converte campos vazios para None
    nota_servicos = int(data['nota_servicos']) if data['nota_servicos'] else None
    nota_patio = int(data['nota_patio']) if data['nota_patio'] else None
    nota_obj = int(data['nota_obj']) if data['nota_obj'] else None
    nota_pontualidade = int(data['nota_pontualidade']) if data['nota_pontualidade'] else None
    
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
        nota_obj=nota_obj,
        nota_pontualidade=nota_pontualidade,
        nota_servicos=nota_servicos,
        nota_patio=nota_patio,
        data_insercao=datetime.utcnow()  # Data de inserção automática
    )

    # Salva o novo voo no banco de dados
    db.session.add(novo_voo)
    db.session.commit()

    return redirect(url_for('lista_voos'))

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

    for companhia in companhias:
        voos = companhia.voos
        total_voos = len(voos)

        companhia.media_obj = sum(voo.nota_obj for voo in voos if voo.nota_obj is not None) / total_voos if total_voos > 0 else 0
        companhia.media_pontualidade = sum(voo.nota_pontualidade for voo in voos if voo.nota_pontualidade is not None) / total_voos if total_voos > 0 else 0
        companhia.media_servicos = sum(voo.nota_servicos for voo in voos if voo.nota_servicos is not None) / total_voos if total_voos > 0 else 0
        companhia.media_patio = sum(voo.nota_patio for voo in voos if voo.nota_patio is not None) / total_voos if total_voos > 0 else 0

    return render_template('companhias.html', companhias=companhias)

# Rota para o dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Dados gerais (independentes da companhia selecionada)
    total_voos = db.session.query(db.func.sum(Voo.qtd_voos)).scalar() or 0
    total_passageiros = db.session.query(db.func.sum(Voo.qtd_passageiros)).scalar() or 0

    # Médias das notas (geral)
    voos = Voo.query.all()
    total_voos_com_notas = len([voo for voo in voos if voo.nota_obj is not None])

    media_obj = sum(voo.nota_obj for voo in voos if voo.nota_obj is not None) / total_voos_com_notas if total_voos_com_notas > 0 else 0
    media_pontualidade = sum(voo.nota_pontualidade for voo in voos if voo.nota_pontualidade is not None) / total_voos_com_notas if total_voos_com_notas > 0 else 0
    media_servicos = sum(voo.nota_servicos for voo in voos if voo.nota_servicos is not None) / total_voos_com_notas if total_voos_com_notas > 0 else 0
    media_patio = sum(voo.nota_patio for voo in voos if voo.nota_patio is not None) / total_voos_com_notas if total_voos_com_notas > 0 else 0

    # Dados para o gráfico de passageiros por companhia
    companhias = Companhia.query.all()
    passageiros_por_companhia = [
        sum(voo.qtd_passageiros for voo in companhia.voos)
        for companhia in companhias
    ]
    nomes_companhias = [companhia.nome for companhia in companhias]

    # Dados para o gráfico de médias das notas
    medias_notas = [media_obj, media_pontualidade, media_servicos, media_patio]
    labels_notas = ["Objetivo", "Pontualidade", "Serviços", "Pátio"]

    # Total de voos por tipo de aeronave (geral)
    total_voos_pc = db.session.query(db.func.sum(Voo.qtd_voos)).filter(Voo.tipo_aeronave == 'PC').scalar() or 0
    total_voos_mc = db.session.query(db.func.sum(Voo.qtd_voos)).filter(Voo.tipo_aeronave == 'MC').scalar() or 0
    total_voos_lc = db.session.query(db.func.sum(Voo.qtd_voos)).filter(Voo.tipo_aeronave == 'LC').scalar() or 0

    # Total de voos por modelo de aeronave (geral)
    voos_por_modelo = db.session.query(
        ModeloAeronave.nome,
        db.func.sum(Voo.qtd_voos).label('total_voos')
    ).join(Voo, Voo.modelo_aeronave_id == ModeloAeronave.id) \
     .group_by(ModeloAeronave.nome) \
     .all()

    modelos_aeronave = [resultado.nome for resultado in voos_por_modelo]
    total_voos_por_modelo = [resultado.total_voos for resultado in voos_por_modelo]

    # Dados específicos da companhia selecionada
    companhia_selecionada = None
    if request.method == 'POST':
        companhia_id = request.form.get('companhia')
        if companhia_id:
            companhia_selecionada = Companhia.query.get(companhia_id)

            # Total de voos e passageiros da companhia selecionada
            companhia_selecionada.total_voos = sum(voo.qtd_voos for voo in companhia_selecionada.voos)
            companhia_selecionada.total_passageiros = sum(voo.qtd_passageiros for voo in companhia_selecionada.voos)

            # Médias das notas da companhia selecionada
            voos_companhia = companhia_selecionada.voos
            total_voos_companhia = len(voos_companhia)

            companhia_selecionada.media_obj = sum(voo.nota_obj for voo in voos_companhia if voo.nota_obj is not None) / total_voos_companhia if total_voos_companhia > 0 else 0
            companhia_selecionada.media_pontualidade = sum(voo.nota_pontualidade for voo in voos_companhia if voo.nota_pontualidade is not None) / total_voos_companhia if total_voos_companhia > 0 else 0
            companhia_selecionada.media_servicos = sum(voo.nota_servicos for voo in voos_companhia if voo.nota_servicos is not None) / total_voos_companhia if total_voos_companhia > 0 else 0
            companhia_selecionada.media_patio = sum(voo.nota_patio for voo in voos_companhia if voo.nota_patio is not None) / total_voos_companhia if total_voos_companhia > 0 else 0

            # Total de voos por modelo de aeronave da companhia selecionada
            voos_por_modelo_companhia = db.session.query(
                ModeloAeronave.nome,
                db.func.sum(Voo.qtd_voos).label('total_voos')
            ).join(Voo, Voo.modelo_aeronave_id == ModeloAeronave.id) \
             .filter(Voo.companhia_id == companhia_id) \
             .group_by(ModeloAeronave.nome) \
             .all()

            companhia_selecionada.modelos_aeronave = [resultado.nome for resultado in voos_por_modelo_companhia]
            companhia_selecionada.total_voos_por_modelo = [resultado.total_voos for resultado in voos_por_modelo_companhia]

            # Total de passageiros por modelo de aeronave da companhia selecionada
            passageiros_por_modelo_companhia = db.session.query(
                ModeloAeronave.nome,
                db.func.sum(Voo.qtd_passageiros).label('total_passageiros')
            ).join(Voo, Voo.modelo_aeronave_id == ModeloAeronave.id) \
             .filter(Voo.companhia_id == companhia_id) \
             .group_by(ModeloAeronave.nome) \
             .all()

            companhia_selecionada.passageiros_por_modelo = [resultado.total_passageiros for resultado in passageiros_por_modelo_companhia]

            # Total de voos por horário da companhia selecionada
            voos_por_horario_companhia = db.session.query(
                Voo.horario_voo,
                db.func.sum(Voo.qtd_voos).label('total_voos')
            ).filter(Voo.companhia_id == companhia_id) \
             .group_by(Voo.horario_voo) \
             .all()

            companhia_selecionada.horarios_voo = [resultado.horario_voo for resultado in voos_por_horario_companhia]
            companhia_selecionada.total_voos_por_horario = [resultado.total_voos for resultado in voos_por_horario_companhia]

            # Total de passageiros por horário da companhia selecionada
            passageiros_por_horario_companhia = db.session.query(
                Voo.horario_voo,
                db.func.sum(Voo.qtd_passageiros).label('total_passageiros')
            ).filter(Voo.companhia_id == companhia_id) \
             .group_by(Voo.horario_voo) \
             .all()

            companhia_selecionada.passageiros_por_horario = [resultado.total_passageiros for resultado in passageiros_por_horario_companhia]

    return render_template('dashboard.html', 
                           total_voos=total_voos, 
                           total_passageiros=total_passageiros, 
                           media_obj=media_obj, 
                           media_pontualidade=media_pontualidade, 
                           media_servicos=media_servicos, 
                           media_patio=media_patio, 
                           nomes_companhias=nomes_companhias, 
                           passageiros_por_companhia=passageiros_por_companhia, 
                           medias_notas=medias_notas, 
                           labels_notas=labels_notas, 
                           companhias=companhias,
                           total_voos_pc=total_voos_pc,
                           total_voos_mc=total_voos_mc,
                           total_voos_lc=total_voos_lc,
                           modelos_aeronave=modelos_aeronave,
                           total_voos_por_modelo=total_voos_por_modelo,
                           companhia_selecionada=companhia_selecionada,
                           zip=zip)


@app.route('/adicionar_voo', methods=['GET', 'POST'])
def adicionar_voo():
    if request.method == 'POST':
        
        numero_voo = request.form['numero_voo']

        # Verifica se o número do voo já existe
        if Voo.query.filter_by(numero_voo=numero_voo).first():
            flash('Este número de voo já está registrado.', 'error')
            return redirect(url_for('adicionar_voo'))
        
        # Processar o formulário e adicionar o voo
        data = request.form

        # Converte campos vazios para None (NULL no banco de dados)
        nota_obj = int(data['nota_obj']) if data['nota_obj'] else None
        nota_pontualidade = int(data['nota_pontualidade']) if data['nota_pontualidade'] else None
        nota_servicos = int(data['nota_servicos']) if data['nota_servicos'] else None
        nota_patio = int(data['nota_patio']) if data['nota_patio'] else None

        # Cria um novo voo com os dados do formulário
        novo_voo = Voo(
            numero_voo=data['numero_voo'],
            companhia_id=data['companhia'],
            modelo_aeronave_id=data['modelo_aeronave'],
            tipo_voo=data['tipo_voo'],
            tipo_aeronave=data['tipo_aeronave'],
            qtd_voos=int(data['qtd_voos']),
            horario_voo=data['horario_voo'],
            qtd_passageiros=int(data['qtd_passageiros']),
            nota_obj=nota_obj,
            nota_pontualidade=nota_pontualidade,
            nota_servicos=nota_servicos,
            nota_patio=nota_patio,
            data_insercao=datetime.utcnow()  # Data de inserção automática
        )

        # Salva o novo voo no banco de dados
        db.session.add(novo_voo)
        db.session.commit()

        return redirect(url_for('lista_voos'))

    # Se for GET, exibe o formulário
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

@app.route('/verificar_numero_voo/<numero_voo>')
def verificar_numero_voo(numero_voo):
    voo = Voo.query.filter_by(numero_voo=numero_voo).first()
    return jsonify(existe=voo is not None)

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
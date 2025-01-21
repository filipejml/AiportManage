from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configuração do banco de dados
app.config['DB_HOST'] = 'localhost'
app.config['DB_NAME'] = 'airport_manager'
app.config['DB_USER'] = 'postgres'
app.config['DB_PASSWORD'] = '123456789'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD']
    )
    return conn

# Função para converter notas de letra para número
def nota_to_num(nota):
    nota_map = {
        'A': 10,
        'B': 9,
        'C': 8,
        'D': 6,
        'E': 4,
        'F': 2
    }
    return nota_map.get(nota, None)  # Retorna None se a nota não for válida

# Rota para a tela inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastro de voos
@app.route('/cadastro_voos', methods=['GET', 'POST'])
def cadastro_voos():
    if request.method == 'POST':
        numero_voo = request.form['numero_voo']
        companhia_aerea = request.form['companhia_aerea']
        modelo_aviao = request.form['modelo_aviao']
        tipo_voo = request.form['tipo_voo']
        tipo_aeronave = request.form['tipo_aeronave']
        qtd_voos = request.form['qtd_voos']
        horario_voo = request.form['horario_voo']
        qtd_passageiros = request.form['qtd_passageiros']
        
        # Convertendo as notas de letras para números
        nota_obj = nota_to_num(request.form['nota_obj'])
        nota_pontualidade = nota_to_num(request.form['nota_pontualidade'])
        nota_servicos = nota_to_num(request.form['nota_servicos'])
        nota_patio = nota_to_num(request.form['nota_patio'])
        
        # Conectar ao banco de dados e inserir os dados
        conn = get_db_connection()
        cur = conn.cursor()

        query = sql.SQL("""
            INSERT INTO voos (
                numero_voo, companhia_aerea, modelo_aviao, tipo_voo, tipo_aeronave, 
                qtd_voos, horario_voo, qtd_passageiros, nota_obj, nota_pontualidade, 
                nota_servicos, nota_patio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)

        cur.execute(query, (numero_voo, companhia_aerea, modelo_aviao, tipo_voo, tipo_aeronave,
                            qtd_voos, horario_voo, qtd_passageiros, nota_obj, nota_pontualidade,
                            nota_servicos, nota_patio))
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))  # Redireciona para a página inicial após o cadastro

    return render_template('cadastro_voo.html')

# Rota para lista de voos

# Outras rotas como lista_voos, companhias_aereas, etc. são mantidas da mesma forma.

if __name__ == '__main__':
    app.run(debug=True)

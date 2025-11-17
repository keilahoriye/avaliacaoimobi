from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "ndZ46vbXW3AuHGx6g0Dm0GNz8uK6zrxN6rK23498723!@#"

# ====== CONEXÃO COM O POSTGRESQL ======
def conectar():
    return psycopg2.connect(
        host="localhost",
        database="avaliacoes_db",
        user="postgres",
        password="7lz3MB7/"
    )

# ====== HOME / MENU PRINCIPAL ======
@app.route("/")
def index():
    if "id_usuario" in session:

        # cliente → vai para lista de avaliações para responder
        if session["perfil"] == "cliente":
            return redirect(url_for("cliente_avaliacoes"))

        # gestores e admins → menu principal
        return render_template("index.html")
    
    # não logado → página inicial pública
    return render_template("home.html")

# ====== LOGIN ======
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_usuario, nome, email, senha, perfil 
            FROM usuario 
            WHERE email = %s
        """, (email,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()

        # Caso email não exista
        if not usuario:
            flash("Email não encontrado.", "erro")
            return render_template("login.html")

        # Caso senha esteja errada
        if usuario[3] != senha:
            flash("Senha incorreta.", "erro")
            return render_template("login.html")

        # Login OK
        session["id_usuario"] = usuario[0]
        session["nome"] = usuario[1]
        session["perfil"] = usuario[4]

        # Redirecionamento por perfil
        if usuario[4] == "cliente":
            return redirect(url_for("cliente_avaliacoes"))
        elif usuario[4] in ("admin", "gestor"):
            return redirect(url_for("index"))
        elif usuario[4] == "corretor":
            return redirect(url_for("index"))
        else:
            flash("Perfil não reconhecido.", "erro")
            return render_template("login.html")

    # GET — apenas exibe o login
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ====== PROTEÇÃO DE ROTAS ======
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session or session["perfil"] != "admin":
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return wrapper

def corretor_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session or session.get("perfil") != "corretor":
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return wrapper

def perfil_requerido(*perfis):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "id_usuario" not in session:
                return redirect(url_for("login"))

            if session.get("perfil") not in perfis:
                return "Acesso negado: você não tem permissão para acessar esta página.", 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ====== USUÁRIOS ======
@app.route("/usuarios")
@perfil_requerido("admin")
def listar_usuarios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nome, email, telefone, perfil FROM usuario ORDER BY id_usuario;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/criar", methods=["GET", "POST"])
@perfil_requerido("admin")
def criar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        perfil = request.form["perfil"]

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuario (nome, email, telefone, senha, perfil)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, email, telefone, senha, perfil))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_usuarios"))

    return render_template("criar_usuario.html")

@app.route("/usuarios/editar/<int:id_usuario>", methods=["GET", "POST"])
@perfil_requerido("admin")
def editar_usuario(id_usuario):
    conn = conectar()
    cur = conn.cursor()

    # Buscar dados atuais do usuário
    cur.execute("SELECT id_usuario, nome, email, telefone, senha, perfil FROM usuario WHERE id_usuario = %s", 
                (id_usuario,))
    usuario = cur.fetchone()

    if not usuario:
        flash("Usuário não encontrado.", "erro")
        cur.close()
        conn.close()
        return redirect(url_for("listar_usuarios"))

    perfil_atual = usuario[5]

    # ===== POST: salvar edição =====
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        novo_perfil = request.form["perfil"]

        # === Se o perfil está mudando de admin → outro perfil, verificar se é o último admin ===
        if perfil_atual == "admin" and novo_perfil != "admin":
            cur.execute("SELECT COUNT(*) FROM usuario WHERE perfil = 'admin'")
            qtd_admin = cur.fetchone()[0]

            if qtd_admin <= 1:
                flash("Não é possível alterar o perfil do único administrador do sistema.", "erro")
                cur.close()
                conn.close()
                return redirect(url_for("listar_usuarios"))

        # === Atualizar usuário ===
        cur.execute("""
            UPDATE usuario
            SET nome = %s, email = %s, telefone = %s, senha = %s, perfil = %s
            WHERE id_usuario = %s
        """, (nome, email, telefone, senha, novo_perfil, id_usuario))

        conn.commit()
        cur.close()
        conn.close()

        flash("Usuário atualizado com sucesso!", "sucesso")
        return redirect(url_for("listar_usuarios"))

    cur.close()
    conn.close()

    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/usuarios/deletar/<int:id_usuario>")
@perfil_requerido("admin")
def deletar_usuario(id_usuario):
    conn = conectar()
    cur = conn.cursor()

    # === 1) Verificar perfil do usuário a ser deletado ===
    cur.execute("SELECT perfil FROM usuario WHERE id_usuario = %s", (id_usuario,))
    resultado = cur.fetchone()

    # Se não encontrou o usuário
    if not resultado:
        flash("Usuário não encontrado.", "erro")
        cur.close()
        conn.close()
        return redirect(url_for("listar_usuarios"))

    perfil = resultado[0]

    # === 2) Se for admin, verificar se é o ÚNICO ===
    if perfil == "admin":
        cur.execute("SELECT COUNT(*) FROM usuario WHERE perfil = 'admin'")
        qtd_admin = cur.fetchone()[0]

        if qtd_admin <= 1:
            flash("Não é possível deletar o único administrador do sistema.", "erro")
            cur.close()
            conn.close()
            return redirect(url_for("listar_usuarios"))

    # === 3) Se chegou aqui, pode deletar ===
    cur.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
    conn.commit()

    cur.close()
    conn.close()

    flash("Usuário deletado com sucesso.", "sucesso")
    return redirect(url_for("listar_usuarios"))

# ====== AVALIAÇÕES ======
@app.route("/avaliacoes")
@perfil_requerido("admin", "gestor")
def listar_avaliacoes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id_avaliacao, a.nome, t.nome_tipo, a.descricao, u.nome
        FROM avaliacao a
        LEFT JOIN tipo_avaliacao t ON a.id_tipo_avaliacao = t.id_tipo_avaliacao
        LEFT JOIN usuario u ON a.id_gestor = u.id_usuario
        ORDER BY a.id_avaliacao;
    """)
    avaliacoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("avaliacoes.html", avaliacoes=avaliacoes)

@app.route("/avaliacoes/criar", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def criar_avaliacao():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_tipo_avaliacao, nome_tipo FROM tipo_avaliacao ORDER BY id_tipo_avaliacao;")
    tipos = cur.fetchall()
    cur.execute("SELECT id_usuario, nome FROM usuario WHERE perfil = 'gestor' ORDER BY nome;")
    gestores = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        id_tipo_avaliacao = request.form["id_tipo_avaliacao"]
        id_gestor = request.form["id_gestor"]

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO avaliacao (nome, descricao, id_tipo_avaliacao, id_gestor, data_criacao)
            VALUES (%s, %s, %s, %s, CURRENT_DATE)
        """, (nome, descricao, id_tipo_avaliacao, id_gestor))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_avaliacoes"))

    return render_template("criar_avaliacao.html", tipos=tipos, gestores=gestores)


@app.route("/avaliacoes/editar/<int:id_avaliacao>", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def editar_avaliacao(id_avaliacao):
    conn = conectar()
    cur = conn.cursor()

    # Buscar gestores e tipos de avaliação
    cur.execute("SELECT id_usuario, nome FROM usuario WHERE perfil = 'gestor' ORDER BY id_usuario;")
    gestores = cur.fetchall()
    cur.execute("SELECT id_tipo_avaliacao, nome_tipo FROM tipo_avaliacao ORDER BY id_tipo_avaliacao;")
    tipos = cur.fetchall()

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        id_tipo_avaliacao = request.form["id_tipo_avaliacao"]
        id_gestor = request.form["id_gestor"]

        cur.execute("""
            UPDATE avaliacao
            SET nome = %s, descricao = %s, id_tipo_avaliacao = %s, id_gestor = %s
            WHERE id_avaliacao = %s
        """, (nome, descricao, id_tipo_avaliacao, id_gestor, id_avaliacao))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_avaliacoes"))

    # Buscar dados da avaliação
    cur.execute("""
        SELECT id_avaliacao, nome, descricao, id_tipo_avaliacao, id_gestor
        FROM avaliacao WHERE id_avaliacao = %s
    """, (id_avaliacao,))
    avaliacao = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("editar_avaliacao.html", avaliacao=avaliacao, gestores=gestores, tipos=tipos)

@app.route("/avaliacoes/deletar/<int:id_avaliacao>")
@perfil_requerido("admin", "gestor")
def deletar_avaliacao(id_avaliacao):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM avaliacao WHERE id_avaliacao = %s", (id_avaliacao,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("listar_avaliacoes"))

# ====== TIPOS DE AVALIAÇÃO ======
@app.route("/tipos_avaliacao")
@perfil_requerido("admin", "gestor")
def listar_tipos_avaliacao():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_tipo_avaliacao, nome_tipo, descricao FROM tipo_avaliacao ORDER BY id_tipo_avaliacao;")
    tipos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("listar_tipos_avaliacao.html", tipos=tipos)

@app.route("/tipos_avaliacao/criar", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def criar_tipo_avaliacao():
    if request.method == "POST":
        nome_tipo = request.form["nome_tipo"]
        descricao = request.form.get("descricao")

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tipo_avaliacao (nome_tipo, descricao)
            VALUES (%s, %s)
        """, (nome_tipo, descricao))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_tipos_avaliacao"))

    return render_template("criar_tipo_avaliacao.html")


@app.route("/tipos_avaliacao/editar/<int:id_tipo_avaliacao>", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def editar_tipo_avaliacao(id_tipo_avaliacao):
    conn = conectar()
    cur = conn.cursor()

    if request.method == "POST":
        nome_tipo = request.form["nome_tipo"]
        descricao = request.form.get("descricao")
        cur.execute("""
            UPDATE tipo_avaliacao
            SET nome_tipo = %s, descricao = %s
            WHERE id_tipo_avaliacao = %s
        """, (nome_tipo, descricao, id_tipo_avaliacao))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_tipos_avaliacao"))

    cur.execute("SELECT * FROM tipo_avaliacao WHERE id_tipo_avaliacao = %s;", (id_tipo_avaliacao,))
    tipo = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("editar_tipo_avaliacao.html", tipo=tipo)


@app.route("/tipos_avaliacao/deletar/<int:id_tipo_avaliacao>")
@perfil_requerido("admin", "gestor")
def deletar_tipo_avaliacao(id_tipo_avaliacao):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM tipo_avaliacao WHERE id_tipo_avaliacao = %s;", (id_tipo_avaliacao,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("listar_tipos_avaliacao"))

# ====== TIPOS DE QUESTÃO ======
@app.route("/tipos")
@perfil_requerido("admin", "gestor")
def listar_tipos_questao():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_tipo, nome_tipo, descricao, opcoes FROM tipo_questao ORDER BY id_tipo;")
    tipos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("listar_tipos_questao.html", tipos=tipos)

@app.route("/tipos/criar", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def criar_tipo_questao():
    if request.method == "POST":
        nome_tipo = request.form["nome_tipo"]
        descricao = request.form.get("descricao")
        tipo_resposta = request.form["tipo_resposta"]
        opcoes = request.form.get("opcoes") if tipo_resposta == "multipla" else None

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tipo_questao (nome_tipo, descricao, opcoes)
            VALUES (%s, %s, %s)
        """, (nome_tipo, descricao, opcoes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_tipos_questao"))

    return render_template("criar_tipo_questao.html")

@app.route("/tipos/editar/<int:id_tipo>", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def editar_tipo_questao(id_tipo):
    conn = conectar()
    cur = conn.cursor()

    if request.method == "POST":
        nome_tipo = request.form["nome_tipo"]
        descricao = request.form.get("descricao")
        opcoes = request.form.get("opcoes")

        cur.execute("""
            UPDATE tipo_questao
            SET nome_tipo = %s, descricao = %s, opcoes = %s
            WHERE id_tipo = %s
        """, (nome_tipo, descricao, opcoes, id_tipo))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_tipos_questao"))

    cur.execute("SELECT id_tipo, nome_tipo, descricao, opcoes FROM tipo_questao WHERE id_tipo = %s", (id_tipo,))
    tipo = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("editar_tipo_questao.html", tipo=tipo)

@app.route("/tipos/deletar/<int:id_tipo>")
@perfil_requerido("admin", "gestor")
def deletar_tipo_questao(id_tipo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM tipo_questao WHERE id_tipo = %s", (id_tipo,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("listar_tipos_questao"))

# ====== QUESTÕES ======
@app.route("/questoes")
@perfil_requerido("admin", "gestor")
def listar_questoes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id_questao, q.texto, a.nome, t.nome_tipo
        FROM questao q
        JOIN avaliacao a ON q.id_avaliacao = a.id_avaliacao
        JOIN tipo_questao t ON q.id_tipo = t.id_tipo
        ORDER BY q.id_questao;
    """)
    questoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("questoes.html", questoes=questoes)

@app.route("/questoes/criar", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def criar_questao():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_avaliacao, nome FROM avaliacao ORDER BY id_avaliacao;")
    avaliacoes = cur.fetchall()
    cur.execute("SELECT id_tipo, nome_tipo FROM tipo_questao ORDER BY id_tipo;")
    tipos = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == "POST":
        id_avaliacao = request.form["id_avaliacao"]
        id_tipo = request.form["id_tipo"]
        texto = request.form["texto"]

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO questao (texto, id_avaliacao, id_tipo)
            VALUES (%s, %s, %s)
        """, (texto, id_avaliacao, id_tipo))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_questoes"))

    return render_template("criar_questao.html", avaliacoes=avaliacoes, tipos=tipos)

@app.route("/questoes/editar/<int:id_questao>", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def editar_questao(id_questao):
    conn = conectar()
    cur = conn.cursor()

    # Buscar avaliações e tipos de questão (para o select)
    cur.execute("SELECT id_avaliacao, nome FROM avaliacao ORDER BY id_avaliacao;")
    avaliacoes = cur.fetchall()
    cur.execute("SELECT id_tipo, nome_tipo FROM tipo_questao ORDER BY id_tipo;")
    tipos = cur.fetchall()

    if request.method == "POST":
        texto = request.form["texto"]
        id_avaliacao = request.form["id_avaliacao"]
        id_tipo = request.form["id_tipo"]

        cur.execute("""
            UPDATE questao
            SET texto = %s, id_avaliacao = %s, id_tipo = %s
            WHERE id_questao = %s
        """, (texto, id_avaliacao, id_tipo, id_questao))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("listar_questoes"))

    cur.execute("""
        SELECT id_questao, texto, id_avaliacao, id_tipo
        FROM questao WHERE id_questao = %s
    """, (id_questao,))
    questao = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("editar_questao.html", questao=questao, avaliacoes=avaliacoes, tipos=tipos)

@app.route("/questoes/deletar/<int:id_questao>")
@perfil_requerido("admin", "gestor")
def deletar_questao(id_questao):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM questao WHERE id_questao = %s", (id_questao,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("listar_questoes"))


# ====== RESPONDER AVALIAÇÃO ======
@app.route("/avaliacoes/<int:id_avaliacao>/responder", methods=["GET", "POST"])
@perfil_requerido("cliente")
def responder_avaliacao(id_avaliacao):
    conn = conectar()
    cur = conn.cursor()

    id_cliente = session["id_usuario"]  # cliente logado

    # ========= GET =========
    if request.method == "GET":
        # lista os corretores
        cur.execute("""
            SELECT id_usuario, nome 
            FROM usuario 
            WHERE perfil = 'corretor'
            ORDER BY nome;
        """)
        corretores = cur.fetchall()

        cur.close()
        conn.close()
        
        return render_template(
            "responder_avaliacao.html",
            id_avaliacao=id_avaliacao,
            id_cliente=id_cliente,
            corretores=corretores
        )

    # ========= POST =========

    id_corretor = request.form["id_corretor"]

    # verifica se já respondeu para esse corretor
    cur.execute("""
        SELECT id_form FROM formulario_respondido
        WHERE id_avaliacao = %s AND id_cliente = %s AND id_corretor = %s
    """, (id_avaliacao, id_cliente, id_corretor))

    ja_respondeu = cur.fetchone()

    if ja_respondeu:
        cur.close()
        conn.close()
        flash("Você já respondeu esta avaliação para este corretor.", "erro")
        return redirect(url_for("cliente_avaliacoes"))

    # insere formulário
    cur.execute("""
        INSERT INTO formulario_respondido (id_avaliacao, id_cliente, id_corretor, data_resposta)
        VALUES (%s, %s, %s, CURRENT_DATE)
        RETURNING id_form
    """, (id_avaliacao, id_cliente, id_corretor))

    id_form = cur.fetchone()[0]
    conn.commit()

    # salva respostas
    for key, value in request.form.items():
        if key.startswith("resposta_texto_"):
            id_questao = key.replace("resposta_texto_", "")
            cur.execute("""
                INSERT INTO resposta (id_form, id_questao, resposta_texto)
                VALUES (%s, %s, %s)
            """, (id_form, id_questao, value))

        elif key.startswith("resposta_numero_"):
            id_questao = key.replace("resposta_numero_", "")
            cur.execute("""
                INSERT INTO resposta (id_form, id_questao, resposta_numero)
                VALUES (%s, %s, %s)
            """, (id_form, id_questao, value))

    conn.commit()
    cur.close()
    conn.close()

    flash("Resposta enviada com sucesso!", "sucesso")
    return redirect(url_for("cliente_avaliacoes"))

# rota JSON para questões (usada no front-end para gerar select)
@app.route("/avaliacoes/<int:id_avaliacao>/questoes/json")
@perfil_requerido("admin", "gestor", "cliente")
def questoes_json(id_avaliacao):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id_questao, q.texto, t.nome_tipo, t.opcoes
        FROM questao q
        JOIN tipo_questao t ON q.id_tipo = t.id_tipo
        WHERE q.id_avaliacao = %s
        ORDER BY q.id_questao;
    """, (id_avaliacao,))
    questoes = cur.fetchall()
    cur.close()
    conn.close()

    questoes_list = []
    for q in questoes:
        opcoes = q[3].split(",") if q[3] else []
        questoes_list.append({
            "id_questao": q[0],
            "texto": q[1],
            "nome_tipo": q[2],
            "opcoes": opcoes
        })
    return jsonify(questoes_list)

@app.route("/cliente/avaliacoes")
@perfil_requerido("cliente")
def cliente_avaliacoes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_avaliacao, nome, descricao
        FROM avaliacao
        ORDER BY id_avaliacao;
    """)
    avaliacoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("cliente_avaliacoes.html", avaliacoes=avaliacoes)

# ====== FORMULÁRIOS RESPONDIDOS ======
@app.route("/formularios")
@perfil_requerido("admin", "gestor")
def formularios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id_form, a.nome, u1.nome, u2.nome, f.data_resposta
        FROM formulario_respondido f
        JOIN avaliacao a ON f.id_avaliacao = a.id_avaliacao
        JOIN usuario u1 ON f.id_cliente = u1.id_usuario
        JOIN usuario u2 ON f.id_corretor = u2.id_usuario
        ORDER BY f.id_form;
    """)
    formularios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("formularios.html", formularios=formularios)

@app.route("/formularios/<int:id_form>")
@perfil_requerido("admin", "gestor")
def listar_respostas(id_form):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id_resposta, r.id_questao, q.texto, r.resposta_texto, r.resposta_numero
        FROM resposta r
        JOIN questao q ON r.id_questao = q.id_questao
        WHERE r.id_form = %s
        ORDER BY r.id_resposta;
    """, (id_form,))
    respostas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("respostas.html", respostas=respostas, id_form=id_form)

@app.route("/respostas/editar/<int:id_resposta>", methods=["GET", "POST"])
@perfil_requerido("admin", "gestor")
def editar_resposta(id_resposta):
    conn = conectar()
    cur = conn.cursor()

    if request.method == "POST":
        resposta_texto = request.form.get("resposta_texto")
        resposta_numero = request.form.get("resposta_numero")

        if resposta_texto:
            cur.execute("""
                UPDATE resposta
                SET resposta_texto = %s, resposta_numero = NULL
                WHERE id_resposta = %s
            """, (resposta_texto, id_resposta))
        else:
            cur.execute("""
                UPDATE resposta
                SET resposta_numero = %s, resposta_texto = NULL
                WHERE id_resposta = %s
            """, (resposta_numero, id_resposta))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("formularios"))

    # GET – carrega os dados atuais da resposta
    cur.execute("""
        SELECT r.id_resposta, q.texto, r.resposta_texto, r.resposta_numero
        FROM resposta r
        JOIN questao q ON r.id_questao = q.id_questao
        WHERE r.id_resposta = %s
    """, (id_resposta,))
    resposta = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("editar_resposta.html", resposta=resposta)


@app.route("/respostas/deletar/<int:id_resposta>")
@perfil_requerido("admin", "gestor")
def deletar_resposta(id_resposta):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM resposta WHERE id_resposta = %s", (id_resposta,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("formularios"))

@app.route("/formularios/deletar/<int:id_form>")
@perfil_requerido("admin", "gestor")
def deletar_formulario(id_form):
    conn = conectar()
    cur = conn.cursor()

    # Apaga respostas primeiro (por causa da FK)
    cur.execute("DELETE FROM resposta WHERE id_form = %s", (id_form,))
    conn.commit()

    # Depois apaga o formulário
    cur.execute("DELETE FROM formulario_respondido WHERE id_form = %s", (id_form,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("formularios"))

# ====== RODAR O FLASK ======
if __name__ == "__main__":
    app.run(debug=True)
import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="avaliacoes_db",
        user="postgres",
        password="7lz3MB7/"
    )

def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    senha = input("Senha: ")
    perfil = input("Perfil (cliente, corretor, gestor, admin): ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuario (nome, email, telefone, senha, perfil)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, email, telefone, senha, perfil))
    conn.commit()
    cur.close()
    conn.close()
    print("\nUsuário cadastrado com sucesso!\n")

def listar_usuarios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nome, email, telefone, perfil FROM usuario ORDER BY id_usuario;")
    usuarios = cur.fetchall()

    if not usuarios:
        print("\nNenhum usuário cadastrado.\n")
    else:
        print("\n=== Lista de Usuários ===")
        for u in usuarios:
            print(f"ID: {u[0]} | Nome: {u[1]} | Email: {u[2]} | Telefone: {u[3]} | Perfil: {u[4]}")
        print("=========================\n")

    cur.close()
    conn.close()

def editar_usuario():
    listar_usuarios()
    id_usuario = input("Digite o ID do usuário que deseja editar: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
    usuario = cur.fetchone()

    if not usuario:
        print("\nUsuário não encontrado.\n")
        cur.close()
        conn.close()
        return

    print("\nDeixe em branco o que não quiser alterar.\n")

    nome = input(f"Novo nome ({usuario[1]}): ") or usuario[1]
    email = input(f"Novo email ({usuario[2]}): ") or usuario[2]
    telefone = input(f"Novo telefone ({usuario[3]}): ") or usuario[3]
    senha = input(f"Nova senha ({usuario[4]}): ") or usuario[4]
    perfil = input(f"Novo perfil ({usuario[5]}): ") or usuario[5]

    cur.execute("""
        UPDATE usuario
        SET nome = %s, email = %s, telefone = %s, senha = %s, perfil = %s
        WHERE id_usuario = %s
    """, (nome, email, telefone, senha, perfil, id_usuario))
    conn.commit()
    cur.close()
    conn.close()

    print("\nUsuário atualizado com sucesso!\n")

def deletar_usuario():
    listar_usuarios()
    id_usuario = input("Digite o ID do usuário que deseja deletar: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
    usuario = cur.fetchone()

    if not usuario:
        print("\nUsuário não encontrado.\n")
    else:
        confirm = input(f"Tem certeza que deseja excluir o usuário '{usuario[1]}'? (s/n): ")
        if confirm.lower() == "s":
            cur.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            print("\nUsuário excluído com sucesso!\n")
        else:
            print("\nOperação cancelada.\n")

    cur.close()
    conn.close()

def criar_avaliacao():
    nome = input("Nome da avaliação: ")
    tipo = input("Tipo da avaliação: ")
    descricao = input("Descrição: ")
    id_gestor = input("ID do gestor responsável: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO avaliacao (nome, tipo, descricao, data_criacao, id_gestor)
        VALUES (%s, %s, %s, CURRENT_DATE, %s)
    """, (nome, tipo, descricao, id_gestor))
    conn.commit()
    cur.close()
    conn.close()
    print("\nAvaliação criada com sucesso!\n")

def listar_avaliacoes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_avaliacao, nome, tipo, descricao, data_criacao, id_gestor FROM avaliacao ORDER BY id_avaliacao;")
    avaliacoes = cur.fetchall()

    if not avaliacoes:
        print("\nNenhuma avaliação encontrada.\n")
    else:
        print("\n=== Lista de Avaliações ===")
        for a in avaliacoes:
            print(f"ID: {a[0]} | Nome: {a[1]} | Tipo: {a[2]} | Gestor ID: {a[5]}")
        print("=============================\n")

    cur.close()
    conn.close()

def editar_avaliacao():
    listar_avaliacoes()
    id_avaliacao = input("Digite o ID da avaliação que deseja editar: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM avaliacao WHERE id_avaliacao = %s", (id_avaliacao,))
    avaliacao = cur.fetchone()

    if not avaliacao:
        print("\nAvaliação não encontrada.\n")
        cur.close()
        conn.close()
        return

    print("\nDeixe em branco o que não quiser alterar.\n")

    nome = input(f"Novo nome ({avaliacao[1]}): ") or avaliacao[1]
    tipo = input(f"Novo tipo ({avaliacao[2]}): ") or avaliacao[2]
    descricao = input(f"Nova descrição ({avaliacao[3]}): ") or avaliacao[3]
    id_gestor = input(f"Novo ID do gestor ({avaliacao[5]}): ") or avaliacao[5]

    cur.execute("""
        UPDATE avaliacao
        SET nome = %s, tipo = %s, descricao = %s, id_gestor = %s
        WHERE id_avaliacao = %s
    """, (nome, tipo, descricao, id_gestor, id_avaliacao))
    conn.commit()
    cur.close()
    conn.close()

    print("\nAvaliação atualizada com sucesso!\n")

def deletar_avaliacao():
    listar_avaliacoes()
    id_avaliacao = input("Digite o ID da avaliação que deseja deletar: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM avaliacao WHERE id_avaliacao = %s", (id_avaliacao,))
    avaliacao = cur.fetchone()

    if not avaliacao:
        print("\nAvaliação não encontrada.\n")
    else:
        confirm = input(f"Tem certeza que deseja excluir a avaliação '{avaliacao[0]}' e suas respostas? (s/n): ")
        if confirm.lower() == "s":
            cur.execute("DELETE FROM avaliacao WHERE id_avaliacao = %s", (id_avaliacao,))
            conn.commit()
            print("\nAvaliação e dados relacionados foram excluídos!\n")
        else:
            print("\nOperação cancelada.\n")

    cur.close()
    conn.close()

def criar_tipo_questao():
    nome_tipo = input("Nome do tipo de questão (ex: 'Escala 0-10', 'Texto livre', 'Sim/Não'): ")
    descricao = input("Descrição do tipo: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tipo_questao (nome_tipo, descricao)
        VALUES (%s, %s)
    """, (nome_tipo, descricao))
    conn.commit()
    cur.close()
    conn.close()

    print("\nTipo de questão criado com sucesso!\n")

def listar_tipos_questao():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_tipo, nome_tipo, descricao FROM tipo_questao ORDER BY id_tipo;")
    tipos = cur.fetchall()

    if not tipos:
        print("\nNenhum tipo de questão cadastrado.\n")
    else:
        print("\n=== Tipos de Questão ===")
        for t in tipos:
            print(f"ID: {t[0]} | Tipo: {t[1]} | Descrição: {t[2]}")
        print("========================\n")

    cur.close()
    conn.close()

def editar_tipo_questao():
    listar_tipos_questao()
    id_tipo = input("Digite o ID do tipo de questão que deseja editar: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tipo_questao WHERE id_tipo = %s", (id_tipo,))
    tipo = cur.fetchone()

    if not tipo:
        print("\nTipo de questão não encontrado.\n")
        cur.close()
        conn.close()
        return

    nome_tipo = input(f"Novo nome ({tipo[1]}): ") or tipo[1]
    descricao = input(f"Nova descrição ({tipo[2] or 'vazio'}): ") or tipo[2]

    cur.execute("""
        UPDATE tipo_questao
        SET nome_tipo = %s, descricao = %s
        WHERE id_tipo = %s
    """, (nome_tipo, descricao, id_tipo))
    conn.commit()
    cur.close()
    conn.close()
    print("\nTipo de questão atualizado com sucesso!\n")

def deletar_tipo_questao():
    listar_tipos_questao()
    id_tipo = input("Digite o ID do tipo de questão que deseja deletar: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome_tipo FROM tipo_questao WHERE id_tipo = %s", (id_tipo,))
    tipo = cur.fetchone()

    if not tipo:
        print("\nTipo de questão não encontrado.\n")
    else:
        confirm = input(f"Tem certeza que deseja excluir o tipo '{tipo[0]}'? (s/n): ")
        if confirm.lower() == "s":
            try:
                cur.execute("DELETE FROM tipo_questao WHERE id_tipo = %s", (id_tipo,))
                conn.commit()
                print("\nTipo de questão excluído com sucesso!\n")
            except Exception as e:
                print("\nErro ao excluir o tipo de questão:", e, "\n")
        else:
            print("\nOperação cancelada.\n")

    cur.close()
    conn.close()

def criar_questao():
    listar_avaliacoes()
    id_avaliacao = input("Digite o ID da avaliação para adicionar questões: ")

    listar_tipos_questao()
    id_tipo = input("Digite o ID do tipo de questão: ")

    texto = input("Digite o texto da questão: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questao (texto, id_avaliacao, id_tipo)
        VALUES (%s, %s, %s)
    """, (texto, id_avaliacao, id_tipo))
    conn.commit()
    cur.close()
    conn.close()

    print("\nQuestão criada com sucesso!\n")

def listar_questoes_por_avaliacao():
    listar_avaliacoes()
    id_avaliacao = input("Digite o ID da avaliação: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id_questao, q.texto, t.nome_tipo
        FROM questao q
        JOIN tipo_questao t ON q.id_tipo = t.id_tipo
        WHERE q.id_avaliacao = %s
        ORDER BY q.id_questao;
    """, (id_avaliacao,))
    questoes = cur.fetchall()

    if not questoes:
        print("\nNenhuma questão encontrada para esta avaliação.\n")
    else:
        print("\n=== Questões da Avaliação ===")
        for q in questoes:
            print(f"ID: {q[0]} | Tipo: {q[2]} | Texto: {q[1]}")
        print("==============================\n")

    cur.close()
    conn.close()

def editar_questao():
    listar_avaliacoes()
    id_avaliacao = input("Digite o ID da avaliação que contém a questão: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id_questao, q.texto, t.id_tipo, t.nome_tipo
        FROM questao q
        JOIN tipo_questao t ON q.id_tipo = t.id_tipo
        WHERE q.id_avaliacao = %s
        ORDER BY q.id_questao;
    """, (id_avaliacao,))
    questoes = cur.fetchall()

    if not questoes:
        print("\nNenhuma questão encontrada para esta avaliação.\n")
        cur.close()
        conn.close()
        return

    print("\n=== Questões da Avaliação ===")
    for q in questoes:
        print(f"ID: {q[0]} | TipoID: {q[2]} ({q[3]}) | Texto: {q[1]}")
    print("==============================\n")

    id_questao = input("Digite o ID da questão que deseja editar: ")

    cur.execute("SELECT id_questao, texto, id_tipo FROM questao WHERE id_questao = %s", (id_questao,))
    questao = cur.fetchone()

    if not questao:
        print("\nQuestão não encontrada.\n")
        cur.close()
        conn.close()
        return

    print("\nDeixe em branco o que não quiser alterar.\n")
    novo_texto = input(f"Novo texto ({questao[1]}): ") or questao[1]

    listar_tipos_questao()
    novo_id_tipo = input(f"Novo ID do tipo (atual {questao[2]}): ") or str(questao[2])

    cur.execute("""
        UPDATE questao
        SET texto = %s, id_tipo = %s
        WHERE id_questao = %s
    """, (novo_texto, novo_id_tipo, id_questao))
    conn.commit()
    cur.close()
    conn.close()
    print("\nQuestão atualizada com sucesso!\n")


def deletar_questao():
    listar_avaliacoes()
    id_avaliacao = input("Digite o ID da avaliação que contém a questão: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id_questao, q.texto
        FROM questao q
        WHERE q.id_avaliacao = %s
        ORDER BY q.id_questao;
    """, (id_avaliacao,))
    questoes = cur.fetchall()

    if not questoes:
        print("\nNenhuma questão encontrada para esta avaliação.\n")
        cur.close()
        conn.close()
        return

    print("\n=== Questões da Avaliação ===")
    for q in questoes:
        print(f"ID: {q[0]} | Texto: {q[1]}")
    print("==============================\n")

    id_questao = input("Digite o ID da questão que deseja deletar: ")

    cur.execute("SELECT texto FROM questao WHERE id_questao = %s", (id_questao,))
    questao = cur.fetchone()

    if not questao:
        print("\nQuestão não encontrada.\n")
    else:
        confirm = input(f"Tem certeza que deseja excluir a questão '{questao[0]}'? (s/n): ")
        if confirm.lower() == "s":
            try:
                cur.execute("DELETE FROM questao WHERE id_questao = %s", (id_questao,))
                conn.commit()
                print("\nQuestão excluída com sucesso!\n")
            except Exception as e:
                print("\nNão foi possível excluir a questão. Pode haver respostas vinculadas a ela.\nErro:", e, "\n")
        else:
            print("\nOperação cancelada.\n")

    cur.close()
    conn.close()

def responder_avaliacao():
    listar_avaliacoes()
    id_avaliacao = input("Escolha o ID da avaliação: ")

    listar_usuarios()
    id_cliente = input("Digite o ID do cliente: ")

    listar_usuarios()
    id_corretor = input("Digite o ID do corretor: ")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO formulario_respondido (id_avaliacao, id_cliente, id_corretor, data_resposta)
        VALUES (%s, %s, %s, CURRENT_DATE)
        RETURNING id_form
    """, (id_avaliacao, id_cliente, id_corretor))
    id_form = cur.fetchone()[0]

    conn.commit()

    cur.execute("""
        SELECT id_questao, texto, id_tipo
        FROM questao
        WHERE id_avaliacao = %s
        ORDER BY id_questao;
    """, (id_avaliacao,))
    questoes = cur.fetchall()

    if not questoes:
        print("\nEsta avaliação ainda não possui questões cadastradas.\n")
        cur.close()
        conn.close()
        return
    
    questoes_restantes = list(questoes)

    while questoes_restantes:
        print("\n=== Questões restantes ===")
        for q in questoes_restantes:
            print(f"ID {q[0]}: {q[1]}")
        print("==========================\n")

        id_questao = input("Digite o ID da questão que deseja responder (ou 0 para sair): ")
        if id_questao == "0":
            break

        questao = next((q for q in questoes_restantes if str(q[0]) == id_questao), None)
        if not questao:
            print("Essa questão não pertence à avaliação atual ou já foi respondida.\n")
            continue

        print(f"\nQuestão selecionada:\n→ {questao[1]}\n")

        tipo = input("A resposta é texto (t) ou número (n)? ")

        if tipo.lower() == "t":
            resposta_texto = input("Digite sua resposta: ")
            cur.execute("""
                INSERT INTO resposta (id_form, id_questao, resposta_texto)
                VALUES (%s, %s, %s)
            """, (id_form, id_questao, resposta_texto))
        else:
            resposta_numero = float(input("Digite a nota (0 a 10): "))
            cur.execute("""
                INSERT INTO resposta (id_form, id_questao, resposta_numero)
                VALUES (%s, %s, %s)
            """, (id_form, id_questao, resposta_numero))

        conn.commit()
        questoes_restantes = [q for q in questoes_restantes if str(q[0]) != id_questao]
        print("\n✅ Resposta registrada!\n")

    print("\nTodas as respostas foram salvas!\n")
    cur.close()
    conn.close()

def listar_formularios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id_form, a.nome AS nome_avaliacao, u1.nome AS cliente, u2.nome AS corretor, f.data_resposta
        FROM formulario_respondido f
        JOIN avaliacao a ON f.id_avaliacao = a.id_avaliacao
        JOIN usuario u1 ON f.id_cliente = u1.id_usuario
        JOIN usuario u2 ON f.id_corretor = u2.id_usuario
        ORDER BY f.id_form;
    """)
    formularios = cur.fetchall()

    if not formularios:
        print("\nNenhum formulário respondido encontrado.\n")
    else:
        print("\n=== Formulários Respondidos ===")
        for f in formularios:
            print(f"ID: {f[0]} | Avaliação: {f[1]} | Cliente: {f[2]} | Corretor: {f[3]} | Data: {f[4]}")
        print("===============================\n")

    cur.close()
    conn.close()

def listar_respostas_por_formulario():
    listar_formularios()
    id_form = input("Digite o ID do formulário respondido: ")

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

    if not respostas:
        print("\nNenhuma resposta encontrada para este formulário.\n")
    else:
        print("\n=== Respostas do Formulário ===")
        for r in respostas:
            texto_ou_numero = r[3] if r[3] else r[4]
            print(f"Questão {r[1]}: {r[2]}\n→ Resposta: {texto_ou_numero}\n")
        print("===============================\n")

    cur.close()
    conn.close()

def menu():
    while True:
        print("=== AVALIAÇÃO DA JORNADA DO CLIENTE DA IMOBILIÁRIA ===")
        print("USUÁRIOS")
        print("1. Criar usuário")
        print("2. Listar usuários")
        print("3. Editar usuário")
        print("4. Deletar usuário")
        print("AVALIAÇÕES")
        print("5. Criar avaliação")
        print("6. Listar avaliações")
        print("7. Editar avaliação")
        print("8. Deletar avaliação")
        print("TIPOS DE QUESTÃO")
        print("9. Criar tipo de questão")
        print("10. Listar tipos de questão")
        print("11. Editar tipos de questão")
        print("12. Deletar tipos de questão")
        print("QUESTÕES")
        print("13. Criar questão")
        print("14. Listar questões")
        print("15. Editar questão")
        print("16. Deletar questão")
        print("RESPOSTAS")
        print("17. Responder avaliação")      
        print("18. Listar formulários respondidos")
        print("19. Ver respostas de um formulário")
        print("0. Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            editar_usuario()
        elif opcao == "4":
            deletar_usuario()
        elif opcao == "5":
            criar_avaliacao()
        elif opcao == "6":
            listar_avaliacoes()
        elif opcao == "7":
            deletar_avaliacao()
        elif opcao == "8":
            editar_avaliacao()
        elif opcao == "9":
            criar_tipo_questao()
        elif opcao == "10":
            listar_tipos_questao()
        elif opcao == "11":
            editar_tipo_questao()
        elif opcao == "12":
            deletar_tipo_questao()
        elif opcao == "13":
            criar_questao()
        elif opcao == "14":
            listar_questoes_por_avaliacao()
        elif opcao == "15":
            editar_questao()
        elif opcao == "16":
            deletar_questao()
        elif opcao == "17":
            responder_avaliacao()
        elif opcao == "18":
            listar_formularios()
        elif opcao == "19":
            listar_respostas_por_formulario()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!\n")

menu()
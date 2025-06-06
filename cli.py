from database import DatabaseManager
import argparse


def main():
    parser = argparse.ArgumentParser(description="Gerencia colaboradores e usuarios do sistema")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser("add", help="Adiciona um colaborador")
    add_p.add_argument("nome")
    add_p.add_argument("setor")
    add_p.add_argument("--usuario", default="")
    add_p.add_argument("--foto", default="")

    upd_p = sub.add_parser("update", help="Atualiza um colaborador")
    upd_p.add_argument("id", type=int)
    upd_p.add_argument("--nome")
    upd_p.add_argument("--setor")
    upd_p.add_argument("--usuario")
    upd_p.add_argument("--foto")

    del_p = sub.add_parser("delete", help="Remove um colaborador")
    del_p.add_argument("id", type=int)

    list_p = sub.add_parser("list", help="Lista colaboradores")
    list_p.add_argument("--setor", help="Filtrar por setor")

    show_p = sub.add_parser("show", help="Mostra detalhes de um colaborador")
    show_p.add_argument("id", type=int)

    user_add = sub.add_parser("useradd", help="Adiciona um novo usuario")
    user_add.add_argument("login")
    user_add.add_argument("senha")
    user_add.add_argument("--perfil", default="usuario")

    user_list = sub.add_parser("userlist", help="Lista usuarios")

    user_upd = sub.add_parser("userupdate", help="Atualiza dados de um usuario")
    user_upd.add_argument("id", type=int)
    user_upd.add_argument("--login")
    user_upd.add_argument("--senha")
    user_upd.add_argument("--perfil")

    user_del = sub.add_parser("userdel", help="Remove um usuario")
    user_del.add_argument("id", type=int)

    user_login = sub.add_parser("login", help="Verifica credenciais de usuario")
    user_login.add_argument("login")
    user_login.add_argument("senha")

    client_add = sub.add_parser("clientadd", help="Adiciona um cliente")
    client_add.add_argument("nome")
    client_add.add_argument("--cnpj", default="")

    client_list = sub.add_parser("clientlist", help="Lista clientes")

    client_upd = sub.add_parser("clientupdate", help="Atualiza dados de um cliente")
    client_upd.add_argument("id", type=int)
    client_upd.add_argument("--nome")
    client_upd.add_argument("--cnpj")

    client_del = sub.add_parser("clientdel", help="Remove um cliente")
    client_del.add_argument("id", type=int)

    stock_add = sub.add_parser("stockadd", help="Adiciona quantidade ao estoque")
    stock_add.add_argument("produto")
    stock_add.add_argument("quantidade", type=int)

    stock_out = sub.add_parser("stockout", help="Registra saida do estoque")
    stock_out.add_argument("produto")
    stock_out.add_argument("quantidade", type=int)

    stock_set = sub.add_parser("stockset", help="Define quantidade exata em estoque")
    stock_set.add_argument("produto")
    stock_set.add_argument("quantidade", type=int)

    stock_list = sub.add_parser("stocklist", help="Lista itens do estoque")

    stock_alert = sub.add_parser("stockalert", help="Lista itens com estoque baixo")
    stock_alert.add_argument("limite", type=int)

    disc_add = sub.add_parser("discadd", help="Registra discrepancia de estoque")
    disc_add.add_argument("op_id", type=int)
    disc_add.add_argument("produto")
    disc_add.add_argument("quantidade", type=int)
    disc_add.add_argument("tipo", choices=["adicional", "discrepancia"])

    disc_list = sub.add_parser("disclist", help="Lista discrepancias")
    disc_list.add_argument("--op", type=int, help="Filtrar por OP")

    disc_rep = sub.add_parser("discreport", help="Resumo de discrepancias por OP")
    disc_rep.add_argument("--op", type=int, help="ID da OP para filtrar")

    bud_add = sub.add_parser("budgetadd", help="Cria um orcamento REV00")
    bud_add.add_argument("descricao")
    bud_add.add_argument("--cliente", default="")
    bud_add.add_argument("--motivo", default="")

    bud_rev = sub.add_parser("budgetrev", help="Registra nova revisao")
    bud_rev.add_argument("id", type=int)
    bud_rev.add_argument("motivo")

    bud_list = sub.add_parser("budgetlist", help="Lista orcamentos")
    bud_list.add_argument("--resultado", choices=["aberto", "vendido", "perdido"], help="Filtrar por resultado")
    bud_list.add_argument("--aprovado", type=int, choices=[0,1], help="Filtrar por aprovado 1 ou 0")
    bud_list.add_argument("--cliente", help="Filtrar pelo nome do cliente")

    bud_hist = sub.add_parser("budgethist", help="Mostra historico de revisoes")
    bud_hist.add_argument("id", type=int)

    bud_time = sub.add_parser("budgettime", help="Mostra tempos do orcamento")
    bud_time.add_argument("id", type=int)

    bud_aprov = sub.add_parser("budgetapprove", help="Aprova orcamento e gera OP")
    bud_aprov.add_argument("id", type=int)
    bud_aprov.add_argument("--montador", type=int, help="ID do colaborador montador")

    bud_res = sub.add_parser("budgetresult", help="Atualiza resultado do orcamento")
    bud_res.add_argument("id", type=int)
    bud_res.add_argument("resultado", choices=["vendido", "perdido"])
    bud_res.add_argument("--motivo", default="")
    bud_res.add_argument("--qualificacao", default="")

    kpi_exp = sub.add_parser("kpiexport", help="Exporta dados de orcamentos para JSON")
    kpi_exp.add_argument("arquivo")
    kpi_exp.add_argument("--orcamento", type=int, help="ID do orcamento a exportar")

    ofx_imp = sub.add_parser("ofximport", help="Importa extrato OFX")
    ofx_imp.add_argument("arquivo")

    ofx_list = sub.add_parser("ofxlist", help="Lista transacoes OFX importadas")
    ofx_list.add_argument("--limit", type=int)

    op_add = sub.add_parser("opadd", help="Cria uma ordem de producao")
    op_add.add_argument("descricao")
    op_add.add_argument("--montador", type=int, help="ID do colaborador montador")
    op_add.add_argument("--estimativa", type=float, default=0.0, help="Horas estimadas")

    op_start = sub.add_parser("opstart", help="Inicia a montagem de uma OP")
    op_start.add_argument("id", type=int)

    op_finish = sub.add_parser("opfinish", help="Finaliza a montagem de uma OP")
    op_finish.add_argument("id", type=int)

    op_kpi = sub.add_parser("opkpi", help="Mostra KPI de tempo de uma OP")
    op_kpi.add_argument("id", type=int)

    op_prog = sub.add_parser("opprogress", help="Mostra tempo decorrido de uma OP")
    op_prog.add_argument("id", type=int)

    mont_kpi = sub.add_parser("montkpi", help="Mostra KPI medio de um montador")
    mont_kpi.add_argument("id", type=int)

    op_list = sub.add_parser("oplist", help="Lista ordens de producao")
    op_list.add_argument("--status", help="Filtrar por status")
    op_list.add_argument("--montador", type=int, help="Filtrar por ID do montador")

    op_upd = sub.add_parser("opupdate", help="Atualiza dados da OP")
    op_upd.add_argument("id", type=int)
    op_upd.add_argument("--status")
    op_upd.add_argument("--montador", type=int, help="ID do colaborador montador")
    op_upd.add_argument("--estimativa", type=float, help="Nova estimativa de horas")

    op_alert = sub.add_parser("opalert", help="Lista OPs aguardando separacao ha X dias")
    op_alert.add_argument("dias", type=int)

    label = sub.add_parser("label", help="Gera etiqueta PDF de uma OP")
    label.add_argument("op_id", type=int)

    args = parser.parse_args()
    db = DatabaseManager()

    if args.cmd == "add":
        usuario_id = db.get_usuario_id(args.usuario) if args.usuario else ""
        cid = db.add_colaborador(args.nome, args.setor, usuario_id, args.foto)
        if cid:
            print(f"Colaborador cadastrado com id {cid}")
    elif args.cmd == "list":
        colaboradores = db.listar_colaboradores(args.setor, with_login=True)
        for c in colaboradores:
            login = c[3] or "-"
            foto = c[4] or "-"
            print(f"{c[0]} - {c[1]} ({c[2]}) usuario:{login} foto:{foto}")
    elif args.cmd == "show":
        col = db.obter_colaborador(args.id, with_login=True)
        if not col:
            print("Colaborador nao encontrado")
        else:
            login = col[3] or "-"
            foto = col[4] or "-"
            print(f"ID: {col[0]}\nNome: {col[1]}\nSetor: {col[2]}\nUsuario: {login}\nFoto: {foto}")
    elif args.cmd == "update":
        usuario_id = None
        if args.usuario is not None:
            usuario_id = db.get_usuario_id(args.usuario) if args.usuario else ""
        sucesso = db.atualizar_colaborador(
            args.id,
            nome=args.nome,
            setor=args.setor,
            usuario_id=usuario_id,
            caminho_foto=args.foto,
        )
        if sucesso:
            print("Colaborador atualizado com sucesso")
        else:
            print("Falha ao atualizar colaborador")
    elif args.cmd == "delete":
        if db.remover_colaborador(args.id):
            print("Colaborador removido")
        else:
            print("Falha ao remover colaborador")
    elif args.cmd == "useradd":
        uid = db.add_usuario(args.login, args.senha, args.perfil)
        if uid:
            print(f"Usuario criado com id {uid}")
        else:
            print("Falha ao criar usuario")
    elif args.cmd == "userlist":
        for u in db.listar_usuarios():
            print(f"{u[0]} - {u[1]} ({u[2]})")
    elif args.cmd == "userupdate":
        if db.atualizar_usuario(args.id, login=args.login, senha=args.senha, perfil=args.perfil):
            print("Usuario atualizado")
        else:
            print("Falha ao atualizar usuario")
    elif args.cmd == "userdel":
        if db.remover_usuario(args.id):
            print("Usuario removido")
        else:
            print("Falha ao remover usuario")
    elif args.cmd == "clientadd":
        cid = db.add_cliente(args.nome, args.cnpj)
        if cid:
            print(f"Cliente criado com id {cid}")
        else:
            print("Falha ao criar cliente")
    elif args.cmd == "clientlist":
        for c in db.listar_clientes():
            cnpj = c[2] or "-"
            print(f"{c[0]} - {c[1]} ({cnpj})")
    elif args.cmd == "clientupdate":
        if db.atualizar_cliente(args.id, nome=args.nome, cnpj=args.cnpj):
            print("Cliente atualizado")
        else:
            print("Falha ao atualizar cliente")
    elif args.cmd == "clientdel":
        if db.remover_cliente(args.id):
            print("Cliente removido")
        else:
            print("Falha ao remover cliente")
    elif args.cmd == "login":
        if db.verificar_login(args.login, args.senha):
            print("Credenciais validas")
        else:
            print("Login ou senha invalidos")
    elif args.cmd == "stockadd":
        db.adicionar_item_estoque(args.produto, args.quantidade)
        print("Estoque atualizado")
    elif args.cmd == "stockout":
        if db.registrar_saida_estoque(args.produto, args.quantidade):
            print("Saida registrada")
        else:
            print("Produto nao encontrado")
    elif args.cmd == "stockset":
        db.definir_quantidade_estoque(args.produto, args.quantidade)
        print("Estoque definido")
    elif args.cmd == "stocklist":
        for s in db.listar_estoque():
            print(f"{s[0]} - {s[1]}: {s[2]}")
    elif args.cmd == "stockalert":
        itens = db.verificar_baixo_estoque(args.limite)
        if not itens:
            print("Nenhum item abaixo do limite")
        else:
            for nome, qtd in itens:
                print(f"{nome}: {qtd}")
    elif args.cmd == "discadd":
        did = db.registrar_discrepancia(args.op_id, args.produto, args.quantidade, args.tipo)
        if did:
            print(f"Discrepancia registrada com id {did}")
        else:
            print("Falha ao registrar discrepancia")
    elif args.cmd == "disclist":
        for d in db.listar_discrepancias(args.op):
            print(f"{d[0]} - OP {d[1]} - {d[2]} {d[3]} ({d[4]}) em {d[5]}")
    elif args.cmd == "discreport":
        rel = db.relatorio_discrepancias_por_op(args.op)
        if not rel:
            print("Nenhum dado de discrepancia")
        else:
            for r in rel:
                print(f"OP {r[0]} - {r[1]}: +{r[2]} adicionais, {r[3]} discrepancias")
    elif args.cmd == "opadd":
        oid = db.criar_op(args.descricao, args.montador, args.estimativa)
        if oid:
            print(f"OP criada com id {oid}")
        else:
            print("Falha ao criar OP")
    elif args.cmd == "opstart":
        if db.iniciar_op(args.id):
            print("OP iniciada")
        else:
            print("Falha ao iniciar OP")
    elif args.cmd == "opfinish":
        if db.finalizar_op(args.id):
            print("OP finalizada")
        else:
            print("Falha ao finalizar OP")
    elif args.cmd == "opkpi":
        info = db.kpi_op(args.id)
        if not info:
            print("OP nao encontrada")
        else:
            est = info['estimado'] or 0
            real = info['real'] or 0
            eff = info['eficiencia']
            print(f"Estimado: {est}h | Real: {real:.2f}h")
            if eff is not None:
                print(f"Eficiencia: {eff:.1f}%")
    elif args.cmd == "opprogress":
        info = db.progresso_op(args.id)
        if not info:
            print("OP nao iniciada ou inexistente")
        else:
            est = info["estimado"] or 0
            dec = info["decorrido"]
            pct = (dec / est * 100) if est else 0
            print(f"Estimado: {est}h | Decorrido: {dec:.2f}h ({pct:.1f}% usado)")
    elif args.cmd == "montkpi":
        info = db.kpi_montador(args.id)
        nome = db.get_colaborador_nome(args.id) or "Montador"
        if not info:
            print("Sem dados para este montador")
        else:
            est = info['estimativa_media'] or 0
            real = info['real_medio'] or 0
            eff = info['eficiencia']
            print(f"{nome} - {info['ops']} OPs")
            print(f"Media estimada: {est:.2f}h | Media real: {real:.2f}h")
            if eff is not None:
                print(f"Eficiencia media: {eff:.1f}%")
    elif args.cmd == "oplist":
        for o in db.listar_ops(args.status, args.montador):
            montador = o[2] or "-"
            est = o[6]
            real = o[7]
            print(f"{o[0]} - {o[1]} / Montador: {montador} [{o[3]}] criado em {o[4]} est:{est}h real:{real:.2f}h")
    elif args.cmd == "opupdate":
        if db.atualizar_op(
            args.id,
            status=args.status,
            montador_id=args.montador,
            estimativa_horas=args.estimativa,
        ):
            print("OP atualizada")
        else:
            print("Falha ao atualizar OP")
    elif args.cmd == "opalert":
        atrasadas = db.ops_atrasadas(args.dias)
        if not atrasadas:
            print("Nenhuma OP atrasada")
        else:
            for oid, desc, data in atrasadas:
                print(f"{oid} - {desc} (desde {data})")
    elif args.cmd == "label":
        op = db.get_op(args.op_id)
        if not op:
            print("OP nao encontrada")
        else:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            pdf.cell(0, 10, txt=f"OP {op[0]} - {op[1]}", ln=1)
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Montador: {op[2] or '-'}", ln=1)
            pdf.cell(0, 10, txt=f"Status: {op[3]}", ln=1)
            pdf.cell(0, 10, txt=f"Data: {op[4]}", ln=1)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 8, txt="Gerado com apoio de IA e de uso exclusivo da ER Elétrica.")
            file_name = f"etiqueta_OP{op[0]}.pdf"
            pdf.output(file_name)
            print(f"Etiqueta gerada: {file_name}")
    elif args.cmd == "budgetadd":
        oid = db.criar_orcamento(args.descricao, args.cliente, args.motivo)
        if oid:
            print(f"Orcamento criado com id {oid}")
        else:
            print("Falha ao criar orcamento")
    elif args.cmd == "budgetrev":
        if db.registrar_revisao(args.id, args.motivo):
            print("Revisao registrada")
        else:
            print("Falha ao registrar revisao")
    elif args.cmd == "budgetlist":
        for b in db.listar_orcamentos(resultado=args.resultado, aprovado=args.aprovado, cliente=args.cliente):
            print(f"{b[0]} - {b[1]} (rev {b[3]}) - {b[4]} / {b[5]}")
    elif args.cmd == "budgethist":
        for r in db.historico_revisoes(args.id):
            print(f"REV{r[0]:02d} - {r[1]} em {r[2]}")
    elif args.cmd == "budgettime":
        tempos = db.calcular_tempos_orcamento(args.id)
        if not tempos:
            print("Nenhum dado de tempo para este orcamento")
        else:
            print(f"Tempo total: {tempos['total']}")
            print(f"Tempo de alteracoes: {tempos['alteracao']}")
            print(f"Tempo ocioso: {tempos['ocioso']}")
    elif args.cmd == "budgetapprove":
        oid = db.aprovar_orcamento(args.id, args.montador)
        if oid:
            print(f"Orcamento aprovado. OP criada com id {oid}")
        else:
            print("Falha ao aprovar orcamento")
    elif args.cmd == "budgetresult":
        if db.atualizar_resultado_orcamento(args.id, args.resultado, args.motivo, args.qualificacao):
            print("Resultado atualizado")
        else:
            print("Falha ao atualizar resultado do orcamento")
    elif args.cmd == "kpiexport":
        if db.exportar_dados_kpi(args.arquivo, args.orcamento):
            print(f"Dados exportados para {args.arquivo}")
        else:
            print("Falha ao exportar dados")
    elif args.cmd == "ofximport":
        count = db.importar_ofx(args.arquivo)
        if count is None:
            print("Falha ao importar OFX")
        else:
            print(f"{count} transacoes importadas")
    elif args.cmd == "ofxlist":
        for t in db.listar_transacoes(args.limit):
            print(f"{t[0]} - {t[1]} | {t[2]}: {t[3]:.2f}")


if __name__ == "__main__":
    main()

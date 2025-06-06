import sqlite3
import logging
import bcrypt
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    """Gerencia o banco de dados da aplicacao."""

    def __init__(self, db_path='orcamentos.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.verificar_estrutura_banco()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def verificar_estrutura_banco(self):
        """Cria as tabelas necessarias se nao existirem."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                perfil TEXT NOT NULL DEFAULT 'usuario'
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS colaboradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                setor TEXT NOT NULL,
                usuario_id TEXT DEFAULT '',
                caminho_foto TEXT DEFAULT ''
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                cnpj TEXT DEFAULT ''
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT NOT NULL UNIQUE,
                quantidade INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS discrepancias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                op_id INTEGER,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                data DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (op_id) REFERENCES ordens_producao(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ordens_producao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                montador_id INTEGER,
                status TEXT NOT NULL DEFAULT 'Aguardando Separacao',
                estimativa_horas REAL DEFAULT 0,
                tempo_real_horas REAL DEFAULT 0,
                inicio_montagem DATETIME,
                fim_montagem DATETIME,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (montador_id) REFERENCES colaboradores(id)
            )
            """
        )
        # Garante que a coluna montador_id exista (para bancos antigos)
        try:
            cursor.execute("PRAGMA table_info(ordens_producao)")
            cols = [c[1] for c in cursor.fetchall()]
            if "montador_id" not in cols:
                cursor.execute("ALTER TABLE ordens_producao ADD COLUMN montador_id INTEGER")
            if "estimativa_horas" not in cols:
                cursor.execute("ALTER TABLE ordens_producao ADD COLUMN estimativa_horas REAL DEFAULT 0")
            if "tempo_real_horas" not in cols:
                cursor.execute("ALTER TABLE ordens_producao ADD COLUMN tempo_real_horas REAL DEFAULT 0")
            if "inicio_montagem" not in cols:
                cursor.execute("ALTER TABLE ordens_producao ADD COLUMN inicio_montagem DATETIME")
            if "fim_montagem" not in cols:
                cursor.execute("ALTER TABLE ordens_producao ADD COLUMN fim_montagem DATETIME")
            if "ultima_atualizacao" not in cols:
                cursor.execute("ALTER TABLE ordens_producao ADD COLUMN ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP")
        except sqlite3.Error:
            pass
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orcamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                cliente TEXT DEFAULT '',
                revisao INTEGER NOT NULL DEFAULT 0,
                motivo TEXT DEFAULT '',
                aprovado INTEGER NOT NULL DEFAULT 0,
                resultado TEXT NOT NULL DEFAULT 'aberto',
                motivo_resultado TEXT DEFAULT '',
                qualificacao_cliente TEXT DEFAULT '',
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        # Garantir colunas novas para bancos antigos
        try:
            cursor.execute("PRAGMA table_info(orcamentos)")
            cols = [c[1] for c in cursor.fetchall()]
            if "aprovado" not in cols:
                cursor.execute("ALTER TABLE orcamentos ADD COLUMN aprovado INTEGER NOT NULL DEFAULT 0")
            if "resultado" not in cols:
                cursor.execute("ALTER TABLE orcamentos ADD COLUMN resultado TEXT NOT NULL DEFAULT 'aberto'")
            if "motivo_resultado" not in cols:
                cursor.execute("ALTER TABLE orcamentos ADD COLUMN motivo_resultado TEXT DEFAULT ''")
            if "qualificacao_cliente" not in cols:
                cursor.execute("ALTER TABLE orcamentos ADD COLUMN qualificacao_cliente TEXT DEFAULT ''")
        except sqlite3.Error:
            pass
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS revisoes_orcamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orcamento_id INTEGER NOT NULL,
                revisao INTEGER NOT NULL,
                motivo TEXT,
                data DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (orcamento_id) REFERENCES orcamentos (id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tempo_orcamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orcamento_id INTEGER NOT NULL,
                evento TEXT NOT NULL,
                data DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ofx_transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL
            )
            """
        )
        self.conn.commit()

    # --- Contagem simples para exibir KPIs ---
    def contar_colaboradores(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM colaboradores")
        return cur.fetchone()[0]

    def contar_clientes(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM clientes")
        return cur.fetchone()[0]

    def contar_produtos(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM produtos")
        return cur.fetchone()[0]

    def contar_ops(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM ordens_producao")
        return cur.fetchone()[0]

    def contar_orcamentos(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM orcamentos")
        return cur.fetchone()[0]

    def add_colaborador(self, nome, setor, usuario_id='', caminho_foto=''):
        """Adiciona um colaborador."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO colaboradores (nome, setor, usuario_id, caminho_foto) VALUES (?, ?, ?, ?)",
                (nome, setor, usuario_id, caminho_foto),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Erro ao adicionar colaborador: {e}")
            return None

    def listar_colaboradores(self, filtro="", setor=None, with_login=False):
        """Retorna lista de colaboradores. Se ``with_login`` for True, inclui o login do usuario associado. Pode filtrar pelo nome."""
        cur = self.conn.cursor()
        if with_login:
            base = (
                "SELECT c.id, c.nome, c.setor, u.login, c.caminho_foto "
                "FROM colaboradores c LEFT JOIN usuarios u ON c.usuario_id = u.id"
            )
        else:
            base = "SELECT c.id, c.nome, c.setor, c.usuario_id, c.caminho_foto FROM colaboradores c"
        params = []
        where = []
        if setor:
            where.append("c.setor = ?")
            params.append(setor)
        if filtro:
            where.append("c.nome LIKE ?")
            params.append(f"%{filtro}%")
        query = base
        if where:
            query += " WHERE " + " AND ".join(where)
        query += " ORDER BY c.nome"
        cur.execute(query, params)
        return cur.fetchall()

    def obter_colaborador(self, cid, with_login=False):
        """Retorna dados de um colaborador especifico."""
        cur = self.conn.cursor()
        if with_login:
            cur.execute(
                "SELECT c.id, c.nome, c.setor, u.login, c.caminho_foto "
                "FROM colaboradores c LEFT JOIN usuarios u ON c.usuario_id = u.id "
                "WHERE c.id = ?",
                (cid,),
            )
        else:
            cur.execute(
                "SELECT id, nome, setor, usuario_id, caminho_foto FROM colaboradores WHERE id = ?",
                (cid,),
            )
        return cur.fetchone()

    def atualizar_colaborador(self, cid, nome=None, setor=None, usuario_id=None, caminho_foto=None):
        """Atualiza os dados de um colaborador."""
        campos = []
        valores = []
        if nome is not None:
            campos.append("nome = ?")
            valores.append(nome)
        if setor is not None:
            campos.append("setor = ?")
            valores.append(setor)
        if usuario_id is not None:
            campos.append("usuario_id = ?")
            valores.append(usuario_id)
        if caminho_foto is not None:
            campos.append("caminho_foto = ?")
            valores.append(caminho_foto)
        if not campos:
            return False
        valores.append(cid)
        sql = f"UPDATE colaboradores SET {', '.join(campos)} WHERE id = ?"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, valores)
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar colaborador: {e}")
            return False

    def remover_colaborador(self, cid):
        """Remove um colaborador pelo id."""
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM colaboradores WHERE id = ?", (cid,))
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao remover colaborador: {e}")
            return False

    def get_colaborador_nome(self, cid):
        cur = self.conn.cursor()
        cur.execute("SELECT nome FROM colaboradores WHERE id = ?", (cid,))
        res = cur.fetchone()
        return res[0] if res else None

    # --------- Metodos para clientes ---------

    def add_cliente(self, nome, cnpj=""):
        """Adiciona um novo cliente."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO clientes (nome, cnpj) VALUES (?, ?)",
                (nome, cnpj),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            logging.error("Cliente ja existe")
            return None
        except sqlite3.Error as e:
            logging.error(f"Erro ao adicionar cliente: {e}")
            return None

    def listar_clientes(self, filtro=""):
        """Lista clientes opcionalmente filtrando pelo nome."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, nome, cnpj FROM clientes WHERE nome LIKE ? ORDER BY nome",
            (f"%{filtro}%",),
        )
        return cur.fetchall()

    def obter_cliente(self, cid):
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome, cnpj FROM clientes WHERE id = ?", (cid,))
        return cur.fetchone()

    def atualizar_cliente(self, cid, nome=None, cnpj=None):
        campos = []
        valores = []
        if nome is not None:
            campos.append("nome = ?")
            valores.append(nome)
        if cnpj is not None:
            campos.append("cnpj = ?")
            valores.append(cnpj)
        if not campos:
            return False
        valores.append(cid)
        sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id = ?"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, valores)
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar cliente: {e}")
            return False

    def remover_cliente(self, cid):
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM clientes WHERE id = ?", (cid,))
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao remover cliente: {e}")
            return False

    def get_cliente_nome(self, cid):
        cur = self.conn.cursor()
        cur.execute("SELECT nome FROM clientes WHERE id = ?", (cid,))
        res = cur.fetchone()
        return res[0] if res else None

    # --------- Metodos para usuarios ---------

    def add_usuario(self, login, senha, perfil="usuario"):
        """Adiciona um novo usuario com senha criptografada."""
        try:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (login, senha_hash, perfil) VALUES (?, ?, ?)",
                (login, senha_hash, perfil),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            logging.error("Login ja existente")
            return None
        except sqlite3.Error as e:
            logging.error(f"Erro ao adicionar usuario: {e}")
            return None

    def listar_usuarios(self):
        """Retorna lista de usuarios cadastrados."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, login, perfil FROM usuarios ORDER BY login")
        return cur.fetchall()

    def atualizar_usuario(self, uid, login=None, senha=None, perfil=None):
        """Atualiza informacoes do usuario."""
        campos = []
        valores = []
        if login is not None:
            campos.append("login = ?")
            valores.append(login)
        if senha is not None:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
            campos.append("senha_hash = ?")
            valores.append(senha_hash)
        if perfil is not None:
            campos.append("perfil = ?")
            valores.append(perfil)
        if not campos:
            return False
        valores.append(uid)
        sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, valores)
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar usuario: {e}")
            return False

    def remover_usuario(self, uid):
        """Remove usuario pelo id."""
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao remover usuario: {e}")
            return False

    def get_usuario_id(self, login):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM usuarios WHERE login = ?", (login,))
        res = cur.fetchone()
        return res[0] if res else None

    def verificar_login(self, login, senha):
        cur = self.conn.cursor()
        cur.execute("SELECT senha_hash FROM usuarios WHERE login = ?", (login,))
        res = cur.fetchone()
        if res and bcrypt.checkpw(senha.encode(), res[0].encode()):
            return True
        return False

    # --------- Metodos de estoque ---------

    def adicionar_item_estoque(self, produto, quantidade):
        """Adiciona quantidade ao item de estoque, criando-o se necessario."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, quantidade FROM estoque WHERE produto = ?",
            (produto,),
        )
        res = cur.fetchone()
        if res:
            eid, atual = res
            nova_qtd = atual + quantidade
            cur.execute(
                "UPDATE estoque SET quantidade = ? WHERE id = ?",
                (nova_qtd, eid),
            )
        else:
            cur.execute(
                "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)",
                (produto, quantidade),
            )
        self.conn.commit()

    def registrar_saida_estoque(self, produto, quantidade):
        """Remove quantidade de um item de estoque."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, quantidade FROM estoque WHERE produto = ?",
            (produto,),
        )
        res = cur.fetchone()
        if not res:
            return False
        eid, atual = res
        nova_qtd = max(0, atual - quantidade)
        cur.execute(
            "UPDATE estoque SET quantidade = ? WHERE id = ?",
            (nova_qtd, eid),
        )
        self.conn.commit()
        return True

    def definir_quantidade_estoque(self, produto, quantidade):
        """Define a quantidade exata de um item no estoque, criando-o se necessario."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id FROM estoque WHERE produto = ?",
            (produto,),
        )
        res = cur.fetchone()
        if res:
            eid = res[0]
            cur.execute(
                "UPDATE estoque SET quantidade = ? WHERE id = ?",
                (quantidade, eid),
            )
        else:
            cur.execute(
                "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)",
                (produto, quantidade),
            )
        self.conn.commit()
        return True

    def listar_estoque(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, produto, quantidade FROM estoque ORDER BY produto")
        return cur.fetchall()

    def verificar_baixo_estoque(self, limite):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT produto, quantidade FROM estoque WHERE quantidade <= ?",
            (limite,),
        )
        return cur.fetchall()

    # --------- Discrepancias de estoque ---------

    def registrar_discrepancia(self, op_id, produto, quantidade, tipo):
        """Registra discrepancias ou materiais adicionais."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO discrepancias (op_id, produto, quantidade, tipo) VALUES (?, ?, ?, ?)",
                (op_id, produto, quantidade, tipo),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Erro ao registrar discrepancia: {e}")
            return None

    def listar_discrepancias(self, op_id=None):
        cur = self.conn.cursor()
        if op_id is not None:
            cur.execute(
                "SELECT id, op_id, produto, quantidade, tipo, data FROM discrepancias WHERE op_id = ? ORDER BY data",
                (op_id,),
            )
        else:
            cur.execute(
                "SELECT id, op_id, produto, quantidade, tipo, data FROM discrepancias ORDER BY data"
            )
        return cur.fetchall()

    def relatorio_discrepancias_por_op(self, op_id=None):
        """Retorna o total de discrepancias e adicionais por OP."""
        cur = self.conn.cursor()
        base = (
            "SELECT d.op_id, o.descricao, "
            "SUM(CASE WHEN d.tipo='adicional' THEN d.quantidade ELSE 0 END) AS adicionais, "
            "SUM(CASE WHEN d.tipo='discrepancia' THEN d.quantidade ELSE 0 END) AS discrepancias "
            "FROM discrepancias d LEFT JOIN ordens_producao o ON d.op_id=o.id "
        )
        if op_id is not None:
            cur.execute(base + "WHERE d.op_id = ? GROUP BY d.op_id", (op_id,))
        else:
            cur.execute(base + "GROUP BY d.op_id")
        return cur.fetchall()

    # --------- Metodos de ordens de producao ---------

    def criar_op(self, descricao, montador_id=None, estimativa_horas=0):
        """Cria uma nova ordem de producao."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO ordens_producao (descricao, montador_id, estimativa_horas) VALUES (?, ?, ?)",
                (descricao, montador_id, estimativa_horas),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar OP: {e}")
            return None

    def listar_ops(self, status=None, montador_id=None):
        cur = self.conn.cursor()
        base = (
            "SELECT o.id, o.descricao, c.nome, o.status, o.data_criacao, o.ultima_atualizacao, o.estimativa_horas, o.tempo_real_horas "
            "FROM ordens_producao o LEFT JOIN colaboradores c ON o.montador_id = c.id"
        )
        conds = []
        vals = []
        if status:
            conds.append("o.status = ?")
            vals.append(status)
        if montador_id is not None:
            conds.append("o.montador_id = ?")
            vals.append(montador_id)
        if conds:
            base += " WHERE " + " AND ".join(conds)
        base += " ORDER BY o.data_criacao"
        cur.execute(base, tuple(vals))
        return cur.fetchall()

    def get_op(self, op_id):
        """Retorna informacoes de uma OP especifica."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT o.id, o.descricao, c.nome, o.status, o.data_criacao, o.estimativa_horas, o.tempo_real_horas "
            "FROM ordens_producao o LEFT JOIN colaboradores c ON o.montador_id = c.id "
            "WHERE o.id = ?",
            (op_id,),
        )
        return cur.fetchone()

    def atualizar_op(self, oid, status=None, montador_id=None, estimativa_horas=None):
        try:
            cur = self.conn.cursor()
            campos = []
            valores = []
            if status is not None:
                campos.append("status = ?")
                valores.append(status)
            if montador_id is not None:
                campos.append("montador_id = ?")
                valores.append(montador_id)
            if estimativa_horas is not None:
                campos.append("estimativa_horas = ?")
                valores.append(estimativa_horas)
            if not campos:
                return False
            campos.append("ultima_atualizacao = CURRENT_TIMESTAMP")
            sql = f"UPDATE ordens_producao SET {', '.join(campos)} WHERE id = ?"
            valores.append(oid)
            cur.execute(sql, valores)
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar OP: {e}")
            return False

    def iniciar_op(self, op_id):
        """Marca o inicio da montagem de uma OP."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE ordens_producao SET inicio_montagem = CURRENT_TIMESTAMP, status = 'Em Producao', ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?",
                (op_id,),
            )
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao iniciar OP: {e}")
            return False

    def finalizar_op(self, op_id):
        """Registra o fim da montagem e calcula o tempo real."""
        from datetime import datetime
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT inicio_montagem FROM ordens_producao WHERE id = ?", (op_id,))
            row = cur.fetchone()
            if not row:
                return False
            inicio = row[0]
            if inicio:
                inicio_dt = datetime.fromisoformat(inicio)
            else:
                inicio_dt = datetime.now()
            tempo_real = (datetime.now() - inicio_dt).total_seconds() / 3600.0
            cur.execute(
                "UPDATE ordens_producao SET fim_montagem = CURRENT_TIMESTAMP, tempo_real_horas = ?, status = 'Concluida', ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?",
                (tempo_real, op_id),
            )
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao finalizar OP: {e}")
            return False

    def kpi_op(self, op_id):
        """Retorna informacoes de tempo estimado versus real da OP."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT estimativa_horas, tempo_real_horas FROM ordens_producao WHERE id = ?",
            (op_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        estimado, real = row
        eficiencia = None
        if estimado and real and real > 0:
            eficiencia = estimado / real * 100
        return {"estimado": estimado, "real": real, "eficiencia": eficiencia}

    def progresso_op(self, op_id):
        """Calcula horas decorrido desde o inicio de uma OP."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT estimativa_horas, inicio_montagem FROM ordens_producao WHERE id = ?",
            (op_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        estimado, inicio = row
        if not inicio:
            return None
        from datetime import datetime
        try:
            inicio_dt = datetime.fromisoformat(inicio)
        except Exception:
            return None
        decorrido = (datetime.now() - inicio_dt).total_seconds() / 3600.0
        return {"estimado": estimado, "decorrido": decorrido}

    def ops_atrasadas(self, dias):
        """Retorna OPs em 'Aguardando Separacao' ha mais de 'dias'."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, descricao, data_criacao FROM ordens_producao "
            "WHERE status = 'Aguardando Separacao' AND "+
            "julianday('now') - julianday(data_criacao) >= ?",
            (dias,),
        )
        return cur.fetchall()

    def kpi_montador(self, montador_id):
        """Retorna media de eficiencia das OPs concluidas de um montador."""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT COUNT(*), AVG(estimativa_horas), AVG(tempo_real_horas) "
            "FROM ordens_producao WHERE montador_id = ? AND tempo_real_horas > 0",
            (montador_id,),
        )
        row = cur.fetchone()
        if not row or row[0] == 0:
            return None
        qtd, est_media, real_media = row
        eficiencia = None
        if est_media and real_media and real_media > 0:
            eficiencia = est_media / real_media * 100
        return {
            "ops": qtd,
            "estimativa_media": est_media,
            "real_medio": real_media,
            "eficiencia": eficiencia,
        }

    # --------- Metodos de orcamentos e revisoes ---------

    def criar_orcamento(self, descricao, cliente="", motivo=""):
        """Cria um novo orcamento (REV00)."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO orcamentos (descricao, cliente, motivo) VALUES (?, ?, ?)",
                (descricao, cliente, motivo),
            )
            oid = cur.lastrowid
            cur.execute(
                "INSERT INTO revisoes_orcamento (orcamento_id, revisao, motivo) VALUES (?, 0, ?)",
                (oid, motivo),
            )
            self.registrar_evento_tempo(oid, 'criado')
            self.conn.commit()
            return oid
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar orcamento: {e}")
            return None

    def registrar_revisao(self, orcamento_id, motivo=""):
        """Registra uma nova revisao do orcamento."""
        cur = self.conn.cursor()
        cur.execute("SELECT revisao FROM orcamentos WHERE id = ?", (orcamento_id,))
        res = cur.fetchone()
        if not res:
            return False
        nova_rev = res[0] + 1
        try:
            cur.execute(
                "UPDATE orcamentos SET revisao = ?, motivo = ?, ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?",
                (nova_rev, motivo, orcamento_id),
            )
            cur.execute(
                "INSERT INTO revisoes_orcamento (orcamento_id, revisao, motivo) VALUES (?, ?, ?)",
                (orcamento_id, nova_rev, motivo),
            )
            self.registrar_evento_tempo(orcamento_id, 'revisao')
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Erro ao registrar revisao: {e}")
            return False

    def listar_orcamentos(self, resultado=None, aprovado=None, cliente=None, descricao=None):
        """Lista orcamentos com filtros opcionais por resultado, aprovacao, cliente ou descricao."""
        cur = self.conn.cursor()
        query = (
            "SELECT id, descricao, cliente, revisao, resultado, qualificacao_cliente, "
            "data_criacao, ultima_atualizacao FROM orcamentos WHERE 1=1"
        )
        params = []
        if resultado:
            query += " AND resultado = ?"
            params.append(resultado)
        if aprovado is not None:
            query += " AND aprovado = ?"
            params.append(1 if aprovado else 0)
        if cliente:
            query += " AND cliente = ?"
            params.append(cliente)
        if descricao:
            query += " AND descricao LIKE ?"
            params.append(f"%{descricao}%")
        query += " ORDER BY id"
        cur.execute(query, params)
        return cur.fetchall()

    def historico_revisoes(self, orcamento_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT revisao, motivo, data FROM revisoes_orcamento WHERE orcamento_id = ? ORDER BY revisao",
            (orcamento_id,),
        )
        return cur.fetchall()

    def registrar_evento_tempo(self, orcamento_id, evento):
        """Registra um evento relacionado ao tempo do orcamento."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO tempo_orcamentos (orcamento_id, evento) VALUES (?, ?)",
                (orcamento_id, evento),
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Erro ao registrar evento de tempo: {e}")
            return None

    def eventos_tempo(self, orcamento_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT evento, data FROM tempo_orcamentos WHERE orcamento_id = ? ORDER BY data",
            (orcamento_id,),
        )
        return cur.fetchall()

    def calcular_tempos_orcamento(self, orcamento_id):
        """Calcula tempos totais, ociosidade e alteracoes."""
        from datetime import datetime, timedelta

        eventos = self.eventos_tempo(orcamento_id)
        if not eventos:
            return None
        tempos = [datetime.fromisoformat(ev[1]) for ev in eventos]
        total = tempos[-1] - tempos[0]
        alteracoes = timedelta()
        ocioso = timedelta()
        for a, b in zip(tempos, tempos[1:]):
            diff = b - a
            alteracoes += diff
            if diff.total_seconds() > 1800:
                ocioso += diff
        return {
            "total": total,
            "alteracao": alteracoes,
            "ocioso": ocioso,
        }

    def aprovar_orcamento(self, orcamento_id, montador_id=None):
        """Marca o orcamento como aprovado e gera uma OP vinculada."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT descricao FROM orcamentos WHERE id = ?", (orcamento_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            descricao = row[0]
            cur.execute(
                "UPDATE orcamentos SET aprovado = 1, ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?",
                (orcamento_id,),
            )
            op_desc = f"OP do orcamento {descricao}"
            cur.execute(
                "INSERT INTO ordens_producao (descricao, montador_id) VALUES (?, ?)",
                (op_desc, montador_id),
            )
            oid = cur.lastrowid
            self.registrar_evento_tempo(orcamento_id, 'aprovado')
            self.conn.commit()
            return oid
        except sqlite3.Error as e:
            logging.error(f"Erro ao aprovar orcamento: {e}")
            return None

    def atualizar_resultado_orcamento(self, orcamento_id, resultado, motivo="", qualificacao=""):
        """Atualiza o resultado final do orçamento (vendido ou perdido)."""
        try:
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE orcamentos SET resultado = ?, motivo_resultado = ?, qualificacao_cliente = ?, ultima_atualizacao = CURRENT_TIMESTAMP WHERE id = ?",
                (resultado, motivo, qualificacao, orcamento_id),
            )
            self.conn.commit()
            return cur.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar resultado do orcamento: {e}")
            return False

    def exportar_dados_kpi(self, file_path, orcamento_id=None):
        """Exporta dados de orçamentos em formato JSON para dashboards de KPI."""
        try:
            cur = self.conn.cursor()
            if orcamento_id:
                cur.execute(
                    "SELECT id, descricao, cliente, revisao, aprovado, resultado, qualificacao_cliente FROM orcamentos WHERE id = ?",
                    (orcamento_id,),
                )
            else:
                cur.execute(
                    "SELECT id, descricao, cliente, revisao, aprovado, resultado, qualificacao_cliente FROM orcamentos"
                )
            rows = cur.fetchall()
            dados = []
            for r in rows:
                tempos = self.calcular_tempos_orcamento(r[0]) or {}
                dados.append(
                    {
                        "id": r[0],
                        "descricao": r[1],
                        "cliente": r[2],
                        "revisao": r[3],
                        "aprovado": bool(r[4]),
                        "resultado": r[5],
                        "qualificacao": r[6],
                        "tempos": {
                            "total": str(tempos.get("total")),
                            "alteracao": str(tempos.get("alteracao")),
                            "ocioso": str(tempos.get("ocioso")),
                        },
                    }
                )
            import json

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except sqlite3.Error as e:
            logging.error(f"Erro ao exportar dados de KPI: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo KPI: {e}")
            return False

    # --------- Importação de OFX ---------

    def importar_ofx(self, file_path):
        """Importa um extrato bancário em formato OFX."""
        try:
            from ofxparse import OfxParser
        except ImportError:
            logging.error("Biblioteca ofxparse não instalada")
            return None
        try:
            with open(file_path, "rb") as f:
                ofx = OfxParser.parse(f)
            cur = self.conn.cursor()
            count = 0
            for acc in ofx.accounts:
                for tr in acc.statement.transactions:
                    desc = tr.memo or tr.payee or ""
                    valor = float(tr.amount)
                    cur.execute(
                        "INSERT INTO ofx_transacoes (data, descricao, valor) VALUES (?, ?, ?)",
                        (tr.date.strftime("%Y-%m-%d"), desc, valor),
                    )
                    count += 1
            self.conn.commit()
            return count
        except Exception as e:
            logging.error(f"Erro ao importar OFX: {e}")
            return None

    def listar_transacoes(self, limit=None):
        cur = self.conn.cursor()
        if limit:
            cur.execute(
                "SELECT id, data, descricao, valor FROM ofx_transacoes ORDER BY data DESC LIMIT ?",
                (limit,),
            )
        else:
            cur.execute(
                "SELECT id, data, descricao, valor FROM ofx_transacoes ORDER BY data DESC"
            )
        return cur.fetchall()

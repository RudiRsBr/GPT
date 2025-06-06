import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout,
    QLineEdit, QDialog, QTabWidget, QInputDialog, QComboBox, QAction, QLabel,
    QCheckBox
)
from PyQt5.QtCore import Qt
from database import DatabaseManager


def aplicar_estilo_moderno(app):
    """Define um tema moderno e minimalista para a aplicação."""
    estilo = """
        QWidget {
            font-family: 'Segoe UI', 'Roboto', Tahoma, sans-serif;
            font-size: 10pt;
        }
        QMainWindow {
            background-color: #f0f2f5;
        }
        QToolBar, QMenuBar {
            background-color: #ffffff;
            border-bottom: 1px solid #d0d0d0;
        }
        QMenu {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
        }
        QMenu::item:selected {
            background-color: #e6e6e6;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #0063b1;
        }
        QLineEdit, QSpinBox, QDoubleSpinBox {
            padding: 4px;
            border: 1px solid #bfbfbf;
            border-radius: 4px;
            background-color: #ffffff;
        }
        QTableWidget, QTreeWidget {
            border: 1px solid #dcdcdc;
            background-color: #ffffff;
            alternate-background-color: #f9f9f9;
        }
        QHeaderView::section {
            background-color: #f7f7f7;
            padding: 4px;
            border: 1px solid #dcdcdc;
        }
        QScrollBar:vertical {
            background: #efefef;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #cccccc;
            min-height: 20px;
            border-radius: 6px;
        }
        QTabWidget::pane {
            border-top: 2px solid #0078d7;
        }
    """
    app.setStyleSheet(estilo)

def aplicar_estilo_escuro(app):
    """Aplica um tema escuro alternativo."""
    estilo = """
        QWidget {
            font-family: 'Segoe UI', 'Roboto', Tahoma, sans-serif;
            font-size: 10pt;
            color: #f0f0f0;
        }
        QMainWindow {
            background-color: #2d2d30;
        }
        QToolBar, QMenuBar {
            background-color: #3f3f46;
            border-bottom: 1px solid #444;
        }
        QMenu {
            background-color: #3f3f46;
            border: 1px solid #444;
        }
        QMenu::item:selected {
            background-color: #505055;
        }
        QPushButton {
            background-color: #0e639c;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QLineEdit, QSpinBox, QDoubleSpinBox {
            padding: 4px;
            border: 1px solid #555;
            border-radius: 4px;
            background-color: #3f3f46;
            color: #f0f0f0;
        }
        QTableWidget, QTreeWidget {
            border: 1px solid #555;
            background-color: #3f3f46;
            alternate-background-color: #2d2d30;
        }
        QHeaderView::section {
            background-color: #444;
            padding: 4px;
            border: 1px solid #555;
        }
        QTabWidget::pane {
            border-top: 2px solid #0e639c;
        }
    """
    app.setStyleSheet(estilo)

class ColaboradorDialog(QDialog):
    def __init__(self, parent=None, db=None, col_id=None):
        super().__init__(parent)
        self.db = db
        self.col_id = col_id
        self.setWindowTitle("Colaborador")
        self.init_ui()
        if self.col_id:
            self.carregar()

    def init_ui(self):
        layout = QFormLayout(self)
        self.nome = QLineEdit()
        self.setor = QLineEdit()
        self.usuario_combo = QComboBox()
        if self.db:
            users = self.db.listar_usuarios() if hasattr(self.db, "listar_usuarios") else []
            self.usuario_combo.addItem("", "")
            for u in users:
                self.usuario_combo.addItem(u[1], u[0])
        self.foto_path = QLineEdit(); self.foto_path.setReadOnly(True)
        btn_sel = QPushButton("Selecionar Foto")
        btn_sel.clicked.connect(self.selecionar_foto)
        foto_layout = QHBoxLayout(); foto_layout.addWidget(self.foto_path); foto_layout.addWidget(btn_sel)
        layout.addRow("Nome:", self.nome)
        layout.addRow("Setor:", self.setor)
        layout.addRow("Usuário:", self.usuario_combo)
        layout.addRow("Foto:", foto_layout)
        btns = QHBoxLayout()
        ok = QPushButton("Salvar")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancelar")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok); btns.addWidget(cancel)
        layout.addRow(btns)

    def carregar(self):
        col = self.db.obter_colaborador(self.col_id)
        if col:
            self.nome.setText(col[1])
            self.setor.setText(col[2])
            idx = self.usuario_combo.findData(col[3])
            if idx != -1:
                self.usuario_combo.setCurrentIndex(idx)
            self.foto_path.setText(col[4] or "")

    def get_data(self):
        return (
            self.nome.text().strip(),
            self.setor.text().strip(),
            self.usuario_combo.currentData(),
            self.foto_path.text().strip(),
        )

    def selecionar_foto(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecionar Foto", "", "Imagens (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file:
            self.foto_path.setText(file)

class ClienteDialog(QDialog):
    def __init__(self, parent=None, db=None, cid=None):
        super().__init__(parent)
        self.db = db
        self.cid = cid
        self.setWindowTitle("Cliente")
        self.init_ui()
        if self.cid:
            self.carregar()

    def init_ui(self):
        layout = QFormLayout(self)
        self.nome = QLineEdit()
        self.cnpj = QLineEdit()
        layout.addRow("Nome:", self.nome)
        layout.addRow("CNPJ:", self.cnpj)
        btns = QHBoxLayout()
        ok = QPushButton("Salvar")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancelar")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok); btns.addWidget(cancel)
        layout.addRow(btns)

    def carregar(self):
        cli = self.db.obter_cliente(self.cid) if hasattr(self.db, 'obter_cliente') else None
        if cli:
            self.nome.setText(cli[1])
            self.cnpj.setText(cli[2] or '')

    def get_data(self):
        return self.nome.text().strip(), self.cnpj.text().strip()

class UsuarioDialog(QDialog):
    def __init__(self, parent=None, db=None, uid=None):
        super().__init__(parent)
        self.db = db
        self.uid = uid
        self.setWindowTitle("Usuário")
        self.init_ui()
        if self.uid:
            self.carregar()

    def init_ui(self):
        layout = QFormLayout(self)
        self.login = QLineEdit()
        self.senha = QLineEdit(); self.senha.setEchoMode(QLineEdit.Password)
        self.perfil = QLineEdit()
        layout.addRow("Login:", self.login)
        layout.addRow("Senha:", self.senha)
        layout.addRow("Perfil:", self.perfil)
        btns = QHBoxLayout()
        ok = QPushButton("Salvar")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancelar")
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok); btns.addWidget(cancel)
        layout.addRow(btns)

    def carregar(self):
        u = None
        if hasattr(self.db, 'listar_usuarios'):
            for us in self.db.listar_usuarios():
                if us[0] == self.uid:
                    u = us
                    break
        if u:
            self.login.setText(u[1])
            self.perfil.setText(u[2])

    def get_data(self):
        return self.login.text().strip(), self.senha.text(), self.perfil.text().strip()

class OrcamentoTabModificado(QWidget):
    """Aba simples para edicao de orcamentos (placeholder)."""
    def __init__(self, titulo, db, parent=None):
        super().__init__(parent)
        self.db = db
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Edição de orçamento ainda não implementada."))

class ColaboradoresTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome...")
        self.search_input.textChanged.connect(lambda: self.carregar())
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Setor", "Foto"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.currentItemChanged.connect(self.mostrar_foto)
        layout.addWidget(self.table)
        self.foto_label = QLabel()
        self.foto_label.setAlignment(Qt.AlignCenter)
        self.foto_label.setMinimumHeight(150)
        self.foto_label.setStyleSheet("border: 1px solid #cccccc; background:#f0f0f0;")
        layout.addWidget(self.foto_label)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.adicionar)
        btn_edit = QPushButton("Editar")
        btn_edit.clicked.connect(self.editar)
        btn_del = QPushButton("Remover")
        btn_del.clicked.connect(self.remover)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_del)
        layout.addLayout(btn_layout)

    def carregar(self):
        filtro = self.search_input.text() if hasattr(self, 'search_input') else ''
        colaboradores = self.db.listar_colaboradores(filtro)
        self.table.setRowCount(0)
        for col in colaboradores:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(col[:4]):
                item = QTableWidgetItem(str(val))
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)
        self.mostrar_foto()

    def obter_id_selecionado(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def adicionar(self):
        dlg = ColaboradorDialog(self, db=self.db)
        if dlg.exec_() == QDialog.Accepted:
            nome, setor, uid, foto = dlg.get_data()
            if nome and setor:
                self.db.add_colaborador(nome, setor, usuario_id=uid or '', caminho_foto=foto)
                self.carregar()

    def editar(self):
        cid = self.obter_id_selecionado()
        if not cid:
            QMessageBox.warning(self, "Aviso", "Selecione um colaborador")
            return
        dlg = ColaboradorDialog(self, db=self.db, col_id=cid)
        if dlg.exec_() == QDialog.Accepted:
            nome, setor, uid, foto = dlg.get_data()
            self.db.atualizar_colaborador(cid, nome=nome, setor=setor, usuario_id=uid, caminho_foto=foto)
            self.carregar()

    def remover(self):
        cid = self.obter_id_selecionado()
        if not cid:
            QMessageBox.warning(self, "Aviso", "Selecione um colaborador")
            return
        if QMessageBox.question(self, "Confirma", "Remover colaborador?") == QMessageBox.Yes:
            self.db.remover_colaborador(cid)
            self.carregar()

    def mostrar_foto(self, *args):
        cid = self.obter_id_selecionado()
        pix = QPixmap()
        texto = "Sem foto"
        if cid:
            col = self.db.obter_colaborador(cid)
            if col and col[4]:
                path = col[4]
                if QDir(path).exists():
                    pix = QPixmap(path)
                    if not pix.isNull():
                        pix = pix.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        texto = ""
        self.foto_label.setPixmap(pix)
        self.foto_label.setText(texto)

class ClientesTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome...")
        self.search_input.textChanged.connect(self.carregar)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CNPJ"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.adicionar)
        btn_edit = QPushButton("Editar")
        btn_edit.clicked.connect(self.editar)
        btn_del = QPushButton("Remover")
        btn_del.clicked.connect(self.remover)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_del)
        layout.addLayout(btn_layout)

    def carregar(self):
        filtro = self.search_input.text() if hasattr(self, 'search_input') else ""
        clientes = self.db.listar_clientes(filtro)
        self.table.setRowCount(0)
        for cli in clientes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(cli):
                item = QTableWidgetItem(str(val))
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def obter_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def adicionar(self):
        dlg = ClienteDialog(self, db=self.db)
        if dlg.exec_() == QDialog.Accepted:
            nome, cnpj = dlg.get_data()
            if nome:
                self.db.add_cliente(nome, cnpj)
                self.carregar()

    def editar(self):
        cid = self.obter_id()
        if not cid:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente")
            return
        dlg = ClienteDialog(self, db=self.db, cid=cid)
        if dlg.exec_() == QDialog.Accepted:
            nome, cnpj = dlg.get_data()
            self.db.atualizar_cliente(cid, nome=nome, cnpj=cnpj)
            self.carregar()

    def remover(self):
        cid = self.obter_id()
        if not cid:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente")
            return
        if QMessageBox.question(self, "Confirma", "Remover cliente?") == QMessageBox.Yes:
            self.db.remover_cliente(cid)
            self.carregar()

class EstoqueTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Produto", "Quantidade"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.adicionar)
        btn_saida = QPushButton("Saida")
        btn_saida.clicked.connect(self.saida)
        btn_set = QPushButton("Definir")
        btn_set.clicked.connect(self.definir)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_saida)
        btn_layout.addWidget(btn_set)
        layout.addLayout(btn_layout)

    def carregar(self):
        itens = self.db.listar_estoque()
        self.table.setRowCount(0)
        for it in itens:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(it):
                item = QTableWidgetItem(str(val))
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def obter_produto(self):
        row = self.table.currentRow()
        if row == -1:
            return None, None
        pid = int(self.table.item(row, 0).text())
        nome = self.table.item(row, 1).text()
        return pid, nome

    def adicionar(self):
        nome, ok = QInputDialog.getText(self, "Produto", "Nome do produto:")
        if not ok or not nome:
            return
        qtd, ok = QInputDialog.getInt(self, "Quantidade", "Adicionar quantidade:", 1, 1)
        if ok:
            self.db.adicionar_item_estoque(nome, qtd)
            self.carregar()

    def saida(self):
        pid, nome = self.obter_produto()
        if not nome:
            QMessageBox.warning(self, "Aviso", "Selecione um item")
            return
        qtd, ok = QInputDialog.getInt(self, "Saida", f"Quantidade de '{nome}' a remover:", 1, 1)
        if ok:
            self.db.registrar_saida_estoque(nome, qtd)
            self.carregar()

    def definir(self):
        pid, nome = self.obter_produto()
        if not nome:
            QMessageBox.warning(self, "Aviso", "Selecione um item")
            return
        qtd, ok = QInputDialog.getInt(self, "Definir", f"Quantidade exata para '{nome}':", 0, 0)
        if ok:
            self.db.definir_quantidade_estoque(nome, qtd)
            self.carregar()

class UsuariosTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Login", "Perfil"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.adicionar)
        btn_edit = QPushButton("Editar")
        btn_edit.clicked.connect(self.editar)
        btn_del = QPushButton("Remover")
        btn_del.clicked.connect(self.remover)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_del)
        layout.addLayout(btn_layout)

    def carregar(self):
        usuarios = self.db.listar_usuarios()
        self.table.setRowCount(0)
        for u in usuarios:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(u):
                item = QTableWidgetItem(str(val))
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def obter_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def adicionar(self):
        dlg = UsuarioDialog(self, db=self.db)
        if dlg.exec_() == QDialog.Accepted:
            login, senha, perfil = dlg.get_data()
            if login and senha:
                self.db.add_usuario(login, senha, perfil or 'usuario')
                self.carregar()

    def editar(self):
        uid = self.obter_id()
        if not uid:
            QMessageBox.warning(self, "Aviso", "Selecione um usuário")
            return
        dlg = UsuarioDialog(self, db=self.db, uid=uid)
        if dlg.exec_() == QDialog.Accepted:
            login, senha, perfil = dlg.get_data()
            self.db.atualizar_usuario(uid, login=login or None,
                                     senha=senha or None, perfil=perfil or None)
            self.carregar()

    def remover(self):
        uid = self.obter_id()
        if not uid:
            QMessageBox.warning(self, "Aviso", "Selecione um usuário")
            return
        if QMessageBox.question(self, "Confirma", "Remover usuário?") == QMessageBox.Yes:
            self.db.remover_usuario(uid)
            self.carregar()

class DiscrepanciasTab(QWidget):
    """Aba para registrar e listar discrepâncias de estoque por OP."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID", "OP", "Produto", "Qtd", "Tipo"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Registrar")
        btn_add.clicked.connect(self.adicionar)
        btn_layout.addWidget(btn_add)
        layout.addLayout(btn_layout)

    def carregar(self, op_id=None):
        itens = self.db.listar_discrepancias(op_id)
        self.table.setRowCount(0)
        for it in itens:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(it[:5]):
                item = QTableWidgetItem(str(val))
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def adicionar(self):
        ops = self.db.listar_ops()
        op_ids = [o[0] for o in ops]
        descs = [o[1] for o in ops]
        op_id = None
        if descs:
            sel, ok = QInputDialog.getItem(self, "OP", "Selecione:", descs, editable=False)
            if not ok:
                return
            op_id = op_ids[descs.index(sel)]
        produto, ok = QInputDialog.getText(self, "Produto", "Nome do produto:")
        if not ok or not produto:
            return
        qtd, ok = QInputDialog.getInt(self, "Quantidade", "Quantidade:", 1, 1)
        if not ok:
            return
        tipo, ok = QInputDialog.getItem(self, "Tipo", "Tipo:", ["adicional", "discrepancia"], editable=False)
        if ok:
            self.db.registrar_discrepancia(op_id, produto, qtd, tipo)
            self.carregar()

class OrcamentosTab(QWidget):
    """Aba de listagem e criacao de orcamentos."""
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.parent_window = parent
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por descricao...")
        self.search_input.textChanged.connect(self.carregar)
        search_layout.addWidget(self.search_input)
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Cliente...")
        self.client_input.textChanged.connect(self.carregar)
        search_layout.addWidget(self.client_input)
        self.result_combo = QComboBox()
        self.result_combo.addItem("Todos", None)
        self.result_combo.addItem("vendido", "vendido")
        self.result_combo.addItem("perdido", "perdido")
        self.result_combo.addItem("aberto", "aberto")
        self.result_combo.currentIndexChanged.connect(self.carregar)
        search_layout.addWidget(self.result_combo)
        self.check_aprov = QCheckBox("Aprovado")
        self.check_aprov.stateChanged.connect(self.carregar)
        search_layout.addWidget(self.check_aprov)
        layout.addLayout(search_layout)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Descricao", "Cliente", "Revisao", "Aprovado", "Resultado"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemDoubleClicked.connect(self.abrir)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Novo")
        btn_add.clicked.connect(self.adicionar)
        btn_aprovar = QPushButton("Aprovar")
        btn_aprovar.clicked.connect(self.aprovar)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_aprovar)
        layout.addLayout(btn_layout)

    def carregar(self):
        desc = self.search_input.text() if hasattr(self, 'search_input') else None
        cliente = self.client_input.text() if hasattr(self, 'client_input') else None
        resultado = self.result_combo.currentData() if hasattr(self, 'result_combo') else None
        aprovado = 1 if (hasattr(self, 'check_aprov') and self.check_aprov.isChecked()) else None
        orcs = self.db.listar_orcamentos(resultado=resultado, aprovado=aprovado, cliente=cliente or None, descricao=desc)
        self.table.setRowCount(0)
        for o in orcs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(o[:6]):
                item = QTableWidgetItem(str(val) if val is not None else "")
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def obter_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def adicionar(self):
        desc, ok = QInputDialog.getText(self, "Descricao", "Descricao do orçamento:")
        if not ok or not desc:
            return
        clientes = [c[1] for c in self.db.listar_clientes()]
        cid = None
        if clientes:
            nome_sel, ok = QInputDialog.getItem(self, "Cliente", "Selecione:", clientes, editable=False)
            if ok:
                cid = nome_sel
        motivo, ok = QInputDialog.getText(self, "Motivo", "Motivo inicial:")
        if ok:
            self.db.criar_orcamento(desc, cid or "", motivo)
            self.carregar()

    def abrir(self, item=None):
        oid = self.obter_id()
        if not oid:
            return
        orc_tab = OrcamentoTabModificado("Orcamento", self.db, self.parent_window)
        # placeholder for loading existing data; out of scope
        if self.parent_window:
            index = self.parent_window.tab_widget.addTab(orc_tab, f"Orc {oid}")
            self.parent_window.tab_widget.setCurrentIndex(index)

    def aprovar(self):
        oid = self.obter_id()
        if oid:
            montadores = self.db.listar_colaboradores(with_login=False)
            nomes = [c[1] for c in montadores]
            ids = [c[0] for c in montadores]
            mid = None
            if nomes:
                nome_sel, ok = QInputDialog.getItem(self, "Montador", "Selecione:", nomes, editable=False)
                if ok:
                    mid = ids[nomes.index(nome_sel)]
            self.db.aprovar_orcamento(oid, mid)
            self.carregar()

class OPTab(QWidget):
    """Aba para gerenciamento de Ordens de Producao."""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Descricao", "Montador", "Status", "Estimativa", "Real"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Nova OP")
        btn_add.clicked.connect(self.adicionar)
        btn_start = QPushButton("Iniciar")
        btn_start.clicked.connect(self.iniciar)
        btn_finish = QPushButton("Finalizar")
        btn_finish.clicked.connect(self.finalizar)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_finish)
        layout.addLayout(btn_layout)

    def carregar(self):
        ops = self.db.listar_ops()
        self.table.setRowCount(0)
        for op in ops:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(op[:6]):
                item = QTableWidgetItem(str(val) if val is not None else "")
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def obter_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def adicionar(self):
        desc, ok = QInputDialog.getText(self, "Descricao", "Descricao da OP:")
        if not ok or not desc:
            return
        colabs = self.db.listar_colaboradores()
        nomes = [c[1] for c in colabs]
        ids = [c[0] for c in colabs]
        mont = None
        if nomes:
            nome_sel, ok = QInputDialog.getItem(self, "Montador", "Selecione:", nomes, editable=False)
            if ok:
                mont = ids[nomes.index(nome_sel)]
        est, ok = QInputDialog.getDouble(self, "Estimativa", "Horas estimadas:", 0, 0)
        if ok:
            self.db.criar_op(desc, mont, est)
            self.carregar()

    def iniciar(self):
        oid = self.obter_id()
        if oid and self.db.iniciar_op(oid):
            self.carregar()

    def finalizar(self):
        oid = self.obter_id()
        if oid and self.db.finalizar_op(oid):
            self.carregar()

class MontagemTab(QWidget):
    """Aba para acompanhamento de montagem em tempo real."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.carregar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        filt = QHBoxLayout()
        filt.addWidget(QLabel("Montador:"))
        self.combo = QComboBox(); self.combo.currentIndexChanged.connect(self.carregar)
        filt.addWidget(self.combo)
        layout.addLayout(filt)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Descrição", "Status", "Estimativa", "Decorrido", "Eficiência"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

    def carregar_montadores(self):
        colabs = self.db.listar_colaboradores()
        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.addItem("Todos", None)
        for cid, nome, *_ in colabs:
            self.combo.addItem(nome, cid)
        self.combo.blockSignals(False)

    def carregar(self):
        self.carregar_montadores()
        mid = self.combo.currentData()
        ops = self.db.listar_ops(montador_id=mid) if hasattr(self.db, 'listar_ops') else []
        self.table.setRowCount(0)
        for op in ops:
            row = self.table.rowCount(); self.table.insertRow(row)
            oid, desc, mont, status, data_criacao, ultima, est, real = op
            prog = self.db.progresso_op(oid)
            dec = prog['decorrido'] if prog else None
            kpi = self.db.kpi_op(oid)
            eff = kpi['eficiencia'] if kpi else None
            vals = [oid, desc, status, est, f"{dec:.2f}" if dec is not None else '', f"{eff:.1f}%" if eff else '']
            for c,val in enumerate(vals):
                item = QTableWidgetItem(str(val))
                if c==0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row,c,item)

class KPIsTab(QWidget):
    """Aba simples para exibir indicadores resumidos."""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.atualizar()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.label)
        btn = QPushButton("Atualizar")
        btn.clicked.connect(self.atualizar)
        layout.addWidget(btn)

    def atualizar(self):
        texto = (
            f"Colaboradores: {self.db.contar_colaboradores()}\n"
            f"Clientes: {self.db.contar_clientes()}\n"
            f"Produtos: {self.db.contar_produtos()}\n"
            f"Orçamentos: {self.db.contar_orcamentos()}\n"
            f"OPs: {self.db.contar_ops()}"
        )
        self.label.setText(texto)

class LoginDialog(QDialog):
    """Diálogo simples para autenticação do usuário."""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.login = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        layout = QFormLayout(self)
        self.user_edit = QLineEdit(); self.user_edit.setPlaceholderText("Usuário")
        self.pass_edit = QLineEdit(); self.pass_edit.setPlaceholderText("Senha"); self.pass_edit.setEchoMode(QLineEdit.Password)
        layout.addRow("Usuário:", self.user_edit)
        layout.addRow("Senha:", self.pass_edit)
        btn = QPushButton("Entrar")
        btn.clicked.connect(self.tentar_login)
        layout.addRow(btn)

    def tentar_login(self):
        user = self.user_edit.text().strip()
        pwd = self.pass_edit.text()
        if self.db.verificar_login(user, pwd):
            self.login = user
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos")

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Sistema de Orçamentos")
        self.resize(700, 500)
        self.theme = 'light'
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.tabs = QTabWidget()
        self.col_tab = ColaboradoresTab(self.db)
        self.user_tab = UsuariosTab(self.db)
        self.cli_tab = ClientesTab(self.db)
        self.est_tab = EstoqueTab(self.db)
        self.disc_tab = DiscrepanciasTab(self.db)
        self.orc_tab = OrcamentosTab(self.db)
        self.op_tab = OPTab(self.db)
        self.mont_tab = MontagemTab(self.db)
        self.kpi_tab = KPIsTab(self.db)
        self.tabs.addTab(self.col_tab, "Colaboradores")
        self.tabs.addTab(self.user_tab, "Usuários")
        self.tabs.addTab(self.cli_tab, "Clientes")
        self.tabs.addTab(self.est_tab, "Estoque")
        self.tabs.addTab(self.disc_tab, "Discrepâncias")
        self.tabs.addTab(self.orc_tab, "Orçamentos")
        self.tabs.addTab(self.op_tab, "OPs")
        self.tabs.addTab(self.mont_tab, "Montagem")
        self.tabs.addTab(self.kpi_tab, "KPIs")
        layout.addWidget(self.tabs)

        toolbar = self.addToolBar("Tema")
        self.action_tema = QAction("Tema Escuro", self)
        self.action_tema.setCheckable(True)
        self.action_tema.triggered.connect(self.toggle_tema)
        toolbar.addAction(self.action_tema)

        menu = self.menuBar()
        ajuda_menu = menu.addMenu("Ajuda")
        sobre_action = QAction("Sobre", self)
        sobre_action.triggered.connect(self.mostrar_sobre)
        ajuda_menu.addAction(sobre_action)

    def toggle_tema(self, checked):
        if checked:
            aplicar_estilo_escuro(QApplication.instance())
            self.theme = 'dark'
            self.action_tema.setText("Tema Claro")
        else:
            aplicar_estilo_moderno(QApplication.instance())
            self.theme = 'light'
            self.action_tema.setText("Tema Escuro")

    def mostrar_sobre(self):
        QMessageBox.information(self, "Sobre", "Sistema de or\xE7amentos com IA exclusivo da ER El\xE9trica")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    aplicar_estilo_moderno(app)
    db = DatabaseManager()
    login = LoginDialog(db)
    if login.exec_() == QDialog.Accepted:
        win = MainWindow(db)
        win.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

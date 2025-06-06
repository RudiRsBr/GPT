import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout,
    QLineEdit, QDialog
)
from PyQt5.QtCore import Qt
from database import DatabaseManager

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
        layout.addRow("Nome:", self.nome)
        layout.addRow("Setor:", self.setor)
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

    def get_data(self):
        return self.nome.text().strip(), self.setor.text().strip()

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Gestao de Colaboradores")
        self.resize(600, 400)
        self.init_ui()
        self.carregar()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Setor"])
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
        colaboradores = self.db.listar_colaboradores()
        self.table.setRowCount(0)
        for col in colaboradores:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, val in enumerate(col[:3]):
                item = QTableWidgetItem(str(val))
                if c == 0:
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row, c, item)

    def obter_id_selecionado(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def adicionar(self):
        dlg = ColaboradorDialog(self, db=self.db)
        if dlg.exec_() == QDialog.Accepted:
            nome, setor = dlg.get_data()
            if nome and setor:
                self.db.add_colaborador(nome, setor)
                self.carregar()

    def editar(self):
        cid = self.obter_id_selecionado()
        if not cid:
            QMessageBox.warning(self, "Aviso", "Selecione um colaborador")
            return
        dlg = ColaboradorDialog(self, db=self.db, col_id=cid)
        if dlg.exec_() == QDialog.Accepted:
            nome, setor = dlg.get_data()
            self.db.atualizar_colaborador(cid, nome=nome, setor=setor)
            self.carregar()

    def remover(self):
        cid = self.obter_id_selecionado()
        if not cid:
            QMessageBox.warning(self, "Aviso", "Selecione um colaborador")
            return
        if QMessageBox.question(self, "Confirma", "Remover colaborador?") == QMessageBox.Yes:
            self.db.remover_colaborador(cid)
            self.carregar()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DatabaseManager()
    win = MainWindow(db)
    win.show()
    sys.exit(app.exec_())

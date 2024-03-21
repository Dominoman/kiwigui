import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton, QDialogButtonBox

from mainwindow import Ui_MainWindow
from searchform import Ui_searchform


class SearchForm(QDialog,Ui_searchform):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.save_button=QPushButton("Save")
        self.buttonBox.addButton(self.save_button,QDialogButtonBox.ButtonRole.ActionRole)
        self.save_button.toggled.connect(self.save)
        self.load_button = QPushButton("Load")
        self.buttonBox.addButton(self.load_button, QDialogButtonBox.ButtonRole.ActionRole)
        self.load_button.toggled.connect(self.load)

    def load(self):
        print("xxx")

    def save(self):
        pass


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionE_xit.triggered.connect(self.file_exit)
        self.actionSearch.triggered.connect(self.file_search)

    def file_exit(self):
        sys.exit()

    def file_search(self):
        dlg = SearchForm()
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

import sys
from datetime import date, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton, QDialogButtonBox

from mainwindow import Ui_MainWindow
from searchform import Ui_searchform

DAYS = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


class SearchForm(QDialog, Ui_searchform):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.save_button = QPushButton("Save")
        self.buttonBox.addButton(self.save_button, QDialogButtonBox.ButtonRole.ActionRole)
        self.save_button.toggled.connect(self.save)
        self.load_button = QPushButton("Load")
        self.buttonBox.addButton(self.load_button, QDialogButtonBox.ButtonRole.ActionRole)
        self.load_button.toggled.connect(self.load)
        today = date.today()
        tomorrow = today + timedelta(days=1)
        self.date_from.setDate(today)
        self.date_to.setDate(today)
        self.return_from.setDate(today)
        self.return_to.setDate(today)
        self.return_from.setDate(today)
        self.return_from.setMinimumDate(tomorrow)
        self.return_from.setSpecialValueText(" ")
        self.return_to.setDate(today)
        self.return_to.setMinimumDate(tomorrow)
        self.return_to.setSpecialValueText(" ")
        self.nights_in_dst_from.setValue(-1)
        self.nights_in_dst_from.setSpecialValueText(" ")
        self.nights_in_dst_to.setValue(-1)
        self.nights_in_dst_to.setSpecialValueText(" ")
        self.max_fly_duration.setValue(-1)
        self.max_fly_duration.setSpecialValueText(" ")
        self.price_from.setValue(-1)
        self.price_from.setSpecialValueText(" ")
        self.price_to.setValue(-1)
        self.price_to.setSpecialValueText(" ")
        for control in [self.ret_from_diff_city, self.ret_to_diff_city, self.one_for_city, self.one_per_date]:
            control.setCheckState(Qt.CheckState.PartiallyChecked)

    def load(self):
        print("xxx")

    def save(self):
        pass

    def generate_query(self) -> str:
        query = f"fly_from={self.fly_from.text()}"
        if self.fly_to.text() != "":
            query += f"&fly_to={self.fly_to}"
        d = self.date_from.date().toString("dd/MM/yyyy")
        query += f"&date_from={d}"
        d = self.date_to.date().toString("dd/MM/yyyy")
        query += f"&date_to={d}"
        if self.return_from.text().strip() != "":
            d = self.return_from.date().toString("dd/MM/yyyy")
            query += f"&return_from={d}"
        if self.return_to.text().strip() != "":
            d = self.return_from.date().toString("dd/MM/yyyy")
            query += f"&return_from={d}"
        if self.nights_in_dst_from.text().strip() != "":
            query += f"&nights_in_dst_from={self.nights_in_dst_from.value()}"
        if self.nights_in_dst_to.text().strip() != "":
            query += f"&nights_in_dst_to={self.nights_in_dst_from.value()}"
        if self.max_fly_duration.text().strip() != "":
            query += f"&max_fly_duration={self.max_fly_duration.value()}"
        if self.ret_from_diff_city.checkState() == Qt.CheckState.Checked:
            query += "&ret_from_diff_city=True"
        elif self.ret_from_diff_city.checkState() == Qt.CheckState.Unchecked:
            query += "&ret_from_diff_city=False"
        if self.ret_to_diff_city.checkState() == Qt.CheckState.Checked:
            query += "&ret_to_diff_city=True"
        elif self.ret_to_diff_city.checkState() == Qt.CheckState.Unchecked:
            query += "&ret_to_diff_city=False"
        if self.one_for_city.checkState() == Qt.CheckState.Checked:
            query += "&one_for_city=1"
        elif self.one_for_city.checkState() == Qt.CheckState.Unchecked:
            query += "&one_for_city=0"
        if self.one_per_date.checkState() == Qt.CheckState.Checked:
            query += "&one_per_date=1"
        elif self.one_per_date.checkState() == Qt.CheckState.Unchecked:
            query += "&one_per_date=0"
        if self.adults.value() > 0:
            query += f"&adults={self.adults.value()}"
        if self.children.value() > 0:
            query += f"&children={self.children.value()}"
        if self.infants.value() > 0:
            query += f"&infants={self.infants.value()}"
        if self.selected_cabins.currentIndex() > 0:
            query += f"&selected_cabins={'MWCF'[self.selected_cabins.currentIndex() - 1]}"
        if self.mix_with_cabins.currentIndex() > 0:
            query += f"&mix_with_cabins={'MWCF'[self.mix_with_cabins.currentIndex() - 1]}"
        if self.adult_hold_bag.text() != "":
            query += f"&adult_hold_bag={self.adult_hold_bag}"
        if self.adult_hand_bag.text() != "":
            query += f"&adult_hand_bag={self.adult_hand_bag}"
        if self.child_hold_bag.text() != "":
            query += f"&child_hold_bag={self.child_hold_bag}"
        if self.child_hand_bag.text() != "":
            query += f"&child_hand_bag={self.child_hand_bag}"
        for item in self.fly_days.selectedItems():
            query += f"&fly_days={DAYS.index(item.text())}"
        if self.fly_days_type.currentIndex() != 0:
            query += f"&fly_days_type={self.fly_days_type.currentText()}"
        for item in self.ret_fly_days.selectedItems():
            query += f"&ret_fly_days={DAYS.index(item.text())}"
        if self.ret_fly_days_type.currentIndex() != 0:
            query += f"&ret_fly_days_type={self.ret_fly_days_type.currentText()}"
        if self.only_working_days.checkState() == Qt.CheckState.Checked:
            query += "&only_working_days=true"
        elif self.only_working_days.checkState() == Qt.CheckState.Unchecked:
            query += "&only_working_days=false"
        if self.only_weekends.checkState() == Qt.CheckState.Checked:
            query += "&only_weekends=true"
        elif self.only_weekends.checkState() == Qt.CheckState.Unchecked:
            query += "&only_weekends=false"
        if self.partner_market.text() != "":
            query += f"&partner_market={self.partner_market.text()}"
        if self.currency.currentIndex() != 0:
            query += f"&curr={self.currency.currentText()}"
        if self.locale.currentIndex() != 0:
            query += f"&local={self.locale.currentText()}"
        if self.price_from.value() != 0:
            query += f"&price_from={self.price_from.text()}"
        if self.price_to.value() != 0:
            query += f"&price_to={self.price_to.text()}"
        if self.dtime_from.currentIndex() > 0:
            query += f"&dtime_from={self.dtime_from.currentText()}"
        if self.dtime_to.currentIndex() > 0:
            query += f"&dtime_to={self.dtime_to.currentText()}"
        if self.atime_from.currentIndex() > 0:
            query += f"&atime_from={self.atime_from.currentText()}"
        if self.atime_to.currentIndex() > 0:
            query += f"&atime_to={self.atime_to.currentText()}"
        if self.ret_dtime_from.currentIndex() > 0:
            query += f"&ret_dtime_from={self.ret_dtime_from.currentText()}"
        if self.ret_dtime_to.currentIndex() > 0:
            query += f"&ret_dtime_to={self.ret_dtime_to.currentText()}"
        if self.ret_atime_from.currentIndex() > 0:
            query += f"&ret_atime_from={self.ret_atime_from.currentText()}"
        if self.ret_atime_to.currentIndex() > 0:
            query += f"&ret_atime_to={self.ret_atime_to.currentText()}"
        if self.stopover_from.text()!="0:00":
            query += f"&stopover_from={self.stopover_from.text()}"
        if self.stopover_to.text()!="0:00":
            query += f"&stopover_to={self.stopover_to.text()}"

        return query


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
        print(dlg.generate_query())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

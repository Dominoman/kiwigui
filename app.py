import sys
from datetime import date, timedelta
from urllib.parse import urlencode

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
        for control in [self.ret_from_diff_city, self.ret_to_diff_city, self.one_for_city, self.one_per_date,self.only_working_days, self.only_weekends,self.conn_on_diff_airport,self.ret_from_diff_airport,self.ret_to_diff_airport]:
            control.setCheckState(Qt.CheckState.PartiallyChecked)

    def load(self):
        print("xxx")

    def save(self):
        pass

    def generate_query(self) -> str:
        def check_tristate_to_bool(widget):
            if widget.checkState() == Qt.CheckState.PartiallyChecked:
                return None
            return widget.checkState() == Qt.CheckState.Checked

        def check_tristate_to_int(widget):
            if widget.checkState() == Qt.CheckState.PartiallyChecked:
                return None
            return 1 if widget.checkState() == Qt.CheckState.Checked else 0

        query_params = {
            "fly_from": self.fly_from.text(),
            "fly_to": self.fly_to.text() or None,
            "date_from": self.date_from.date().toString("dd/MM/yyyy"),
            "date_to": self.date_to.date().toString("dd/MM/yyyy"),
            "return_from": self.return_from.date().toString("dd/MM/yyyy") if self.return_from.text().strip() else None,
            "return_to": self.return_to.date().toString("dd/MM/yyyy") if self.return_to.text().strip() else None,
            "nights_in_dst_from": self.nights_in_dst_from.value() if self.nights_in_dst_from.text().strip() else None,
            "nights_in_dst_to": self.nights_in_dst_to.value() if self.nights_in_dst_to.text().strip() else None,
            "max_fly_duration": self.max_fly_duration.value() if self.max_fly_duration.text().strip() else None,
            "ret_from_diff_city": check_tristate_to_bool(self.ret_from_diff_city),
            "ret_to_diff_city": check_tristate_to_bool(self.ret_to_diff_city),
            "one_for_city": check_tristate_to_int(self.one_for_city),
            "one_per_date": check_tristate_to_bool(self.one_per_date),
            "adults": self.adults.value() if self.adults.value() > 0 else None,
            "children": self.children.value() if self.children.value() > 0 else None,
            "infants": self.infants.value() if self.infants.value() > 0 else None,
            "selected_cabins": 'MWCF'[
                self.selected_cabins.currentIndex() - 1] if self.selected_cabins.currentIndex() > 0 else None,
            "mix_with_cabins": 'MWCF'[
                self.mix_with_cabins.currentIndex() - 1] if self.mix_with_cabins.currentIndex() > 0 else None,
            "adult_hold_bag": self.adult_hold_bag.text() or None,
            "adult_hand_bag": self.adult_hand_bag.text() or None,
            "child_hold_bag": self.child_hold_bag.text() or None,
            "child_hand_bag": self.child_hand_bag.text() or None,
            "fly_days": [DAYS.index(item.text()) for item in self.fly_days.selectedItems()],
            "fly_days_type": self.fly_days_type.currentText() if self.fly_days_type.currentIndex() != 0 else None,
            "ret_fly_days": [DAYS.index(item.text()) for item in self.ret_fly_days.selectedItems()],
            "ret_fly_days_type": self.ret_fly_days_type.currentText() if self.ret_fly_days_type.currentIndex() != 0 else None,
            "only_working_days": check_tristate_to_bool(self.only_working_days),
            "only_weekends": check_tristate_to_bool(self.only_weekends),
            "partner_market": self.partner_market.text() or None,
            "curr": self.currency.currentText() if self.currency.currentIndex() != 0 else None,
            "local": self.locale.currentText() if self.locale.currentIndex() != 0 else None,
            "price_from": self.price_from.text() if self.price_from.value() != 0 else None,
            "price_to": self.price_to.text() if self.price_to.value() != 0 else None,
            "dtime_from": self.dtime_from.currentText() if self.dtime_from.currentIndex() > 0 else None,
            "dtime_to": self.dtime_to.currentText() if self.dtime_to.currentIndex() > 0 else None,
            "atime_from": self.atime_from.currentText() if self.atime_from.currentIndex() > 0 else None,
            "atime_to": self.atime_to.currentText() if self.atime_to.currentIndex() > 0 else None,
            "ret_dtime_from": self.ret_dtime_from.currentText() if self.ret_dtime_from.currentIndex() > 0 else None,
            "ret_dtime_to": self.ret_dtime_to.currentText() if self.ret_dtime_to.currentIndex() > 0 else None,
            "stopover_from": self.stopover_from.text() if self.stopover_from.text() != "0:00" else None,
            "stopover_to": self.stopover_to.text() if self.stopover_to.text() != "0:00" else None,
            "max_stopovers": self.max_stopovers.value() if self.max_stopovers.value()!=0 else None,
            "max_sector_stopovers": self.max_sector_stopovers.value() if self.max_sector_stopovers.value() != 0 else None,
            "conn_on_diff_airport": check_tristate_to_int(self.conn_on_diff_airport),
            "ret_from_diff_airport": check_tristate_to_int(self.ret_from_diff_airport),
            "ret_to_diff_airport": check_tristate_to_int(self.ret_to_diff_airport),
        }
        # Remove None values
        query_params = {k: v for k, v in query_params.items() if v is not None}
        return urlencode(query_params, doseq=True)


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

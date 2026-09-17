from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit
)

import sys


class SeatingGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seating optimiser")
        self.resize(1000, 700)

        self.guest_names = []

        self.couples = []

        self.singles = []

        main_layout = QVBoxLayout()

        # guests

        guests_label = QLabel("Guests")

        self.guest_list = QListWidget()

        guest_controls = QHBoxLayout()

        self.guest_input = QLineEdit()
        self.guest_input.setPlaceholderText("Guest name")

        add_guest_btn = QPushButton("Add")
        remove_guest_btn = QPushButton("Remove")

        add_guest_btn.clicked.connect(self.add_guest)
        remove_guest_btn.clicked.connect(self.remove_guest)

        guest_controls.addWidget(self.guest_input)
        guest_controls.addWidget(add_guest_btn)
        guest_controls.addWidget(remove_guest_btn)

        # couples

        couples_label = QLabel("Couples")

        self.couples_list = QListWidget()

        couples_controls = QHBoxLayout()

        # dropdown list for couples
        self.person1_combo = QComboBox()
        self.person2_combo = QComboBox()

        add_couple_btn = QPushButton("Add")
        add_couple_btn.clicked.connect(self.add_couple)

        remove_couple_btn = QPushButton("Remove")
        remove_couple_btn.clicked.connect(self.remove_couple)

        couples_controls.addWidget(self.person1_combo)
        couples_controls.addWidget(self.person2_combo)
        couples_controls.addWidget(add_couple_btn)
        couples_controls.addWidget(remove_couple_btn)

        # relations

        relations_label = QLabel("Relations")

        self.relations_table = QTableWidget()

        # output

        calculate_btn = QPushButton("Find best solution")
        calculate_btn.clicked.connect(self.calculate)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        # layout

        main_layout.addWidget(guests_label)
        main_layout.addWidget(self.guest_list)
        main_layout.addLayout(guest_controls)

        main_layout.addWidget(couples_label)
        main_layout.addWidget(self.couples_list)
        main_layout.addLayout(couples_controls)

        main_layout.addWidget(relations_label)
        main_layout.addWidget(self.relations_table)

        main_layout.addWidget(calculate_btn)

        main_layout.addWidget(QLabel("Output"))
        main_layout.addWidget(self.result_box)

        self.setLayout(main_layout)

    def add_guest(self):
        """
        Function adds guest to guest_list and couples dropdown list 
        """

        name = self.guest_input.text().strip()

        if not name:
            return

        self.guest_names.append(name)

        self.singles.append(name)

        self.guest_list.addItem(name)

        self.person1_combo.addItem(name)
        self.person2_combo.addItem(name)

        self.update_relations_table()

        self.guest_input.clear()

        self.refresh_combos()

    def remove_guest(self):
        """
        Function removes guest from guest_list 
        """

        row = self.guest_list.currentRow()

        if row < 0:
            return

        self.guest_names.pop(row)

        guest_name = self.guest_names[row]

        if guest_name in self.singles:
            self.singles.remove(guest_name)

        self.guest_list.takeItem(row)

        self.refresh_combos()
        self.update_relations_table()

    def refresh_combos(self):

        self.person1_combo.clear()
        self.person2_combo.clear()

        self.person1_combo.addItems(self.singles)
        self.person2_combo.addItems(self.singles)

    def add_couple(self):
        """
        Function that creates a couple out of singles (person can be only in 1 couple)
        """

        person1 = self.person1_combo.currentText()
        person2 = self.person2_combo.currentText()

        if person1 == person2:
            return

        # check if person is in some couple already
        for p1, p2 in self.couples:
            if person1 in (p1, p2):
                return

            if person2 in (p1, p2):
                return

        self.couples.append((person1, person2))

        self.couples_list.addItem(
            f"{person1} - {person2}"
        )

        # relation of couple must be 100
        idx1 = self.guest_names.index(person1)
        idx2 = self.guest_names.index(person2)

        item1 = self.relations_table.item(idx1, idx2)
        item2 = self.relations_table.item(idx2, idx1)

        item1.setText("100")
        item2.setText("100")

        # removes couple from dropdown list
        self.singles.remove(person1)
        self.singles.remove(person2)
        self.refresh_combos()


    def remove_couple(self):
        """
        Function that removes couple and turns them into singles
        """

        row = self.couples_list.currentRow()

        if row < 0:
            return

        person1, person2 = self.couples[row]

        idx1 = self.guest_names.index(person1)
        idx2 = self.guest_names.index(person2)


        # default relation
        self.relations_table.item(idx1, idx2).setText("0")
        self.relations_table.item(idx2, idx1).setText("0")

        self.couples.pop(row)
        self.couples_list.takeItem(row)

        # turn them into singles again
        self.singles.append(person1)
        self.singles.append(person2)

        self.refresh_combos()


    #=========================================
    # to rewrite
    #========================================

    def update_relations_table(self):

        n = len(self.guest_names)

        self.relations_table.setRowCount(n)
        self.relations_table.setColumnCount(n)

        self.relations_table.setHorizontalHeaderLabels(
            self.guest_names
        )

        self.relations_table.setVerticalHeaderLabels(
            self.guest_names
        )

        for row in range(n):
            for col in range(n):

                if row == col:
                    item = QTableWidgetItem("-")
                else:
                    item = QTableWidgetItem("0")

                self.relations_table.setItem(row, col, item)

    def calculate(self):

        result = []

        result.append("Tutaj podłączymy SeatingOptimizer\n")

        result.append("Goście:")

        for guest in self.guest_names:
            result.append(f"• {guest}")

        result.append("\nPary:")

        for i in range(self.couples_list.count()):
            result.append(
                self.couples_list.item(i).text()
            )

        self.result_box.setText(
            "\n".join(result)
        )

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SeatingGUI()
    window.show()

    sys.exit(app.exec())
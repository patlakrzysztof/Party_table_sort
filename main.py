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

from PySide6.QtCore import Qt

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
        self.guest_list.setSortingEnabled(True)

        guest_controls = QHBoxLayout()

        self.guest_input = QLineEdit()
        self.guest_input.setPlaceholderText("Guest name")
        self.guest_input.returnPressed.connect(
            self.add_guest
        )

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

        relations_label = QLabel("Relations (from -99 to 99)")

        self.relations = {}

        # dropdown list for relations
        self.relations_person_combo = QComboBox()

        # relation table
        self.relations_table = QTableWidget()
        self.relations_table.setColumnCount(2)
        self.relations_table.setHorizontalHeaderLabels(
            ["Person", "Relation"]
        )

        self.relations_person_combo.currentTextChanged.connect(
            self.update_relations_table
        )

        self.relations_table.itemChanged.connect(
            self.relation_changed
        )

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
        main_layout.addWidget(self.relations_person_combo)
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

        guest_name = self.guest_names[row]

        # checking if guest has a pair
        for couple_idx, (person1, person2) in enumerate(self.couples[:]):

            if guest_name == person1:
                partner = person2

            elif guest_name == person2:
                partner = person1

            else:
                continue

            # removing couple relation (always sorted)
            key = tuple(sorted([person1, person2]))
            self.relations.pop(key, None)

            # remove a couple
            self.couples.pop(couple_idx)
            self.couples_list.takeItem(couple_idx)

            # partner turns into single
            if partner not in self.singles:
                self.singles.append(partner)

            break

        else: # guest is single
            self.singles.remove(guest_name)

        # removing guests relations
        for key in list(self.relations.keys()):
            if guest_name in key:
                del self.relations[key]

        self.guest_names.pop(row)

        self.guest_list.takeItem(row)

        self.refresh_combos()
        self.update_relations_table()

    def refresh_combos(self):
        """
        Helper function that refreshes combos for couples
        """

        self.person1_combo.clear()
        self.person2_combo.clear()

        self.person1_combo.addItems(sorted(self.singles))

        self.person2_combo.addItems(sorted(self.singles))
        
        self.relations_person_combo.clear()
        self.relations_person_combo.addItems(sorted(self.guest_names))

        self.update_relations_table()

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

        # relation of couple must be 100 (always sorted)
        key = tuple(sorted([person1, person2]))
        self.relations[key] = 100

        self.update_relations_table()

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

        # deleting relation
        key = tuple(sorted([person1, person2]))
        self.relations.pop(key, None)

        self.couples.pop(row)
        self.couples_list.takeItem(row)

        # turn them into singles again
        self.singles.append(person1)
        self.singles.append(person2)

        self.refresh_combos()


    def update_relations_table(self):
        """
        Function that updates the relations table that is being viewed
        """

        selected = self.relations_person_combo.currentText()

        self.relations_table.blockSignals(True)

        if not selected:
            self.relations_table.setRowCount(0)
            self.relations_table.blockSignals(False)
            return

        others = sorted([ person for person in self.guest_names if person != selected ])

        self.relations_table.setRowCount(len(others))

        for row, other in enumerate(others):

            name_item = QTableWidgetItem(other)

            # cannot change name of the row
            name_item.setFlags(
                name_item.flags() & ~Qt.ItemIsEditable
            )

            # sorted for a dictionary
            key = tuple(sorted([selected, other]))

            if key in self.relations:
                value = str(self.relations[key])
            else:
                value = "-"

            relation_item = QTableWidgetItem(value)

            # couples are not editable (mocked 100)
            if key in self.relations and self.relations[key] == 100:
                relation_item.setFlags(
                    relation_item.flags() & ~Qt.ItemIsEditable
                )

            self.relations_table.setItem(row, 0, name_item)
            self.relations_table.setItem(row, 1, relation_item)

        self.relations_table.blockSignals(False)

    def relation_changed(self, element):
        """
        Function that changes the relation of an element
        """

        # react only to a relation value changes
        if element.column() != 1:
            return

        selected = self.relations_person_combo.currentText()

        if not selected:
            return

        other = self.relations_table.item(element.row(),0).text()

        value = element.text().strip()

        # key must always be sorted
        key = tuple(sorted([selected, other]))

        # deleting a relation
        if value == "-":
            self.relations.pop(key, None)
            return

        # relation must be an intinger
        try:
            relation = int(value)
        except ValueError:
            self.update_relations_table()
            return

        # relation must be between -99 and 99
        if relation < -99 or relation > 99:
            self.update_relations_table()
            return

        self.relations[key] = relation

    def calculate(self):

        result = []

        result.append("SeatingOptimizer\n")

        result.append("Guests:")

        for guest in self.guest_names:
            result.append(f"• {guest}")

        result.append("Couples:")

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
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
    QTextEdit,
    QFileDialog,
    QSplitter
)

from PySide6.QtCore import Qt

import sys

from optimiser import SeatingOptimizer

class SeatingGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seating optimiser")
        self.resize(1400, 900)

        self.guest_names = []

        self.couples = []

        self.singles = []

        self.tables_capacity = []

        main_layout = QVBoxLayout()

        left_layout = QVBoxLayout()

        right_layout = QVBoxLayout()

        top_splitter = QSplitter(Qt.Horizontal)

        main_splitter = QSplitter(Qt.Vertical)

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

        # tables

        tables_label = QLabel("Tables ( Capacity x Count )")

        self.tables_list = QListWidget()

        tables_controls = QHBoxLayout()

        self.table_capacity_input = QLineEdit()
        self.table_capacity_input.setPlaceholderText("Capacity")

        self.table_count_input = QLineEdit()
        self.table_count_input.setPlaceholderText("Count")

        add_table_btn = QPushButton("Add")
        remove_table_btn = QPushButton("Remove")

        add_table_btn.clicked.connect(self.add_table)
        remove_table_btn.clicked.connect(self.remove_table)

        self.table_capacity_input.returnPressed.connect(self.add_table)

        self.table_count_input.returnPressed.connect(self.add_table)

        tables_controls.addWidget(self.table_capacity_input)
        tables_controls.addWidget(self.table_count_input)
        tables_controls.addWidget(add_table_btn)
        tables_controls.addWidget(remove_table_btn)

        # relations

        relations_label = QLabel("Relations (from -99 to 99)")

        self.relations = {}

        # dropdown list for relations
        self.relations_person_combo = QComboBox()

        # relation table
        self.relations_table = QTableWidget()
        self.relations_table.setColumnCount(2)
        self.relations_table.setHorizontalHeaderLabels(["Person", "Relation"])

        self.relations_person_combo.currentTextChanged.connect(self.update_relations_table)

        self.relations_table.itemChanged.connect(self.relation_changed)

        # algorithm settings

        self.summary_label = QLabel("Guests: 0 | Seats: 0")

        settings_label = QLabel("Algorithm settings")

        settings_layout = QHBoxLayout()

        self.iterations_input = QLineEdit()
        self.iterations_input.setPlaceholderText("Iterations")
        self.iterations_input.setText("1000")

        settings_layout.addWidget(QLabel("Iterations:"))

        settings_layout.addWidget(self.iterations_input)

        # output

        calculate_btn = QPushButton("Find best solution")
        calculate_btn.clicked.connect(self.calculate)

        save_btn = QPushButton("Save output")
        save_btn.clicked.connect(self.save_output)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        # layout

        # left panel
        left_layout.addWidget(guests_label)
        left_layout.addWidget(self.guest_list)
        left_layout.addLayout(guest_controls)

        left_layout.addWidget(couples_label)
        left_layout.addWidget(self.couples_list)
        left_layout.addLayout(couples_controls)

        left_layout.addWidget(tables_label)
        left_layout.addWidget(self.tables_list)
        left_layout.addLayout(tables_controls)

        left_layout.addWidget(self.summary_label)

        left_layout.addWidget(settings_label)
        left_layout.addLayout(settings_layout)

        left_layout.addWidget(calculate_btn)
        left_layout.addWidget(save_btn)

        # right panel
        right_layout.addWidget(relations_label)
        right_layout.addWidget(self.relations_person_combo)
        right_layout.addWidget(self.relations_table)

        self.relations_table.setMinimumWidth(400)

        # splitters
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # output panel
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)

        output_layout.addWidget(QLabel("Output"))
        output_layout.addWidget(self.result_box)

        # top splitter (left / right)
        top_splitter = QSplitter(Qt.Horizontal)

        top_splitter.addWidget(left_widget)
        top_splitter.addWidget(right_widget)

        top_splitter.setStretchFactor(0, 1)
        top_splitter.setStretchFactor(1, 2)

        # main splitter (top / bottom)
        main_splitter = QSplitter(Qt.Vertical)

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(output_widget)

        main_splitter.setStretchFactor(0, 3)
        main_splitter.setStretchFactor(1, 1)

        # main window layout
        main_layout.addWidget(main_splitter)

        self.setLayout(main_layout)

        self.update_counts()


    def add_table(self):
        """
        Function that adds tables of given capacity
        """

        try:
            capacity = int(
                self.table_capacity_input.text()
            )

            count = int(
                self.table_count_input.text()
            )

        except ValueError:
            return

        if capacity <= 0 or count <= 0:
            return

        for _ in range(count):
            self.tables_capacity.append(capacity)

        self.refresh_tables_list()

        self.table_capacity_input.clear()
        self.table_count_input.clear()

        self.update_counts()

    def remove_table(self):
        """
        Function that removes table group.
        """

        row = self.tables_list.currentRow()

        if row < 0:
            return

        capacities = {}

        for capacity in self.tables_capacity:
            capacities[capacity] = capacities.get(capacity, 0) + 1

        selected_capacity = sorted(capacities)[row]

        # remove all tables with this capacity
        self.tables_capacity = [capacity for capacity in self.tables_capacity if capacity != selected_capacity]

        self.refresh_tables_list()
        self.update_counts()

    def refresh_tables_list(self):
        """
        Helper function that refreshes tables list
        """

        self.tables_list.clear()

        capacities = {}

        for capacity in self.tables_capacity:

            if capacity not in capacities:
                capacities[capacity] = 0

            capacities[capacity] += 1

        for capacity in sorted(capacities):

            count = capacities[capacity]

            self.tables_list.addItem(
                f"{capacity} x {count}"
            )

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

        self.update_counts()

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

        self.update_counts()

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

    def update_counts(self):
        """
        Helper function that counts guests and seats
        """
        guests_count = len(self.guest_names)
        seats_count = sum(self.tables_capacity)

        self.summary_label.setText(
            f"Guests: {guests_count} | Seats: {seats_count}"
        )

    def build_relations_matrix(self):
        """
        Helper function that builds a relations matrix for SeatingOptimiser class
        """

        n = len(self.guest_names)

        relations_matrix = [
            [None if i == j else 0 for j in range(n)]
            for i in range(n)
        ]

        for (person1, person2), relation in self.relations.items():

            idx1 = self.guest_names.index(person1)
            idx2 = self.guest_names.index(person2)

            relations_matrix[idx1][idx2] = relation
            relations_matrix[idx2][idx1] = relation

        return relations_matrix

    def build_couples_index_table(self):
        """
        Helper function that makes couples indexed table for SeatingOptimiser class
        """

        couples_indices = []

        for person1, person2 in self.couples:

            idx1 = self.guest_names.index(person1)
            idx2 = self.guest_names.index(person2)

            couples_indices.append([idx1, idx2])

        return couples_indices

    def save_output(self):
        """
        Function that saves output to a text file.
        """

        text = self.result_box.toPlainText()

        if not text:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save result",
            "seating_result.txt",
            "Text files (*.txt);;All files (*)"
        )

        if not filename:
            return

        # writing output to a file
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)

        except Exception as e:
            self.result_box.append(
                f"\n\nSave error:\n{e}"
            )

    def calculate(self):
        """
        Function that runs the SeatingOptimiser class and calculates the output using it
        """

        try:

            iterations = int(
                self.iterations_input.text()
            )

        except ValueError:

            self.result_box.setText("Iterations must be an integer.")
            return

        if iterations <= 0:

            self.result_box.setText("Iterations must be positive.")
            return

        try:

            relations_matrix = self.build_relations_matrix()

            couples_indices = self.build_couples_index_table()

            # making a class
            optimizer = SeatingOptimizer(
                guest_list = self.guest_names,
                guest_relations = relations_matrix,
                couples_list = couples_indices,
                tables_capacity = self.tables_capacity,
                max_iterations = iterations
            )

            # calculating the output
            best_tables, best_value = (optimizer.find_best_solution())

            result = []

            # writing the output
            result.append(
                f"Best solution value: {best_value}\n(value represents how good are the relations at the tables)"
            )

            result.append("")

            for table_idx, table in enumerate(best_tables):

                result.append(
                    f"Table {table_idx + 1}:"
                )

                guests = []

                for element_idx in table:

                    element = optimizer.elements[element_idx]

                    for guest_idx in element["index"]:

                        guests.append(
                            self.guest_names[guest_idx]
                        )

                result.append(
                    ", ".join(guests)
                )

                result.append("")

            self.result_box.setText(
                "\n".join(result)
            )

        except Exception as e:
            self.result_box.setText(
                f"Error:\n{e}"
            )

            return

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SeatingGUI()
    window.show()

    sys.exit(app.exec())
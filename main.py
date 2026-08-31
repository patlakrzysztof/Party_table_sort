from exceptions import ElementNotAtTable,InitError,NoFreeSeats
import math
import copy


class SeatingOptimizer:

    def __init__(
        self,
        guest_list,
        guest_relations,
        couples_list,
        number_of_tables,
        initial_temperature=100,
        cooling_rate=15,
        max_iterations=1
    ):

        self.guest_list = guest_list
        self.guest_relations = guest_relations
        self.couples_list = couples_list

        self.number_of_tables = number_of_tables

        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations

        self.tables = [[] for _ in range(number_of_tables)]
        self.table_values = [math.inf for _ in range(number_of_tables)]

        total_guests = len(guest_list)
        base_capacity = total_guests // number_of_tables
        remainder = total_guests % number_of_tables

        self.tables_capacity = [
            base_capacity + 1 if i < remainder else base_capacity
            for i in range(number_of_tables)
        ]

        # calculate elements from the start
        self.elements, self.relations = self.calculate_elements()

        # initializing tables
        self.initialize_tables()
        
        # calculate initial table values
        self.table_values = [self.calculate_table_value(self.tables[i]) for i in range(len(self.tables))]
        

    def calculate_elements(self):
        """
        function that calculates all elements and their relations
        and returns them (the list starts with all the couples,
        then are the loners)
        """

        # our elements table
        elements = []

        # for not doubling couples
        taken_guests = set()

        # adding couples to elements
        for couple in self.couples_list:
            elements.append({
                "index": [couple[0], couple[1]],
                "size": 2
            })

            taken_guests.add(couple[0])
            taken_guests.add(couple[1])

        # adding other guests to elements
        for i in range(len(self.guest_list)):
            if i not in taken_guests:
                elements.append({
                    "index": [i],
                    "size": 1
                })

        # new relations of elements
        relations = [[] for _ in range(len(elements))]

        # making new relation graph for elements (couple relation = sum(partners relations))
        for i, element in enumerate(elements):
            new_relation = [0 for _ in range(len(elements))]
            new_relation[i] = None

            if element["size"] == 1:
                index1 = element["index"][0]
                for j, element2 in enumerate(elements):
                    if i == j:
                        continue
                    elif element2["size"] == 1:
                        new_relation[j] = self.guest_relations[index1][element2["index"][0]]
                    elif element2["size"] == 2:
                        couple = element2["index"]
                        new_relation[j] = self.guest_relations[index1][couple[0]] + self.guest_relations[index1][couple[1]]
            elif element["size"] == 2:
                index1 = element["index"][0]
                index2 = element["index"][1]
                for j, element2 in enumerate(elements):
                    if i == j:
                        continue
                    elif element2["size"] == 1:
                        index3 = element2["index"][0]
                        new_relation[j] = self.guest_relations[index1][index3] + self.guest_relations[index2][index3]
                    elif element2["size"] == 2:
                        couple = element2["index"]
                        new_relation[j] = (
                            self.guest_relations[index1][couple[0]]
                            + self.guest_relations[index1][couple[1]]
                            + self.guest_relations[index2][couple[0]]
                            + self.guest_relations[index2][couple[1]]
                        )

            relations[i] = new_relation

        return elements, relations

    def initialize_tables(self):
        remaining_capacity = self.tables_capacity.copy()

        for element_idx, element in enumerate(self.elements):
            size = element["size"]

            for table_idx in range(self.number_of_tables):
                if remaining_capacity[table_idx] >= size:
                    self.tables[table_idx].append(element_idx)
                    remaining_capacity[table_idx] -= size
                    break
            else:
                raise InitError(
                f"Could not place element {element_idx}"
                f"(size={size}) at any table"
            )

    def calculate_table_value(self, table):
        """
        helper function that calculates the value
        of the table from relations table
        """
        res = 0
        for i in range(len(table)):
            for j in range(i + 1, len(table)):
                if (self.relations[table[i]][table[j]] is None or self.relations[table[j]][table[i]] is None):
                    raise TypeError("Relation value is None")
                res += self.relations[table[i]][table[j]]
                res += self.relations[table[j]][table[i]]
        return res

    def update_table_values(self, *table_indices):
        """
        function that updates table values of tables given as arguments
        """
        for idx in table_indices:
            self.table_values[idx] = self.calculate_table_value(self.tables[idx])

    def calculate_solution_value(self):
        """
        function that calculates value of the current solution
        """
        return sum(self.calculate_table_value(table) for table in self.tables)

    def calculate_table_size(self, table):
        """
        helper function that calculates how many guests are currently
        sitting at a table (couples count as 2, singles as 1)
        """
        return sum(self.elements[i]["size"] for i in table)

    def check_element_move(
            self,
            table_from_idx,
            element,
            table_to_idx
    ):
        """
        helper function that calculates if moving element
        is positive or negative
        (returns a tuple of numbers that represents overall values change 
        and a value change for both tables (>0 is positive and <0 is negative))
        """

        if table_from_idx == table_to_idx:
            return (0, 0, 0)

        table_from = self.tables[table_from_idx]
        table_to = self.tables[table_to_idx]

        if element not in table_from:
            raise ElementNotAtTable(f"Element {element} is not sitting at this table ({table_from_idx})")

        element_size = self.elements[element]["size"]

        new_table_to_size = self.calculate_table_size(table_to) + element_size

        if new_table_to_size > self.tables_capacity[table_to_idx]:
            raise NoFreeSeats(f"Move cannot happen due to lack of seats at the table {table_to_idx}")

        old_table_from_value = self.table_values[table_from_idx]
        old_table_to_value = self.table_values[table_to_idx]

        new_table_from_value = old_table_from_value
        new_table_to_value = old_table_to_value

        # calculate new value of the table_from
        for i in range(len(table_from)):
            if table_from[i] != element:
                new_table_from_value -= (
                    self.relations[table_from[i]][element]
                    + self.relations[element][table_from[i]]
                )

        # calculate new value of the table_to
        for i in range(len(table_to)):
            new_table_to_value += self.relations[table_to[i]][element] + self.relations[element][table_to[i]]

        table_from_diff = new_table_from_value - old_table_from_value
        table_to_diff = new_table_to_value - old_table_to_value
        # if change is for good for a table diff number should be > 0

        # checking if the change is for good for the main algorithm
        return (table_from_diff + table_to_diff, table_from_diff, table_to_diff)

    def move_element(
            self,
            table_from_idx,
            element,
            table_to_idx
        ):
            """
            function that move element between tables
            """

            if table_from_idx == table_to_idx:
                return

            table_from = self.tables[table_from_idx]

            if element not in table_from:
                        raise ElementNotAtTable(f"Element {element} is not sitting at this table ({table_from_idx})")

            self.tables[table_from_idx].remove(element)
            self.tables[table_to_idx].append(element)
            

    def check_elements_swap(
        self,
        table1_idx,
        table2_idx,
        element1,
        element2
    ):
        """
        helper function that calculates if element swap
        is positive or negative
        (from table1 element1 is taken to table2 and the other way around)
        (returns a tuple of numbers that represents overall values change 
        and a value change for both tables (>0 is positive and <0 is negative))
        """

        table1 = self.tables[table1_idx]
        table2 = self.tables[table2_idx]

        if element1 not in table1:
            raise ElementNotAtTable(f"Element {element1} is not sitting at this table ({table1_idx})")
        
        if element2 not in table2:
            raise ElementNotAtTable(f"Element {element2} is not sitting at this table ({table2_idx})")

        element1_size = self.elements[element1]["size"]
        element2_size = self.elements[element2]["size"]

        new_size_table1 = self.calculate_table_size(table1) - element1_size + element2_size
        new_size_table2 = self.calculate_table_size(table2) - element2_size + element1_size

        if new_size_table1 > self.tables_capacity[table1_idx]:
            raise NoFreeSeats(f"Swap cannot happen due to lack of seats at the table {table1_idx}")
        
        if new_size_table2 > self.tables_capacity[table2_idx]:
            raise NoFreeSeats(f"Swap cannot happen due to lack of seats at the table {table2_idx}")
        
        old_table1_value = self.table_values[table1_idx]
        old_table2_value = self.table_values[table2_idx]

        new_table1_value = old_table1_value
        new_table2_value = old_table2_value

        # calculate new value of the table1
        for i in range(len(table1)):
            if table1[i] != element1:
                new_table1_value -= (
                    self.relations[table1[i]][element1]
                    + self.relations[element1][table1[i]]
                )
                new_table1_value += (
                    self.relations[table1[i]][element2]
                    + self.relations[element2][table1[i]]
                )

        # calculate new value of the table2
        for i in range(len(table2)):
            if table2[i] != element2:
                new_table2_value -= self.relations[table2[i]][element2] + self.relations[element2][table2[i]]
                new_table2_value += self.relations[table2[i]][element1] + self.relations[element1][table2[i]]

        table1_diff = new_table1_value - old_table1_value
        table2_diff = new_table2_value - old_table2_value
        # if change is for good for a table diff number should be > 0

        # checking if the change is for good for the main algorithm
        return (table1_diff + table2_diff, table1_diff, table2_diff)

    def swap_elements(
        self,
        table1_idx,
        table2_idx,
        element1,
        element2
    ):
        """
        function that swap elements between tables
        (element1 from table1 to table2 and the other way for element2)
        """

        table1 = self.tables[table1_idx]
        table2 = self.tables[table2_idx]

        if element1 not in table1:
            raise ElementNotAtTable(f"Element {element1} is not sitting at this table ({table1_idx})")

        if element2 not in table2:
            raise ElementNotAtTable(f"Element {element2} is not sitting at this table ({table2_idx})")

        self.tables[table1_idx].remove(element1)
        self.tables[table1_idx].append(element2)

        self.tables[table2_idx].remove(element2)
        self.tables[table2_idx].append(element1)

        
    
    def acceptance_probability(self, T, diff):
        if diff >= 0:
            return 1.0

        return math.exp(diff / T)

    def find_best_solution(self):

        current_solution = 0
        best_solution = 0
        best_tables = copy.deepcopy(self.tables)

        print(self.tables)

        print(self.elements)

        try:
            print(self.check_elements_swap(0,1,0,4))
            self.swap_elements(0,1,0,4)
            print(self.tables)
        except (ElementNotAtTable,NoFreeSeats) as e:
            print(e)

# guest list
guest_list = [
    "Amelia",
    "Krzysiek",
    "Paweł",
    "Aleksander",
    "Ruda",
    "Mateusz",
    "Gotka",
    "Kamil"
]

# our graph of dependencies [-100,100] - None for self
guest_relations = [
    [None,100,80,-100,40,70,93,-100],    #Amelia
     [100,None,80,-80,30,80,60,-100],    #Krzysiek
     [80,80,None,0,70,80,100,-100],      #Paweł
     [90,-50,0,None,0,0,60,20],        #Aleksander
     [40,30,70,0,None,100,70,-100],      #Ruda
     [80,80,80,0,100,None,40,70],      #Mateusz
     [93,60,100,60,70,40,None,-100],     #Gotka
     [-100,-100,-100,20,-100,70,-100,None] #Kamil
     ]

# couples (couple must sit together)
couples_list = [[0,1],[2,6],[4,5]]

optimizer = SeatingOptimizer(
    guest_list=guest_list,
    guest_relations=guest_relations,
    couples_list=couples_list,
    number_of_tables=3,
)

optimizer.find_best_solution()
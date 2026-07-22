from exceptions import ElementNotAtTable
import math

# number of tables
number_of_tables = 3

# table of tables
tables = [[] for _ in range(number_of_tables)]
table_values = [math.inf for i in range(len(tables))]

# guests
guest_list = ["Amelia","Krzysiek","Paweł","Aleksander","Ruda","Mateusz","Gotka","Kamil"]

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


total_guests = len(guest_list)
base_capasity = total_guests // number_of_tables
remainder = total_guests % number_of_tables

# first tables get one extra seat until all reminder are seated
tables_capasity = [base_capasity + 1 if i < remainder else base_capasity for i in range(number_of_tables)]


def calculate_elements():
    """
    function that calculates all elements and their relations from couples_list, guest_relations and guest_list 
    and returns them
    """
    # our elements table
    elements = []

    # for not doubling couples
    taken_guests = set()

    # adding couples to elements
    for couple in couples_list:
        elements.append({
            "index":[couple[0],couple[1]],
            "size": 2
        })
        taken_guests.add(couple[0])
        taken_guests.add(couple[1])

    # adding other guests to elements
    for i in range(len(guest_list)):
        if i not in taken_guests:
            elements.append({
                "index":[i],
                "size": 1
            })

    # new relations of elements
    relations = [[] for _ in range(len(elements))]

    # making new relation graph for elements (couple relation = sum(partners relations))
    for i,element in enumerate(elements):
        new_relation = [0 for _ in range(len(elements))]
        new_relation[i] = None

        if element["size"] == 1:
            index1 = element["index"][0]
            for j,element2 in enumerate(elements):
                if i==j:
                    continue
                elif element2["size"] == 1:
                    new_relation[j]=guest_relations[index1][element2["index"][0]]
                elif element2["size"] == 2:
                    couple = element2["index"]
                    new_relation[j] = guest_relations[index1][couple[0]] + guest_relations[index1][couple[1]]
        elif element["size"] == 2:
            index1 = element["index"][0]
            index2 = element["index"][1]
            for j,element2 in enumerate(elements):
                if i==j:
                    continue
                elif element2["size"] == 1:
                    index3 = element2["index"][0]
                    new_relation[j] = guest_relations[index1][index3] + guest_relations[index2][index3]
                elif element2["size"] == 2:
                    couple = element2["index"]
                    new_relation[j] = guest_relations[index1][couple[0]] + guest_relations[index1][couple[1]]+guest_relations[index2][couple[0]]+guest_relations[index2][couple[1]]

        relations[i]=new_relation

    return elements,relations


def calculate_table_value(table,relations):
    """
    helper function that calculates the value of the table from relations table
    """
    res = 0
    for i in range(len(table)):
        for j in range(i+1,len(table)):
            if (relations[table[i]][table[j]] is None or relations[table[j]][table[i]] is None):
                raise TypeError("Relation value is None")
            res += relations[table[i]][table[j]]
            res += relations[table[j]][table[i]]
    return res


def calculate_table_size(table, elements):
    """
    helper function that calculates how many guests are actually
    sitting at a table (couples count as 2, singles as 1)
    """
    return sum(elements[i]["size"] for i in table)


def check_elements_swap(table1_idx, table2_idx, element1, element2, table_values, relations):
    """
    helper function that calculates if element swap is positive or negative 
    (from table1 element1 is taken to table2 and the other way around)
    (returns a tuple of numbers that represents overall values change and a value change for both tables (>0 is positive and <0 is negative))
    """
    table1 = tables[table1_idx]
    old_table1_value = table_values[table1_idx]
    new_table1_value = old_table1_value

    table2 = tables[table2_idx]
    old_table2_value = table_values[table2_idx]
    new_table2_value = old_table2_value

    if element1 not in table1:
        raise ElementNotAtTable(f"Element {element1} is not sitting at this table ({table1_idx})")
    
    if element2 not in table2:
        raise ElementNotAtTable(f"Element {element2} is not sitting at this table ({table2_idx})")
    
    # calculate new value of the table1
    for i in range(len(table1)):
        if table1[i] != element1:
            new_table1_value -= (relations[table1[i]][element1] + relations[element1][table1[i]])
            new_table1_value += (relations[table1[i]][element2] + relations[element2][table1[i]])

    # calculate new value of the table2
    for i in range(len(table2)):
        if table2[i] != element2:
            new_table2_value -= (relations[table2[i]][element2] + relations[element2][table2[i]])
            new_table2_value += (relations[table2[i]][element1] + relations[element1][table2[i]])
            
    table1_diff = new_table1_value - old_table1_value
    table2_diff = new_table2_value - old_table2_value
    # if change is for good for a table diff number should be > 0

    # checking if the change is for good for the main algorithm
    return (table1_diff+table2_diff, table1_diff, table2_diff)


def swap_elements(table1_idx, table2_idx, element1, element2):
    """
    function that swap elements between tables
    (element1 from table1 to table2 and the other way for element2)
    """
    table1 = tables[table1_idx]
    table2 = tables[table2_idx]

    if element1 not in table1:
        raise ElementNotAtTable(f"Element {element1} is not sitting at this table ({table1_idx})")
    
    if element2 not in table2:
        raise ElementNotAtTable(f"Element {element2} is not sitting at this table ({table2_idx})")

    for i in range(len(table1)):
        if table1[i]==element1:
            tables[table1_idx][i]=element2
            break

    for i in range(len(table2)):
        if table2[i]==element2:
            tables[table2_idx][i]=element1
            break



def acceptance_probability(T,diff):
    """
    helper function for calculating acceptance probability (using diff and T) for simulated annealing algorithm
    """
    return math.exp(-diff/T)


def find_best_solution(tables,iterations):
    """
    main function that is trying to find the best seats for all the tables using simulated annealing (heuristic)
    """
    elements,relations = calculate_elements()

    # making initial tables
    for i in range(len(elements)):
        tables[i%number_of_tables].append(i)

    # calculates initial table values
    table_values = [calculate_table_value(tables[i],relations) for i in range(len(tables))]





    print(tables)
    print(elements)

    try:
        print(check_elements_swap(0,1,0,4,table_values,relations))
        swap_elements(0,1,0,4)
        print(tables)
    except ElementNotAtTable as e:
        print(e)

    

find_best_solution(tables,1)


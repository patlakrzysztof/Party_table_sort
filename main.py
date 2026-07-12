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
    return sum(elements[idx]["size"] for idx in table)


def check_elements_swap(table_idx,element_in,element_out,table_values,relations):
    """
    helper function that calculates if element swap is positive or negative
    """
    table = tables[table_idx]
    new_table_value = table_values[table_idx]

    if element_out not in table:
        raise ElementNotAtTable(f"Element {element_out} is not sitting at this table")
    
    for i in range(len(table)):
        if table[i] != element_out:
            new_table_value -= (relations[table[i]][element_out] + relations[element_out][table[i]])
            new_table_value += (relations[table[i]][element_in] + relations[element_in][table[i]])
            
    return new_table_value>table_values[table_idx]


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
        print(check_elements_swap(0,4,3,table_values,relations))
    except ElementNotAtTable as e:
        print(e)
    

find_best_solution(tables,1)


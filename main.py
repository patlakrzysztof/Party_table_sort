# guests
guests = ["Amelia","Krzysiek","Paweł","Aleksander","Ruda","Mateusz","Gotka"]

# our graph of dependencies [-100,100] - None for self
guest_relations = [[None,100,80,-100,40,70,93], #Amelia
     [100,None,80,-80,30,80,60], #Krzysiek
     [80,80,None,0,70,80,100], #Paweł
     [90,-50,0,None,0,0,60], #Aleksander
     [40,30,70,0,None,100,70], #Ruda
     [80,80,80,0,100,None,40], #Mateusz
     [93,60,100,60,70,40,None], #Gotka
     ]

# marriages and couples (couple must sit together)
couples = [[0,1],[2,6],[4,5]]

# our elements to assign to table
elements = []

# for not doubling couples
taken_guests = set()

# adding couples to elements
for couple in couples:
    elements.append({
        "index":[couple[0],couple[1]],
        "size": 2
    })
    taken_guests.add(couple[0])
    taken_guests.add(couple[1])

# adding other guests to elements
for i in range(len(guests)):
    if i not in taken_guests:
        elements.append({
            "index":i,
            "size": 1
        })

relations = [[] for _ in range(len(elements))]

# making new relation graph for elements
for i,element in enumerate(elements):
    new_relation = [0 for _ in range(len(elements))]
    new_relation[i] = None

    if element["size"]==1:
        index1 = element["index"]
        for j,element2 in enumerate(elements):
            if i==j:
                continue
            elif element2["size"]==1:
                new_relation[j]=guest_relations[index1][element2["index"]]
            elif element2["size"]==2:
                couple = element2["index"]
                new_relation[j]=guest_relations[index1][couple[0]]+guest_relations[index1][couple[1]]
    elif element["size"]==2:
        index1 = element["index"][0]
        index2 = element["index"][1]
        for j,element2 in enumerate(elements):
            if i==j:
                continue
            elif element2["size"]==1:
                index3 = element2["index"]
                new_relation[j]=guest_relations[index1][index3]+guest_relations[index2][index3]
            elif element2["size"]==2:
                couple = element2["index"]
                new_relation[j]=guest_relations[index1][couple[0]]+guest_relations[index1][couple[1]]+guest_relations[index2][couple[0]]+guest_relations[index2][couple[1]]

    relations[i]=new_relation



# number of tables
n = 3

# table of tables
tables = [[] for _ in range(n)]

"""
function that calculates the value of the table
"""
def table_value(table,relations):
    res=0
    for i in range(len(table)):
        for j in range(i+1,len(table)):
            if (relations[table[i]][table[j]] is None):
                raise TypeError
            res+=relations[table[i]][table[j]]
    return res


# making initial tables
for i in range(len(elements)):
    tables[i%n].append(i)

print(tables)
print(guest_relations)
print(relations)




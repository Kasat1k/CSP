import networkx as nx
import matplotlib.pyplot as plt

def is_valid(coloring, region, color, constraints):
    for neighbor in constraints[region]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True

def select_unassigned_variable(variables, domains, constraints, coloring):
    # MRV
    unassigned = [v for v in variables if v not in coloring]
    mrv = min(unassigned, key=lambda var: len([color for color in domains if is_valid(coloring, var, color, constraints)]))
    # Degree Heuristic
    degree = sorted(unassigned, key=lambda var: -len([n for n in constraints[var] if n not in coloring]))
    return degree[0] if degree else mrv

def backtrack(coloring, variables, domains, constraints, path_cost):
    if len(coloring) == len(variables):
        return coloring, path_cost

    uncolored = select_unassigned_variable(variables, domains, constraints, coloring)
    
    for color in domains:
        if is_valid(coloring, uncolored, color, constraints):
            coloring[uncolored] = color
            result, cost = backtrack(coloring.copy(), variables, domains, constraints, path_cost + 1)
            if result:
                return result, cost
            coloring.pop(uncolored)
    return None, path_cost


def color_map():
    variables = [ #X_i
        'Вінницька', 'Волинська', 'Дніпропетровська', 'Донецька', 'Житомирська',
        'Закарпатська', 'Запорізька', 'Івано-Франківська', 'Київська', 'Кіровоградська',
        'Луганська', 'Львівська', 'Миколаївська', 'Одеська', 'Полтавська',
        'Рівненська', 'Сумська', 'Тернопільська', 'Харківська', 'Херсонська',
        'Хмельницька', 'Черкаська', 'Чернівецька', 'Чернігівська'
    ]
    domains = ['blue', 'red', 'green', 'yellow']#D_i
    constraints = { #C_i
        'Вінницька': ['Житомирська', 'Київська', 'Черкаська', 'Кіровоградська', 'Одеська', 'Хмельницька'],
        'Волинська': ['Рівненська', 'Львівська'],
        'Дніпропетровська': ['Полтавська', 'Харківська', 'Донецька', 'Запорізька', 'Херсонська', 'Кіровоградська'],
        'Донецька': ['Харківська', 'Дніпропетровська', 'Запорізька', 'Луганська'],
        'Житомирська': ['Рівненська', 'Хмельницька', 'Вінницька', 'Київська'],
        'Закарпатська': ['Львівська', 'Івано-Франківська'],
        'Запорізька': ['Дніпропетровська', 'Донецька', 'Херсонська'],
        'Івано-Франківська': ['Закарпатська', 'Львівська', 'Чернівецька', 'Тернопільська'],
        'Київська': ['Житомирська', 'Чернігівська', 'Черкаська', 'Полтавська', 'Вінницька'],
        'Кіровоградська': ['Черкаська', 'Полтавська', 'Дніпропетровська', 'Херсонська', 'Миколаївська', 'Вінницька'],
        'Луганська': ['Харківська', 'Донецька'],
        'Львівська': ['Волинська', 'Рівненська', 'Тернопільська', 'Івано-Франківська', 'Закарпатська'],
        'Миколаївська': ['Одеська', 'Кіровоградська', 'Херсонська'],
        'Одеська': ['Вінницька', 'Кіровоградська', 'Миколаївська'],
        'Полтавська': ['Черкаська', 'Київська', 'Сумська', 'Харківська', 'Дніпропетровська', 'Кіровоградська'],
        'Рівненська': ['Волинська', 'Житомирська', 'Хмельницька', 'Львівська', 'Тернопільська'],
        'Сумська': ['Чернігівська', 'Полтавська', 'Харківська'],
        'Тернопільська': ['Львівська', 'Рівненська', 'Хмельницька', 'Івано-Франківська', 'Чернівецька'],
        'Харківська': ['Сумська', 'Полтавська', 'Дніпропетровська', 'Луганська', 'Донецька'],
        'Херсонська': ['Запорізька', 'Дніпропетровська', 'Кіровоградська', 'Миколаївська'],
        'Хмельницька': ['Рівненська', 'Житомирська', 'Вінницька', 'Чернівецька', 'Тернопільська'],
        'Черкаська': ['Київська', 'Житомирська', 'Вінницька', 'Кіровоградська', 'Полтавська'],
        'Чернівецька': ['Івано-Франківська', 'Тернопільська', 'Хмельницька'],
        'Чернігівська': ['Київська', 'Сумська']
    }

    G = nx.Graph()
    G.add_nodes_from(variables)
    for region, neighbors in constraints.items():
        for neighbor in neighbors:
            G.add_edge(region, neighbor)

    initial_path_cost = 0
    coloring_solution, final_path_cost = backtrack({}, variables, domains, constraints, initial_path_cost)
    
    if coloring_solution:
        print(f"Solution found with path cost: {final_path_cost}")
        pos = nx.spring_layout(G)
        color_map = [coloring_solution.get(node) for node in G.nodes()]
        nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=3000, edge_color='black', linewidths=1, font_size=12)
        plt.show()
    else:
        print("No solution exists.")

color_map()
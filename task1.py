import networkx as nx
from collections import deque
import matplotlib as _matplotlib
_matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as _plt
matplotlib = _matplotlib
plt = _plt

def task1():
    """
    Завдання 1: Застосування алгоритму максимального потоку для логістики товарів

    Мережа складається з:
    - 2 Термінали (джерела)
    - 4 Склади (проміжні вузли)
    - 14 Магазинів (споживачі)
    """

    # Створюємо граф
    G = nx.DiGraph()

    # Нумерація вузлів (20 вершин згідно з вимогами):
    # 0, 1 - Термінали 1, 2
    # 2, 3, 4, 5 - Склади 1, 2, 3, 4
    # 6-19 - Магазини 1-14

    # Додаємо ребра з пропускною здатністю згідно з таблицею
    edges = create_edges()

    # Додаємо всі ребра до графа
    for u, v, cap in edges:
        G.add_edge(u, v, capacity=cap)

    # Створюємо матрицю пропускної здатності
    num_nodes = 20  # 20 вузлів згідно з вимогами
    capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for u, v, cap in edges:
        capacity_matrix[u][v] = cap

    # Для мультиджерельної задачі створюємо супер-джерело та супер-стік
    # (тільки для обчислення, не входять в основні 20 вершин)
    extended_nodes = 22
    extended_capacity = [[0] * extended_nodes for _ in range(extended_nodes)]

    # Копіюємо існуючі ребра
    for i in range(num_nodes):
        for j in range(num_nodes):
            extended_capacity[i][j] = capacity_matrix[i][j]

    # Супер-джерело (20) -> Термінали
    extended_capacity[20][0] = 10000  # Супер-джерело -> Термінал 1
    extended_capacity[20][1] = 10000  # Супер-джерело -> Термінал 2

    # Магазини -> Супер-стік (21)
    for store in range(6, 20):  # Магазини 1-14
        extended_capacity[store][21] = 10000

    source = 20  # Супер-джерело (для обчислення)
    sink = 21    # Супер-стік (для обчислення)

    # Обчислюємо максимальний потік
    max_flow, flow_matrix = edmonds_karp_with_flow(extended_capacity, source, sink)

    # Виводимо результати
    print("="*80)
    print("ЗАВДАННЯ 1: Застосування алгоритму максимального потоку для логістики товарів")
    print("="*80)
    print(f"\nМаксимальний потік від терміналів до магазинів: {max_flow} одиниць\n")

    # Створюємо таблицю результатів: Термінал -> Магазин
    print("="*80)
    print("ТАБЛИЦЯ РЕЗУЛЬТАТІВ: Фактичний потік від терміналів до магазинів")
    print("="*80)
    print(f"{'Термінал':<15} {'Магазин':<15} {'Фактичний Потік (одиниць)':<30}")
    print("-"*80)

    terminal_flows = {}
    store_flows = {}

    # Обчислюємо потоки від терміналів до магазинів через склади
    for terminal in [0, 1]:  # Термінали 1 та 2
        terminal_name = f"Термінал {terminal + 1}"
        terminal_flows[terminal_name] = 0

        for store in range(6, 20):  # Магазини 1-14
            store_name = f"Магазин {store - 5}"

            # Обчислюємо потік від терміналу до магазину через всі можливі склади
            total_flow = 0
            for warehouse in range(2, 6):  # Склади 1-4
                # Потік: Термінал -> Склад -> Магазин
                flow_t_to_w = flow_matrix[terminal][warehouse]
                flow_w_to_s = flow_matrix[warehouse][store]

                if flow_t_to_w > 0 and flow_w_to_s > 0:
                    # Пропорційний розподіл потоку
                    total_warehouse_out = sum(flow_matrix[warehouse][s] for s in range(6, 20))
                    if total_warehouse_out > 0:
                        contribution = (flow_w_to_s / total_warehouse_out) * flow_t_to_w
                        total_flow += contribution

            if total_flow > 0.5:  # Округлюємо малі значення
                print(f"{terminal_name:<15} {store_name:<15} {total_flow:<30.2f}")
                terminal_flows[terminal_name] += total_flow
                store_flows[store_name] = store_flows.get(store_name, 0) + total_flow

    # Аналіз результатів
    analysis_of_results(edges, flow_matrix)

    # Візуалізація графа
    visualize_network(edges, flow_matrix)

def analysis_of_results(edges, flow_matrix):
    """
    Друкує відповіді на аналітичні запитання
    """

    print("\n" + "="*80)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("="*80)

    # 1. Які термінали забезпечують найбільший потік?
    print("\n1. Термінали, що забезпечують найбільший потік товарів:")
    for terminal in [0, 1]:
        terminal_name = f"Термінал {terminal + 1}"
        flow_from_terminal = sum(flow_matrix[terminal][w] for w in range(2, 6))
        print(f"   {terminal_name}: {flow_from_terminal} одиниць")

    # 2. Маршрути з найменшою пропускною здатністю
    print("\n2. Маршрути з найменшою пропускною здатністю (вузькі місця):")
    bottlenecks = []
    for u, v, cap in edges:
        if cap != float('inf') and cap < 15:
            bottlenecks.append((u, v, cap, flow_matrix[u][v]))

    bottlenecks.sort(key=lambda x: x[2])

    node_names = {
        0: "Термінал 1", 1: "Термінал 2",
        2: "Склад 1", 3: "Склад 2", 4: "Склад 3", 5: "Склад 4"
    }
    for i in range(6, 20):
        node_names[i] = f"Магазин {i - 5}"

    for u, v, cap, flow in bottlenecks[:5]:
        from_name = node_names.get(u, f"Вузол {u}")
        to_name = node_names.get(v, f"Вузол {v}")

        print(f"   {from_name} -> {to_name}: пропускна здатність = {cap}, потік = {flow}")

    print("\nВплив на загальний потік:")
    print("   - Ці вузькі місця обмежують максимальний потік через мережу")
    print(f"   - {node_names.get(bottlenecks[0][1])} отримує найменше товарів через найменшу пропускну здатність ({bottlenecks[0][2]} одиниць)")

    # 3. Магазини з найменшим постачанням
    print("\n3. Магазини з найменшим постачанням:")
    store_deliveries = []
    for store in range(6, 20):
        total_to_store = sum(flow_matrix[w][store] for w in range(2, 6))
        store_deliveries.append((f"Магазин {store-5}", total_to_store))

    store_deliveries.sort(key=lambda x: x[1])
    for store_name, delivery in store_deliveries[:5]:
        print(f"   {store_name}: {delivery} одиниць")

    print("\nРекомендації для збільшення постачання:")
    print(f"   - Збільшити пропускну здатність {node_names.get(bottlenecks[0][0])} -> {node_names.get(bottlenecks[0][1])} з {bottlenecks[0][2]} до 15+ одиниць")
    print("   - Додати альтернативні маршрути до магазинів з низьким постачанням")
    print("   - Оптимізувати розподіл потоків між складами")

    # 4. Вузькі місця та рекомендації
    print("\n4. Вузькі місця та рекомендації для покращення:")
    print(f"   - {node_names.get(bottlenecks[0][0])} -> {node_names.get(bottlenecks[0][1])} має найменшу пропускну здатність ({bottlenecks[0][2]} одиниць)")
    print(f"   - {node_names.get(bottlenecks[1][0])} -> {node_names.get(bottlenecks[1][1])} обмежений до {bottlenecks[1][2]} одиниць")
    print("   - Збільшення пропускної здатності цих маршрутів може покращити загальний потік")

    print("\n" + "="*80)


def visualize_network(edges, flow_matrix):
    """Візуалізація мережі логістики"""

    # Original matplotlib visualization code
    G = nx.DiGraph()

    # Додаємо ребра з пропускною здатністю та потоком
    for u, v, cap in edges:
        flow = flow_matrix[u][v]
        if flow > 0:
            G.add_edge(u, v, capacity=cap, flow=flow)

    # Створюємо позиції для візуалізації
    pos = {}

    # Термінали
    pos[0] = (0, 3)
    pos[1] = (0, 1)

    # Склади
    pos[2] = (2, 4)
    pos[3] = (2, 3)
    pos[4] = (2, 2)
    pos[5] = (2, 1)

    # Магазини (розташовані у два стовпці)
    for i in range(6, 13):
        pos[i] = (4, 4.5 - (i - 6) * 0.7)
    for i in range(13, 20):
        pos[i] = (5, 4.5 - (i - 13) * 0.7)

    plt.figure(figsize=(16, 10))

    # Малюємо вузли різними кольорами
    node_colors = []
    for node in G.nodes():
        if node in [0, 1]:
            node_colors.append('lightgreen')  # Термінали
        elif node in [2, 3, 4, 5]:
            node_colors.append('lightblue')  # Склади
        else:
            node_colors.append('lightcoral')  # Магазини

    nx.draw(G, pos, with_labels=True, node_size=800, node_color=node_colors,
            font_size=8, font_weight="bold", arrows=True, arrowsize=10)

    # Додаємо мітки з пропускною здатністю та потоком
    edge_labels = {}
    for u, v in G.edges():
        cap = G[u][v]['capacity']
        flow = G[u][v]['flow']
        edge_labels[(u, v)] = f"{flow:.0f}/{cap:.0f}"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    plt.title("Логістична мережа: Термінали -> Склади -> Магазини\n(Потік/Пропускна здатність)",
              fontsize=14, fontweight='bold')

    plt.savefig('logistics_network.png', dpi=150, bbox_inches='tight')
    print("\n Граф збережено у файл 'logistics_network.png'")
    plt.close()


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][
                neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку (повертає також матрицю потоку)
def edmonds_karp_with_flow(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow,
                            capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node

        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow, flow_matrix

def create_edges():
    edges = [
        # Термінал 1 -> Склади
        (0, 2, 25),  # Термінал 1 -> Склад 1
        (0, 3, 20),  # Термінал 1 -> Склад 2
        (0, 4, 15),  # Термінал 1 -> Склад 3

        # Термінал 2 -> Склади
        (1, 4, 15),  # Термінал 2 -> Склад 3
        (1, 5, 30),  # Термінал 2 -> Склад 4
        (1, 3, 10),  # Термінал 2 -> Склад 2

        # Склад 1 -> Магазини
        (2, 6, 15),  # Склад 1 -> Магазин 1
        (2, 7, 10),  # Склад 1 -> Магазин 2
        (2, 8, 20),  # Склад 1 -> Магазин 3

        # Склад 2 -> Магазини
        (3, 9, 15),  # Склад 2 -> Магазин 4
        (3, 10, 10),  # Склад 2 -> Магазин 5
        (3, 11, 25),  # Склад 2 -> Магазин 6

        # Склад 3 -> Магазини
        (4, 12, 20),  # Склад 3 -> Магазин 7
        (4, 13, 15),  # Склад 3 -> Магазин 8
        (4, 14, 10),  # Склад 3 -> Магазин 9

        # Склад 4 -> Магазини
        (5, 15, 20),  # Склад 4 -> Магазин 10
        (5, 16, 10),  # Склад 4 -> Магазин 11
        (5, 17, 15),  # Склад 4 -> Магазин 12
        (5, 18, 5),  # Склад 4 -> Магазин 13
        (5, 19, 10),  # Склад 4 -> Магазин 14
    ]

    return edges


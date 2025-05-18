import networkx as nx
import matplotlib.pyplot as plt

NUM_COUPLES = 3
INITIAL_STATE = (((NUM_COUPLES, NUM_COUPLES), (0, 0)), 0)  # (left, right), boat_position
GOAL_STATE = (((0, 0), (NUM_COUPLES, NUM_COUPLES)), 1)

def is_valid_state(banks):
    """Validasi apakah kondisi aman untuk setiap tepian sungai"""
    (h_left, w_left), (h_right, w_right) = banks

    # Cek keamanan di tepian kiri dan kanan
    left_safe = h_left == 0 or w_left <= h_left
    right_safe = h_right == 0 or w_right <= h_right

    return left_safe and right_safe

def generate_moves():
    """Generate semua kombinasi penumpang yang valid untuk perahu"""
    return [(h, w) for h in range(3) for w in range(3) if 1 <= h + w <= 2]

def calculate_new_banks(banks, boat_pos, h_move, w_move):
    """Hitung distribusi baru penumpang setelah penyeberangan"""
    (h_left, w_left), (h_right, w_right) = banks

    if boat_pos == 0:  # Perahu di tepi kiri
        new_left = (h_left - h_move, w_left - w_move)
        new_right = (h_right + h_move, w_right + w_move)
    else:  # Perahu di tepi kanan
        new_left = (h_left + h_move, w_left + w_move)
        new_right = (h_right - h_move, w_right - w_move)

    return (new_left, new_right)

def get_next_states(current_state):
    """Generate semua kemungkinan state berikutnya yang valid"""
    banks, boat_pos = current_state
    next_states = []

    for h_move, w_move in generate_moves():
        # Cek kapasitas penumpang di bank asal
        if boat_pos == 0 and (banks[0][0] < h_move or banks[0][1] < w_move):
            continue
        if boat_pos == 1 and (banks[1][0] < h_move or banks[1][1] < w_move):
            continue

        new_banks = calculate_new_banks(banks, boat_pos, h_move, w_move)

        # Validasi kondisi keamanan
        if is_valid_state(new_banks):
            new_boat_pos = 1 - boat_pos  # Toggle boat position
            next_states.append((new_banks, new_boat_pos))

    return list(set(next_states))  # Hapus duplikat

def build_state_graph():
    """Bangun graf penyeberangan menggunakan BFS"""
    G = nx.DiGraph()
    queue = [(INITIAL_STATE, [])]
    visited = set()
    visited.add(INITIAL_STATE)

    while queue:
        current_state, path = queue.pop(0)
        current_node = f"State: {current_state}"
        G.add_node(current_node)

        if current_state == GOAL_STATE:
            print("Solusi ditemukan! Langkah-langkah:")
            for step in path + [current_state]:
                print(f"• {step}")
            break

        for next_state in get_next_states(current_state):
            next_node = f"State: {next_state}"
            G.add_edge(current_node, next_node)

            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [current_state]))

    return G

def visualize_graph(graph):
    """Visualisasikan graf menggunakan NetworkX dan Matplotlib"""
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(15, 10))
    nx.draw(graph, pos, with_labels=True, node_size=2500, 
            node_color='lightgreen', font_size=8, 
            edge_color='gray', arrows=True)
    plt.title("Graf Penyeberangan Sungai - 3 Pasangan Suami Istri")
    plt.show()

if __name__ == "__main__":
    state_graph = build_state_graph()
    visualize_graph(state_graph)

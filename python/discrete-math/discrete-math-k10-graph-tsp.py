NUM_COUPLES = 3  # <-- SOLUSI UTAMA

import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

def is_valid_state(banks):
    (h_left, w_left), (h_right, w_right) = banks
    return (h_left >= w_left or h_left == 0) and (h_right >= w_right or h_right == 0)

def get_next_states(current_state):
    (banks, boat_pos) = current_state
    (h_left, w_left), (h_right, w_right) = banks
    next_states = []
    
    # Generate semua kemungkinan pergerakan
    for h_move in range(3):
        for w_move in range(3):
            if 1 <= h_move + w_move <= 2:
                if boat_pos == 0:  # Perahu di kiri
                    if h_left >= h_move and w_left >= w_move:
                        new_left = (h_left - h_move, w_left - w_move)
                        new_right = (h_right + h_move, w_right + w_move)
                        if is_valid_state((new_left, new_right)):
                            next_states.append(((new_left, new_right), 1))
                else:  # Perahu di kanan
                    if h_right >= h_move and w_right >= w_move:
                        new_left = (h_left + h_move, w_left + w_move)
                        new_right = (h_right - h_move, w_right - w_move)
                        if is_valid_state((new_left, new_right)):
                            next_states.append(((new_left, new_right), 0))
    return next_states

def generate_all_states():
    states = []
    for h_left in range(NUM_COUPLES + 1):
        for w_left in range(NUM_COUPLES + 1):
            banks = (
                (h_left, w_left), 
                (NUM_COUPLES - h_left, NUM_COUPLES - w_left)
            )
            if is_valid_state(banks):
                states.append((banks, 0))
                states.append((banks, 1))
    return states

def create_distance_matrix(states):
    n = len(states)
    distance_matrix = np.full((n, n), np.inf)
    
    for i, state_i in enumerate(states):
        for j, state_j in enumerate(states):
            if i != j and state_j in get_next_states(state_i):
                distance_matrix[i][j] = 1
                
    return distance_matrix

if __name__ == "__main__":
    all_states = generate_all_states()
    print(f"Total state valid: {len(all_states)}")
    
    start_state = (((3, 3), (0, 0)), 0)
    end_state = (((0, 0), (3, 3)), 1)
    
    try:
        start_idx = all_states.index(start_state)
        end_idx = all_states.index(end_state)
    except ValueError as e:
        print(f"Error: {e} - Pastikan format state sesuai!")
        exit()

    distance_matrix = create_distance_matrix(all_states)
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    
    print(f"Jalur terpendek: {distance} langkah")

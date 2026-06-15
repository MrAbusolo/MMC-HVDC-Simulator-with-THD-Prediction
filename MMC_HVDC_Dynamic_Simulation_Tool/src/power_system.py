def calculate_line_voltages(v_a, v_b, v_c):
    v_ab = v_a - v_b
    v_bc = v_b - v_c
    v_ca = v_c - v_a

    return v_ab, v_bc, v_ca
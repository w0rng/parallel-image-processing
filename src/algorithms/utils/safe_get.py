def safe_get_from_matrix(matrix, y, x):
    if not (0 <= y < len(matrix) and 0 <= x < len(matrix[0])):
        return None
    return matrix[y][x]
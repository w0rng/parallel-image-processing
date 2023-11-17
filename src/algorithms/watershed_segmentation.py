def is_valid_pixel(image, visited, row, col, level):
    rows = len(image)
    cols = len(image[0])
    return (row >= 0 and row < rows and col >= 0 and col < cols and not visited[row][col] and image[row][col][
        0] > level)


def water_division(image, water_level):
    rows = len(image)
    cols = len(image[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    category = 1

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                if image[i][j][0] <= water_level:
                    visited[i][j] = True
                    image[i][j] = 0
                else:
                    stack = [(i, j)]
                    visited[i][j] = True
                    image[i][j] = category

                    while stack:
                        row, col = stack.pop()

                        for dr, dc in directions:
                            new_row, new_col = row + dr, col + dc
                            if is_valid_pixel(image, visited, new_row, new_col, water_level):
                                stack.append((new_row, new_col))
                                visited[new_row][new_col] = True
                                image[new_row][new_col] = category

                    category += 1

    return image

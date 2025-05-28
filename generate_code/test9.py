def minPath(grid, k):
    """
    Given a grid with N rows and N columns (N >= 2) and a positive integer k,
    each cell of the grid contains a value. Every integer in the range [1, N * N]
    inclusive appears exactly once on the cells of the grid.

    You have to find the minimum path of length k in the grid. You can start
    from any cell, and in each step you can move to any of the neighbor cells,
    in other words, you can go to cells which share an edge with your current
    cell.
    Please note that a path of length k means visiting exactly k cells (not
    necessarily distinct).
    You CANNOT go off the grid.
    A path A (of length k) is considered less than a path B (of length k) if
    after making the ordered lists of the values on the cells that A and B go
    through (let's call them lst_A and lst_B), lst_A is lexicographically less
    than lst_B, in other words, there exist an integer index i (1 <= i <= k)
    such that lst_A[i] < lst_B[i] and for any j (1 <= j < i) we have
    lst_A[j] = lst_B[j].
    It is guaranteed that the answer is unique.
    Return an ordered list of the values on the cells that the minimum path go through.

    Examples:

    Input: grid = [ [1,2,3], [4,5,6], [7,8,9]], k = 3
    Output: [1, 2, 1]

    Input: grid = [ [5,9,3], [4,1,6], [7,8,2]], k = 1
    Output: [1]
    """
    if not grid or k <= 0:
        return []

    n_rows, n_cols = len(grid), len(grid[0])
    # Find the global minimum value and its positions (could be multiple)
    min_val = min(min(row) for row in grid)
    frontier = {(r, c) for r in range(n_rows) for c in range(n_cols) if grid[r][c] == min_val}

    path = [min_val]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for _ in range(k - 1):
        best_next_val = float("inf")
        next_frontier = set()

        for r, c in frontier:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n_rows and 0 <= nc < n_cols:
                    val = grid[nr][nc]
                    if val < best_next_val:
                        best_next_val = val
                        next_frontier = {(nr, nc)}
                    elif val == best_next_val:
                        next_frontier.add((nr, nc))

        path.append(best_next_val)
        frontier = next_frontier

    return path

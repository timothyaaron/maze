import random

import pygame


def build_maze(grid, path, SHOW_MAZE):

    def _valid_direction(cell):
        return cell not in visited_cells and cell in grid

    stack_list = []
    visited_cells = []

    idx = 0, 0
    stack_list.append(idx)
    visited_cells.append(idx)

    if SHOW_MAZE:
        grid[idx].show_walls()
        pygame.display.update()

    while stack_list:
        valid_directions = [d for d in grid[idx].directions if _valid_direction(d)]

        if valid_directions:
            new_idx = random.choice(valid_directions)

            path[new_idx] = idx  # do I need this?
            visited_cells.append(new_idx)
            stack_list.append(new_idx)

            # link from idx to new_idx
            absolute_direction = grid[idx].directions[new_idx]
            grid[idx].links[absolute_direction] = new_idx

            # link from new_idx to idx
            absolute_direction = grid[new_idx].directions[idx]
            grid[new_idx].links[absolute_direction] = idx

            idx = new_idx

            if SHOW_MAZE:
                pygame.time.Clock().tick(120)
                grid[idx].show_walls()
                pygame.display.update()

        else:
            idx = stack_list.pop()

    # add a random extra connection off the path
    # at each 1/5
    # … not sure this helps
    for x in range(5):
        start = int(x/5 * len(path))
        end = int((x+1)/5 * len(path))
        idx = random.choice(list(path)[start:end])
        links = grid[idx].links.values()
        valid_directions = [
            d for d in grid[idx].directions
            if d in grid and d not in links and len(links) == 2
        ]
        print(start, end, idx, valid_directions)
        if valid_directions:
            new_idx = random.choice(valid_directions)
            new_dir = grid[idx].directions[new_idx]
            grid[idx].links[new_dir] = new_idx

            p_dir = grid[new_idx].directions[idx]
            grid[new_idx].links[p_dir] = idx

            if SHOW_MAZE:
                pygame.time.Clock().tick(30)
                grid[idx].show_walls()
                # grid[new_idx].show_walls()
                pygame.display.update()

import rubik

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    
    if start == end:
        return []
    
    start_level = set(start)
    end_level = set(end)
    parent_from_start = { (start, None): None }
    frontier_from_start = [(start, None)]
    parent_from_end = { (end, None): None }
    frontier_from_end = [(end, None)]
    
    for i in range(0, 7):
        next = []
        for position in frontier_from_start:
            for neighbor in neighbors(position[0]):
                if neighbor[0] not in start_level:
                    start_level.add(neighbor[0])
                    parent_from_start[neighbor] = position
                    next.append(neighbor)
                    if neighbor[0] == end:
                        return construct_path(neighbor, parent_from_start)    
        frontier_from_start = next
        next = []
        for position in frontier_from_end:
            for neighbor in neighbors(position[0]):
                if neighbor[0] not in end_level:
                    end_level.add(neighbor[0])
                    parent_from_end[neighbor] = position
                    next.append(neighbor)
        frontier_from_end = next
        intersection = set([el[0] for el in frontier_from_start]).intersection([el[0] for el in frontier_from_end])
        if intersection:
            conf = intersection.pop()
            start_end = _find_conf(conf, frontier_from_start)
            end_end = _find_conf(conf, frontier_from_end)
            return construct_path_two_ends(start_end, parent_from_start, end_end, parent_from_end)
        
                
def _find_conf(conf, frontier):
    for el in frontier:
        if el[0] == conf:
            return el                    

def neighbors(position):
    neighbors = []
    for twist in rubik.quarter_twists:
        neighbors.append((rubik.perm_apply(twist, position), twist))
    return neighbors     


def construct_path(end, parent):
    position = end
    result = []
    while parent[position] is not None:
        result.append(position[1])
        position = parent[position]
    result.reverse()
    return result

def construct_path_two_ends(start_end, parent_from_start, end_end, parent_from_end):
    position = start_end
    result = []
    while parent_from_start[position] is not None:
        result.append(position[1])
        position = parent_from_start[position]
    result.reverse()
    
    position = end_end
    while parent_from_end[position] is not None:
        result.append(rubik.perm_inverse(position[1]))
        position = parent_from_end[position]
    
    return result
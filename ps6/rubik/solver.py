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
    
    level = set(start)
    parent = { (start, None): None }
    frontier = [(start, None)]
    while frontier:
        next = []
        for position in frontier:
            for neighbor in neighbors(position[0]):
                if neighbor[0] not in level:
                    level.add(neighbor[0])
                    parent[neighbor] = position
                    next.append(neighbor)
                if neighbor[0] == end:
                    return construct_path(neighbor, parent)             
        frontier = next
                
                        

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
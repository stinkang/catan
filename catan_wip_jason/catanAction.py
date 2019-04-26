import numpy as np

# Note: Catan Board vertices (locations for buildings) are indexed 0 - 24, from going from left to right, bottom upwards

def action(self):
    
    
def planBoard(baseBoard):
    """Draft idea: Place initial settlement near where adjacent dice tiles are close to 7 as possible, 
    except when deserts are present
    
    Possible expansions: building initally near a trading port, build towards a trading port"""
    potential_vertices = [(1,1), (2,1), (3,1), 
                          (1,2), (2,2), (3,2),
                          (1,3), (2,3), (3,3)] # Want center of the board to maximize resources of adjacent tiles
    expected_vals_vertex = []
    for vertex in potential_vertices:
        x, y = vertex
        if 7 in tile_dice_vals:
            expected_vals_vertex = 999 # Don't build adjacent deserts!
            continue
        avg_vertex_vals = mean(adj_vertex_dice_vals(x, y, baseBoard)) 
        expected_vals_vertex.append(avg_vertex_vals)
    distance_from_expected_val = [abs(7 - exp) for exp in expected_vals_vertex] # Calculate vertex with adjacent values nearest 7
    min_dist = min(distance_from_expected_val)
    optSettlementLoc = potential_vertices[distance_from_expected_val.index(min_dist)] # Select vertex with adjacent values nearest 7
    while !baseBoard.if_can_build(settlement, optSettlementLoc[0], optSettlementLoc[1]) # Error handling when optimal location taken
        potential_vertices.remove(optSettlementLoc)
        distance_from_expected_val.remove(minDist)
        min_dist = min(distance_from_expected_val)
        optSettlementLoc = potential_vertices[distance_from_expected_val.index(min_dist)]
    return optSettlementLoc
    
def dumpPolicy(self, max_resources):
    """Draft idea: Dump resources keeping ratios needed to build 2 roads and 1 settlement
    Possible expansion: Consider the layout of the board for when to dump resources: for both adjacent resource tiles and existing 
    buildings"""
    dumped_resources = [0, 0, 0]
    ideal_ratios = [1, 3/4, 1/4]
    dumpCount = sum(self.resources) - max_resources
    while dumpCount > 0:
        current_ratios = normalized_resource_ratios(self.resources)
        if current_ratios[2] > ideal_ratios[2]:
            dumped_resources[2] += 1
            continue
        if current_ratios[1] > ideal_ratios[1]:
            dumped_resources[1] += 1
            continue
        if current_ratios[0] > ideal_ratios[0]:
            dumped_resources[0] += 1
            continue
        if self.resources[2] - dumped_resources > 0: # If no extra resources, just dump in order of 1grain 2brick 3wood
            dumped_resources[2] += 1 
            continue
        if self.resources[1] - dumped_resources > 0:
            dumped_resources[1] += 1 
            continue
        if self.resources[0] - dumped_resources > 0:
            dumped_resources[0] += 1 
            continue
    return dumped_resources
            
### HELPER FUNCTIONS ###    
 
def adj_vertex_dice_vals(x, y, board):
    """Returns the dice values of adjacent tiles to a given vertex (building location)
    x = vertex x coord
    y = vertex y coord
    board = Catan board"""
    tile_dice_vals = []
    for dx in [-1, 0]:
        for dy in [-1, 0]:
            xx = x + dx
            yy = y + dy
            if board.is_tile(xx, yy):
                tile_dice_vals.append(board.dice[yy, xx])
    return tile_dice_vals

def normalized_resource_ratios(resources):
    """Returns the ratio of existing resources normalized by wood = 1"""
    return [resources[0], resources[1] / resources[0], resources[2] / resources[0]]

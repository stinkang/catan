import numpy as np

# Note: Catan Board vertices (locations for buildings) are indexed 0 - 24, from going from left to right, bottom upwards
vertex_locations = [(0,0), (1,0), (2,0), (3,0), (4,0),
                    (0,1), (1,1), (2,1), (3,1), (4,1),
                    (0,2), (1,2), (2,2), (3,2), (4,2),
                    (0,3), (1,3), (2,3), (3,3), (4,3),
                    (0,4), (1,4), (2,4), (3,4), (4,4),]
# Probability of sum of 2 dice rolls being value of index + 2
prob_land = [0.0278, 0.0556, 0.0833, 0.1111, 0.1389, 0.1667, 0.1389, 0.1111, 0.0833, 0.0556, 0.0278]

def action(self):
    """Draft idea:
    1. Strategy dependent on initial settlement location

        -Always build when resources permit
        -Always trade when conditions for trading have been met (ratio balancing)

        Early Game
        -Trade: build roads to trading ports (top left grain or top right general) before expanding, building settlements along the way
            -Choose port based on shortest Manhattan distance, build roads to the port
            -Make trades to maximize # of roads built
            -Once port has been reached, is unreachable, or road count >= 3, shift strategy to build a settlement (maximizing # of settlements, then highest probability of resource drops)
            -Change to network strategy
        -Network: focus on building roads to vertices locations with highest probability of resource drops
            -Choose vertex with Manhattan distance of 2 subject to above (or 1, if road has been built) and collect resources to build a settlement there
            -Trade excess away grain for missing brick/wood, if any
        -If unable to build additional settlements, or if 3 settlements exist, change strategy to "city"

        Late Game
        -City: upgrade all existing settlements to cities
            -Update trading strategy: get rid of wood for brick / grain
            -When upgrading, prioritize locations with brick / grain and strive for 1:2:2 ratio of adjacent blocks
            -If X # of actions have passed without a city being built, switch to development card strategy
        -Card: focus on harvesting development cards
            -Solely trade to maintain 1:2:2 ratio of resources
            -When big X # of actions have passed without a settlement/city build possible, use this strategy
    2.  
    """
    if self.strategy == "trade":
        #TODO
    if self.strategy == "network":
        #TODO
    if self.strategy == "city":
        #TODO
    if self.strategy == "card":
        #TODO
    self.turn_count += 1
    
def planBoard(baseBoard):
    """Draft idea: Place initial settlement near where adjacent dice tiles are close to 7 as possible, 
    except when deserts are present
    
    Possible expansions: building initally near a trading port, build towards a trading port"""
    self.desired_ratios = [1, 3/4, 1/4] # State variable, tracks the desired ratio for making trades
    potential_vertices = [(1,1), (2,1), (3,1), 
                      (1,2), (2,2), (3,2),
                      (1,3), (2,3), (3,3)] # Want center of the board to maximize resources of adjacent tiles
    sorted_potential_vertices = sort_vertices_for_building_exp(potential_vertices, board, no_desert=True)
    adj_resources = adj_vertex_resources(sorted_potential_vertices[0], board)
    optSettlementLoc = sorted_potential_vertices[0]
    count = 0
    while adj_resources[0] == 0 or adj_resources[1] == 0: # Avoid cases where wood or brick is not initally present
        if count >= 2:
            count += 1
            optSettlementLoc = sorted_potential_vertices[0] # Assume bad board, go for trading strategy
            self.strategy = "trade"
            break
        optSettlementLoc = sorted_potential_vertices[count+1]
        adj_resources = adj_vertex_resources(dummy_vertices[0], board)
        count += 1    
    if !baseBoard.if_can_build(settlement, optSettlementLoc[0], optSettlementLoc[1]) # Error handling when optimal location taken
        if count < 3:
            optSettlementLoc = sorted_potential_vertices[count+1]
            self.strategy = "network"
        optSettlementLoc = sorted_potential_vertices[1]
    self.adj_resource_total = adj_resources # State variable, tracks adjacent resource fields
    self.turn_count = 0 # State variable, tracks number of turns taken
    return optSettlementLoc
    
def dumpPolicy(self, max_resources):
    """Draft idea: Dump resources keeping ratios needed to build 2 roads and 1 settlement
    Possible expansion: Consider the layout of the board for when to dump resources: for both adjacent resource tiles and existing 
    buildings"""
    dumped_resources = [0, 0, 0]
    dumpCount = sum(self.resources) - max_resources
    while dumpCount > 0:
        current_ratios = normalized_resource_ratios(self.resources)
        if current_ratios[2] > self.desired_ratios[2]:
            dumped_resources[2] += 1
            continue
        if current_ratios[0] > self.desired_ratios[0]:
            dumped_resources[0] += 1
            continue
        if current_ratios[1] > self.desired_ratios[1]:
            dumped_resources[1] += 1
            continue
        if self.resources[2] - dumped_resources > 0: # If no extra resources, just dump in order of grain - wood - brick
            dumped_resources[2] += 1 
            continue
        if self.resources[0] - dumped_resources > 0:
            dumped_resources[0] += 1 
            continue
        if self.resources[1] - dumped_resources > 0:
            dumped_resources[1] += 1 
            continue
    return dumped_resources
            
### HELPER FUNCTIONS ###    
 
def adj_vertex_dice_vals(vertex, board):
    """Returns the dice values of adjacent tiles to a given vertex (building location)"""
    x, y = vertex
    dice_vals = []
    for dx in [-1, 0]:
        for dy in [-1, 0]:
            xx = x + dx
            yy = y + dy
            if board.is_tile(xx, yy):
                dice_vals.append(board.dice[yy, xx])
    return dice_vals

def adj_vertex_resources_vals(vertex, board)
    """Returns the resource values of adjacent tiles to given vertex (building location)"""
    x, y = vertex
    resources = []
    for dx in [-1, 0]:
        for dy in [-1, 0]:
            xx = x + dx
            yy = y + dy
            if board.is_tile(xx, yy):
                die = self.dice[yy, xx]
                if die != 7:
                    r = self.resources[yy, xx]
                    resources[r] += 1
    return resources
    # self.resources_per_turn  - define in other functions

def sort_vertices_for_building_exp(vertices, board, no_desert=False):
    """Given a list of vertices for settlement building, return a sorted version
    high to low by the likelihood of a turn resulting in resource collection
    
    Prioritize no deserts when no_desert is true"""
    prob_land = [0.0278, 0.0556, 0.0833, 0.1111, 0.1389, 0.1667, 0.1389, 0.1111, 0.0833, 0.0556, 0.0278]
    if no_desert:
        prob_land[5] = -999
    prob_adj_vertex = []
    for vertex in vertices:
        vertex_dice_vals = adj_vertex_dice_vals(vertex, board)
        prob_adj = 0
        for dice_val in vertex_dice_vals:
            prob_adj += prob_land[dice_val - 2]
        prob_adj_vertex.append(prob_adj)
    sorted_vertices = [vertex for _,vertex in sorted(zip(prob_adj_vertex,vertices))] # Sort original vertices by highest probabilities
    sorted_vertices.reverse()
    return sorted_vertices

def adj_vertex_resources(vertex, board):
    x, y = vertex
    adj_resources = [0, 0, 0]
    for dx in [-1, 0]:
        for dy in [-1, 0]:
            xx = x + dx
            yy = y + dy
            if board.is_tile(xx, yy):
                die = board.dice[yy, xx]
                if die != 7:
                    adj_resources[board.resources[yy, xx]] += 1
    return adj_resources

def normalized_resource_ratios(resources):
    """Returns the ratio of existing resources normalized by wood = 1"""
    return [resources[0], resources[1] / resources[0], resources[2] / resources[0]]




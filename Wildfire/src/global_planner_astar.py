"""
This code contains two global planners based on discreet motion planning and sampling based motion planning. 
These will give a global path plan to the local planner. 
"""

from environment import *
from utils import *
from firetruck import *

class NODE:
    def __init__(self,pos,grid_pos,parent = 'root',width=10,win_width=500,angle = 0) -> None:
        self.pos = pos
        self.angle = angle
        self.grid_pos = grid_pos
        self.state = (grid_pos[0],grid_pos[1],angle)
        
        self.grid_x,self.grid_y = grid_pos
        self.type = "drivable"
        self.parent = parent
        self.center = (self.pos[0]+ width//2,self.pos[1]+width//2)
        self.center_state = (self.center[0],self.center[1],angle)
        self.rect = pygame.Rect(0,0,width,width)
        self.rect.center = self.center
        self.neighbours = []
        self.width = width
        self.win_width = win_width
        self.near_by_bush = []
    def get_rect(self):
        return self.rect
    
    def get_center(self):
        return self.center

    def find_nearby_bush(self,forest):
        self.near_by_bush = forest.can_extinguish(self.rect,False)
        return self.near_by_bush
        
    def find_neighbours(self,graph,cost):
        if self.grid_x -1 > 0 and self.grid_y -1 > 0 and graph[self.grid_x -1][self.grid_y -1].type == 'drivable':#topLeft
            self.neighbours.append((NODE(graph[self.grid_x -1][self.grid_y -1].pos,graph[self.grid_x -1][self.grid_y -1].grid_pos,parent = self,angle = 135), cost + abs(3-self.angle/45)))
        if self.grid_y -1 > 0 and graph[self.grid_x][self.grid_y -1].type == 'drivable':#topMid
            self.neighbours.append((NODE(graph[self.grid_x][self.grid_y -1].pos,graph[self.grid_x][self.grid_y -1].grid_pos,parent = self,angle = 90), cost+abs(2-self.angle/45)))
        if self.grid_x +1 < 50 and self.grid_y -1 > 0 and graph[self.grid_x +1][self.grid_y -1].type == 'drivable':#topRight
            self.neighbours.append((NODE(graph[self.grid_x +1][self.grid_y -1].pos,graph[self.grid_x +1][self.grid_y -1].grid_pos,parent = self,angle = 45), cost +abs(1-self.angle/45)))
        if self.grid_x -1 > 0 and graph[self.grid_x -1][self.grid_y].type == 'drivable':#midLeft
            self.neighbours.append((NODE(graph[self.grid_x -1][self.grid_y].pos,graph[self.grid_x -1][self.grid_y].grid_pos,parent = self,angle = 180), cost+abs(4-self.angle/45)))
        if self.grid_x +1 < 50 and graph[self.grid_x +1][self.grid_y].type == 'drivable':#midRight
            self.neighbours.append((NODE(graph[self.grid_x +1][self.grid_y].pos,graph[self.grid_x +1][self.grid_y].grid_pos,parent = self,angle = 0),cost+ abs(0-self.angle/45)))
        if self.grid_x -1 > 0 and self.grid_y +1 < 50 and graph[self.grid_x -1][self.grid_y +1].type == 'drivable':#bottomLeft
            self.neighbours.append((NODE(graph[self.grid_x -1][self.grid_y +1].pos,graph[self.grid_x -1][self.grid_y +1].grid_pos,parent = self,angle = 225), cost+abs(5-self.angle/45)))
        if self.grid_y +1 < 50 and graph[self.grid_x][self.grid_y +1].type == 'drivable':#bottomMid
            self.neighbours.append((NODE(graph[self.grid_x][self.grid_y +1].pos,graph[self.grid_x][self.grid_y +1].grid_pos,parent = self,angle =270),cost+ abs(6-self.angle/45)))
        if self.grid_x +1 < 50 and self.grid_y +1 < 50 and graph[self.grid_x +1][self.grid_y +1].type == 'drivable':#bottomRight
            self.neighbours.append((NODE(graph[self.grid_x +1][self.grid_y +1].pos,graph[self.grid_x +1][self.grid_y +1].grid_pos,parent = self,angle = 315),cost+ abs(7-self.angle/45)))
        return self.neighbours  
    def draw(self,win):
        if self.type == "drivable":
            color = WHITE
        else:
            color = BLACK
        
        pygame.draw.rect(win,color,self.rect)


def tree(forest,width = 10):
    #Take the object of class Forest and gives out a list of nodes that make the quadTree.
    
    grid = forest.get_grid()
    forest_width = forest.width
    bush_width = forest.bush_width
    graph = np.empty((forest_width//width,forest_width//width),dtype=NODE)
    
    for xi in range(graph.shape[0]):
        for yi in range(graph.shape[1]):
            
            node = NODE((xi*width,yi*width),(xi,yi))
            if grid[xi][yi] == 1:
                node.type = "bush"
            graph[xi][yi] = node
    return graph

def update_tree(graph,forest):
    #adds the near by bushes to each node cell
    for xi in range(graph.shape[0]):
        for yi in range(graph.shape[1]):
            graph[xi][yi].find_nearby_bush(forest)
            

def draw_graph(graph,win):
    for i in range(graph.shape[0]):
        for j in range(graph.shape[1]):
            graph[i][j].draw(win)
    
def heuristic_cost(state,goal):
    s_x,s_y,s_angle = state
    g_x,g_y,g_angle = goal
    cost = ((s_x-g_x)**2 + (s_y-g_y)**2)**0.5
    return cost

def draw_path(path,bush_width = 10):
    [pygame.draw.circle(win,RED,center=(x*bush_width,y*bush_width),radius=2,width=2) for x,y,_ in path]
    pygame.display.update()
    return

def collision(car_rect,obs):
    collide = False
    for obstacle in obs:
        collide = pygame.Rect.colliderect(obstacle,car_rect)
        if collide == True:
            break   
    return  collide


def find_path(root_node,goal_state,graph,truck,forest,bush_width = 10,):
    queue = []
    queue.append((root_node,0))
    visited = []
    x,y,angle = root_node.state
    visited.append(root_node.state)
    flag = False
    while len(queue)>0:
        queue = sorted(queue,key = lambda x:x[1])
        curr_node,cost = queue.pop(0)
        if curr_node.state[0] == goal_state[0] and curr_node.state[1]==goal_state[1]:
            goal_state = curr_node
            flag = True
            break
        child_nodes = curr_node.find_neighbours(graph,cost)
        for child_node,cost in child_nodes:
            x,y,angle = child_node.state
            if (x,y,angle) not in visited and not forest.is_collision([truck.ref_rect((x*10,y*10,angle))]):
                visited.append(child_node.state)
                cost = cost + heuristic_cost(child_node.state,goal_state)
                queue.append((child_node,cost))
    if flag:
        node = goal_state
    else:
        return []
    path = []
    while node.parent!='root':
        path.append(node.center_state)
        node = node.parent
    return path


if __name__ == "__main__":
    pygame.init()
    width_win = 500
    height_win = 500
    run = True
    win = pygame.display.set_mode((width_win,height_win))
    pygame.display.set_caption("Title")
    win.fill(WHITE)
    
    f = Forest()
    f.create()
    grid = f.get_grid()
    np.save("grid.npy",grid)
    draw_type = "forest"
    graph = tree(f)     
    truck = Firetruck()
    draw_graph(graph,win)
    start_node = graph[0][0]
    goal_state = graph[-1][-1].state
    while run:
        win.fill(WHITE)
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
        random_x = np.random.randint(0,50)
        random_y = np.random.randint(0,50)
        while  not graph[random_x][random_y].type == "drivable":
            random_x = np.random.randint(0,50)
            random_y = np.random.randint(0,50)
        goal_state = graph[random_x][random_y]
        bushes = goal_state.find_nearby_bush(f)
        goal_state = goal_state.state
        bushes[0].set_fire(0)

        
        start_time = time.time()
        path = find_path(start_node,goal_state,graph,truck,f)

        draw_path(path)
        end_time = time.time() - start_time
        print('duration',end_time)
        for state in reversed(path):
            win.fill(WHITE)
            pygame.draw.circle(win,RED,center = (goal_state[0]*10,goal_state[1]*10),radius=4)
            print(state)
            truck.change_state(state)
            truck.draw(win)
            f.draw(win)
            pygame.display.update()
            pygame.time.wait(500)
        bushes[0].extinguish_fire(0)
        start_node = graph[random_x][random_y]
        truck.change_state(start_node.center_state)


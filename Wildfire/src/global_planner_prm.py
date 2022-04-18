from utils import *
from firetruck import *
from scipy.spatial import KDTree
import math
from environment import *
from global_planner_astar import *
#Probabilistic Roadmap Parameters:

MAX_SAMPLES = 10000 # Number of sample points
N_EDGES = 8 # Number of edges from one sampled point -- 8 connectivity
MAX_EDGE_LEN = 1000.0 # max edge length


forest1 = Forest()
obstacles = forest1.bushes
truck = Firetruck()

class D_Node:
    """ Node for Dijjkstra planning"""
    def __init__(self,position,angle,parent,edge=20):
        self.x = position[0]
        self.y = position[1]
        self.angle = angle
        self.state = (self.x,self.y,self.angle)
        self.edge = edge
        self.parent = parent
        self.neighbours = []

    def get_neighbour_list(self,samples):
        for sample in samples:
            dis = math.dist([self.x,self.y],[sample[0],sample[1]])
            if dis <self.edge:
                node = D_Node((sample[0],sample[1]),sample[2],parent=self)
                self.neighbours.append((node,abs(self.angle//45 - sample[2]//45)))
    
    def get_neighbours(self):
        return self.neighbours

    def __str__(self):
        return str(self.x)+','+str(self.y)+","+str(self.angle)+" cost : "+str(self.cost)+" came from :" + str(self.parent_index)

def sample_points(forest):
    """ Sample points """
    max_x = forest.width
    max_y = forest.width
    min_x = 0
    min_y = 0

    samples =[]

    while len(samples) <= MAX_SAMPLES:
        x_choice = np.random.randint(min_x,max_x)
        y_choice = np.random.randint(min_y,max_y)
        theta_choice = np.random.randint(0,8)*45

        # Check if sampled point is valid
        truck.change_state((x_choice,y_choice,theta_choice))
        is_valid = not forest1.is_collision([truck.ref_rect(truck.get_state())])

        if is_valid:
            samples.append((x_choice,y_choice,theta_choice))
        
        # Add start and goal as sampled points
        samples.append((0,0,0))
    
    return samples

def generate_road_map(sampled_pts):
    """ Generate road map """
    road_map = {}
    for sample in sampled_pts:
        node = D_Node((sample[0],sample[1]),sample[2],parent='root')
        node.get_neighbour_list(sampled_pts)
        road_map[sample[0],sample[1]] = node
    return road_map

def search_roadmap(root_node,goal_state,graph,bush_width = 10):
    queue = []
    queue.append((root_node,0))
    visited = []
    x,y,angle = root_node.state
    visited.append(root_node.state)
    while len(queue)>0:
        queue = sorted(queue,key = lambda x:x[1])
        curr_node,cost = queue.pop(0)
        if heuristic_cost(curr_node.state,goal_state)<5:
            goal_state = curr_node
            break
        child_nodes = curr_node.get_neighbours()
        for child_node,cost in child_nodes:
            x,y,angle = child_node.state
            if (x,y,angle) not in visited:
                visited.append(child_node.state)
                cost = cost + heuristic_cost(child_node.state,goal_state)
                queue.append((child_node,cost))
            
    node = goal_state
    path = []
    while node.parent!='root':
        path.append(node.center_state)
        node = node.parent
    return path

def prm_plan(forest):
    """ PRM PLanners """

    sampled_pts = sample_points(forest)
    #print(sampled_pts)
    print(len(sampled_pts))
    road_map = generate_road_map(sampled_pts)
    print(len(road_map))
    path = search_roadmap(road_map[0,0],(50,80,0),road_map)

    return path

if __name__ == "__main__":
    print("Hello")
    pygame.init()
    width_win = 500
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")

    forest1 = Forest(coverage=20)
    obstacles = forest1.bushes
    run = True
    win.fill(WHITE)
    path = prm_plan(forest1)
    for state in path:
        pygame.draw.circle(win,BLUE,center=(state[0],state[1]),radius=2)
    forest1.draw(win)
    pygame.display.update()
    pygame.time.wait(200)
        
    
    
    

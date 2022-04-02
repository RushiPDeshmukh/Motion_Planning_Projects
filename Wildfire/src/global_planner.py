"""
This code contains two global planners based on discreet motion planning and sampling based motion planning. 
These will give a global path plan to the local planner. 
"""

from environment import *
from utils import *

class NODE:
    def __init__(self,pos,grid_pos,parent = 'root',width=10,win_width=500) -> None:
        self.pos = pos
        self.grid_pos = grid_pos
        self.grid_x,self.grid_y = grid_pos
        self.type = "drivable"
        self.parent = parent
        self.center = (self.pos[0]+ width//2,self.pos[1]+width//2)
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
        
    def find_neighbours(self,graph):
        if self.grid_x -1 > 0 and self.grid_y -1 > 0 and graph[self.grid_x -1][self.grid_y -1].type == 'drivable':#topLeft
            self.neighbours.append(graph[self.grid_x -1][self.grid_y -1])
        if self.grid_y -1 > 0 and graph[self.grid_x][self.grid_y -1].type == 'drivable':#topMid
            self.neighbours.append(graph[self.grid_x][self.grid_y -1])
        if self.grid_x +1 < 50 and self.grid_y -1 > 0 and graph[self.grid_x +1][self.grid_y -1].type == 'drivable':#topRight
            self.neighbours.append(graph[self.grid_x +1][self.grid_y -1])
        if self.grid_x -1 > 0 and graph[self.grid_x -1][self.grid_y].type == 'drivable':#midLeft
            self.neighbours.append(graph[self.grid_x -1][self.grid_y])
        if self.grid_x +1 < 50 and graph[self.grid_x +1][self.grid_y].type == 'drivable':#midRight
            self.neighbours.append(graph[self.grid_x +1][self.grid_y])
        if self.grid_x -1 > 0 and self.grid_y +1 < 50 and graph[self.grid_x -1][self.grid_y +1].type == 'drivable':#bottomLeft
            self.neighbours.append(graph[self.grid_x -1][self.grid_y +1])
        if self.grid_y +1 < 50 and graph[self.grid_x][self.grid_y +1].type == 'drivable':#bottomMid
            self.neighbours.append(graph[self.grid_x][self.grid_y +1])
        if self.grid_x +1 < 50 and self.grid_y +1 < 50 and graph[self.grid_x +1][self.grid_y +1].type == 'drivable':#bottomRight
            self.neighbours.append(graph[self.grid_x +1][self.grid_y +1])
        
            

    
    def draw(self,win):
        if self.type == "drivable":
            color = WHITE
        else:
            color = BLACK
        
        pygame.draw.rect(win,color,self.rect)

def tree(forest,width = 10):
    #Take the object of class Forest and gives out a list of nodes that make the quadTree.
    
    grid = forest.get_grid()
    graph = np.empty(grid.shape,dtype=NODE)
    
    for xi in range(grid.shape[0]):
        for yi in range(grid.shape[1]):
            
            node = NODE((xi*width,yi*width),(xi,yi))
            if grid[xi][yi] == 1:
                node.type = "bush"
            graph[xi][yi] = node
    return graph

def draw_graph(graph,win):
    for i in range(graph.shape[0]):
        for j in range(graph.shape[1]):
            graph[i][j].draw(win)
    
    


if __name__ == "__main__":
    width_win = 500
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf',10)
    text = font.render("T",True,BLACK)
    textrect = text.get_rect()
    textrect.topleft = (450,10)
    
    run = True
    pos = (0,0)
    f = Forest()
    f.create()
    t_last = time.time()
    t = 0
    draw_type = "forest"
    graph = tree(f)           
    while t <= 300 and run:
        win.fill(WHITE)
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_g:
                    draw_type = "grid"
                if ev.key == pygame.K_f:
                    draw_type = "forest"
        if t%30 == 0:
            f.trigger_fire(t)
        #Spreading fire is too quick
        if t%20 == 0:
             f.spread_fire(t)
        if draw_type == "forest":
            f.draw(win)
        else:
            draw_graph(graph,win)
        text = font.render("Time: "+str(t),True,BLACK)
        win.blit(text,textrect) 
        pygame.display.update()
        pygame.time.wait(1000)
        t += int(time.time() - t_last)
        t_last = time.time()
        print(t)


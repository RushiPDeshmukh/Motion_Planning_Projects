import numpy as np
import random


def random_patch():
    patch1 = [1,1,1,1]
    patch2 = [[1,0,0],[1,1,1]]
    patch3 = [[0,0,1],[1,1,1]]
    patch4 = [[1,1],[1,1]]
    patch5 = [[0,1,1],[1,1,0]]
    patch6 = [[1,1,0],[0,1,1]]
    patch7 = [[0,1,0],[1,1,1]]
    patchs = {'1':patch1,'2':patch2,'3':patch3,'4':patch4,'5':patch5,'6':patch6,'7':patch7}
    
    random_shape = str(random.randint(1,8))
    random_orientation = random.randint(1,4)
    patch = np.array(patchs[random_shape])

    if len(patch.shape) == 1:
        #Change the orientation of patch
        patch = patch.T if random_orientation%2 == 0 else patch
    else:
        #Change the orientation of patch
        patch = np.rot90(patch,random_orientation,(0,1))

    shape_patch = patch.shape

    return patch,shape_patch

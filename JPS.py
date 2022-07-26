import math

IS_BLOCK = 0

class Node(object):
    def __init__(self, pos):
        assert(len(pos) == 2)
        self.pos = pos
        self.father = None
        self.neighbors = []
        self.gvalue = 0
        self.hvalue = 0
        self.fvalue = 0
    def get_hevristic(self, enode):
        #欧几里得距离
        h = math.hypot(self.pos[0] - enode.pos[0], self.pos[1] - enode.pos[1])
        return h

    def compute_fx(self, enode, father):
        if father == None:
            print('未设置当前节点的父节点！')
        #权重
        gx_father = father.gvalue
        #采用欧式距离计算父节点到当前节点的距离
        gx_f2n = math.hypot(self.pos[0] - father.pos[0], self.pos[1] - father.pos[1])
        # gx_f2n = math.sqrt((father.pos[0] - self.pos[0])**2 + (father.pos[1] - self.pos[1])**2)
        gvalue = gx_f2n + gx_father #加上父节点的g值
        # print("father.pos:",father.pos,"gx_father:",gx_father,"self.pos:",self.pos,"gx_f2n:",gx_f2n,"gvalue:",gvalue)
        #当前节点到终点的距离
        hvalue = self.get_hevristic(enode)
        fvalue = hvalue + gvalue
        # fvalue = hvalue
        return gvalue,hvalue,fvalue

    def set_fx(self, enode, father):
        self.gvalue, self.hvalue, self.fvalue = self.compute_fx(enode, father)
        self.father = father

    def update_fx(self, enode, father):
        gvalue, hvalue, fvalue = self.compute_fx(enode, father)
        if fvalue < self.fvalue:
            self.gvalue, self.hvalue, self.fvalue = gvalue, hvalue, fvalue
            self.father = father

class JPS(object):
    def __init__(self,map, pos_sn, pos_en):
        self.map = map            #地图对象
        self.rows = len(map)
        self.cols = len(map[0])
        self.openlist, self.closelist = [], []
        self.snode = Node(pos_sn) #用于存储路径规划的起始节点
        self.enode = Node(pos_en) #用于存储路径规划的目标节点
        self.cnode = self.snode   #用于存储当前搜索到的节点
        self.addpoints = 0        #添加的跳点数
        self.count = 0            #用于记录搜索次数
        self.is_find_end = False  #是否找到终点

    def search(self):
        self.openlist.append(self.snode)
        self.is_find_end = False  #是否找到终点
        while len(self.openlist) > 0:
            self.openlist.sort(key=lambda x:x.fvalue)
            self.cnode = self.openlist.pop(0)
            self.count += 1
            #判断是否到达终点
            if self.cnode.pos == self.enode.pos:
                self.enode.father = self.cnode.father
                self.is_find_end = True
                break
            # 扩展当前fx最小的节点，并进入下一次循环搜索
            self.find_jump_point_hv(self.cnode)
            self.find_jump_point_diagonal(self.cnode)
            #将节点从openlist移动到closelist
            self.closelist.append(self.cnode)
        print("搜索次数：",self.count)
        print("添加跳点数：",self.addpoints)
        print("代价：",self.cnode.gvalue)
        return self.is_find_end

    #添加openlist
    def add_jump_node(self,cnode,jump_pos,neighbors):
        if jump_pos in list(map(lambda x:x.pos, self.closelist)):
            return None
        open_pos_list = list(map(lambda x:x.pos, self.openlist))
        if jump_pos in open_pos_list:
            jump_node = self.openlist[open_pos_list.index(jump_pos)]
            jump_node.update_fx(self.enode, cnode)
            jump_node.neighbors = neighbors
        else:
            jump_node = Node(jump_pos)
            jump_node.set_fx(self.enode,cnode)
            jump_node.neighbors = neighbors
            self.openlist.append(jump_node)
            self.addpoints += 1
        return jump_node

    def append_jump_nodes_to_openlist(self,cnode,jump_pos_list,neighbors):
        for i in range(0,len(jump_pos_list)):
            self.add_jump_node(cnode,jump_pos_list[i],neighbors[i])

    #父方向
    def get_father_direction(self,cnode):
        #斜方向
        x,y = 0,0
        if cnode.father.pos[0] !=  cnode.pos[0] and cnode.father.pos[1] != cnode.pos[1]:
            if cnode.pos[0] > cnode.father.pos[0]:
                x = 1
            else:
                x = -1
            if cnode.pos[1] > cnode.father.pos[1]:
                y = 1
            else:
                y = -1
        elif cnode.father.pos[0] !=  cnode.pos[0]:#水平
            if cnode.pos[0] > cnode.father.pos[0]:
                x = 1
            else:
                x = -1
        elif cnode.father.pos[1] !=  cnode.pos[1]:#垂直
            if cnode.pos[1] > cnode.father.pos[1]:
                y = 1
            else:
                y = -1
        return (x,y)

    def find_jump_point_hv(self,cnode):
        dirList = []
        if cnode.father is None:
            #上下左右
            dirList = [(0, 1),(0, -1),(-1, 0),(1, 0)]
        else:
            dir = self.get_father_direction(cnode)
            if dir[0] != 0:
                dirList.append((dir[0],0))
            if dir[1] != 1:
                dirList.append((0,dir[1]))
        
        for dir in dirList:
            if self.is_find_end:
                break
            if dir[0] != 0 and dir[1] == 0:
                ret_x,jump_nodes_x,neighbors_x = self.search_x(cnode.pos,dir)
                if ret_x:
                    self.append_jump_nodes_to_openlist(cnode,jump_nodes_x,neighbors_x)
            if dir[1] != 0 and dir[0] == 0:
                ret_y,jump_nodes_y,neighbors_y = self.search_y(cnode.pos,dir)
                if ret_y:
                    self.append_jump_nodes_to_openlist(cnode,jump_nodes_y,neighbors_y)

    def find_jump_point_diagonal(self,cnode):
        dirList = []
        if cnode.father is None:
            dirList = [(1, 1),(1, -1),(-1, 1),(-1, -1)]
        else:
            dir = self.get_father_direction(cnode)
            dirList.append(dir)

            for pos in cnode.neighbors:
                dirList.append((pos[0]-cnode.pos[0],pos[1]-cnode.pos[1]))
        
        for dir in dirList:
            if self.is_find_end:
                break
            if dir[0] != 0 and dir[1] != 0:
                self.search_diagonal(cnode,dir)

    #是否结束点
    def is_end_point(self,pos):
        if pos == self.enode.pos:
            self.is_find_end = True
        return self.is_find_end

    #在x方向上搜索强制邻居
    def get_force_neighbor_x(self,x,y,dir_x):
        neighbor = []
        next_x = x + dir_x
        if next_x < 0 or next_x >= self.cols-1:
            return neighbor
        if self.map[y][next_x] == IS_BLOCK:
            return neighbor
        if y+1 < self.rows and self.map[y+1][x] == IS_BLOCK and self.map[y+1][next_x] != IS_BLOCK:
            neighbor.append((next_x,y+1))
        if y-1 > 0 and self.map[y-1][x] == IS_BLOCK and self.map[y-1][next_x] != IS_BLOCK:
            neighbor.append((next_x,y-1))
        return neighbor

    #在y方向上搜索强制邻居
    def get_force_neighbor_y(self,x,y,dir_y):
        neighbor = []
        next_y = y + dir_y
        if next_y < 0 or next_y >= self.rows-1:
            return neighbor
        if self.map[next_y][x] == IS_BLOCK:
            return neighbor
        if x-1 > 0 and self.map[y][x-1] == IS_BLOCK and self.map[next_y][x-1] != IS_BLOCK:
            neighbor.append((x-1,next_y))
        if x+1 < self.cols and self.map[y][x+1] == IS_BLOCK and self.map[next_y][x+1] != IS_BLOCK:
            neighbor.append((x+1,next_y))
        return neighbor

    #横向探索
    def search_x(self,pos,dir):
        ret = False
        dir_x = dir[0] #x方向
        x = pos[0]
        y = pos[1]
        jump_pos_list = []
        jump_pos_neighbors = []
        while True:
            x += dir_x
            if x < 0 or x > self.cols - 1:#超出边界
                break
            if self.map[y][x] == IS_BLOCK:
                break 
            if self.is_end_point((x,y)):
                jump_pos_list.clear()
                jump_pos_list.append(self.enode.pos)
                jump_pos_neighbors.clear()
                jump_pos_neighbors.append([])
                ret = True
                break
            neighbor = self.get_force_neighbor_x(x,y,dir_x)
            if len(neighbor) > 0:#找到跳点
                jump_pos = (x,y)
                jump_pos_list.append(jump_pos)
                jump_pos_neighbors.append(neighbor)
                ret = True
                if y != self.enode.pos[1]: #如果和结束点在同一排 就继续往前搜索
                    break
        return ret,jump_pos_list,jump_pos_neighbors

    #纵向探索
    def search_y(self,pos,dir):
        ret = False
        dir_y = dir[1] #y方向
        x = pos[0]
        y = pos[1]
        jump_pos_list = []
        jump_pos_neighbors = []
        while True:
            y += dir_y
            if y < 0 or y > self.rows - 1:#超出边界
                break
            if self.map[y][x] == IS_BLOCK:
                break 
            if self.is_end_point((x,y)):
                jump_pos_list.clear()
                jump_pos_list.append(self.enode.pos)
                jump_pos_neighbors.clear()
                jump_pos_neighbors.append([])
                ret = True
                break
            neighbor = self.get_force_neighbor_y(x,y,dir_y)
            if len(neighbor) > 0:#找到跳点
                jump_pos = (x,y)
                jump_pos_list.append(jump_pos)
                jump_pos_neighbors.append(neighbor)
                ret = True
                if x != self.enode.pos[0]: #如果和结束点在同一列 就继续往前搜索
                    break
        return ret,jump_pos_list,jump_pos_neighbors

    def search_diagonal(self,cnode,dir):
        x = cnode.pos[0]
        y = cnode.pos[1]
        dir_x = dir[0]
        dir_y = dir[1]
        while True:
            x += dir_x
            y += dir_y
            if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
                break
            if self.map[y][x] == IS_BLOCK:
                break
            if self.map[y-dir_y][x] == IS_BLOCK and self.map[y][x-dir_x] == IS_BLOCK:
                break 
            if self.is_end_point((x,y)):
                self.add_jump_node(cnode,self.enode.pos,[])
                break
            #先判断自己是否为跳点
            
            #然后纵横搜索
            temp_pos = (x,y)
            ret_x,jump_pos_x,neighbors_x = self.search_x(temp_pos,(dir_x,0))
            ret_y,jump_pos_y,neighbors_y = self.search_y(temp_pos,(0,dir_y))
            if ret_x or ret_y:
                jump_node = self.add_jump_node(cnode,temp_pos,[])
                if jump_node != None:
                    if ret_x:
                        self.append_jump_nodes_to_openlist(jump_node,jump_pos_x,neighbors_x)
                    if ret_y:
                        self.append_jump_nodes_to_openlist(jump_node,jump_pos_y,neighbors_y)

    #获取路径
    def get_minroute(self):
        minroute = []
        current_node = self.enode
        while(True):
            minroute.append(current_node.pos)
            if current_node.father == None:
                print("pos:",current_node.pos,"father:",current_node.father)
                break
            current_node = current_node.father            
        minroute.append(self.snode.pos)
        minroute.reverse()
        return minroute

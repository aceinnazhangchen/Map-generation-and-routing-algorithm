from tkinter import W
import turtle
import math
from load_map import read_csv_to_array
from ramdom_map import init
from ramdom_map import draw_grid

isBlock = 0

def draw_dot(x,y,color):
    turtle.goto(x*10+5,y*10-5)
    turtle.dot(10,color)

def draw_map_dot(array_2d,x,y,color):
    draw_dot(x-len(array_2d)/2,y-len(array_2d[x])/2,color)

class Node(object):
    def __init__(self, pos):
        self.pos = pos
        self.father = None
        self.gvalue = 0
        self.hvalue = 0
        self.fvalue = 0

    def get_cost_easy(self,father):
        if self.pos[0] == father.pos[0] or self.pos[1] == father.pos[1]:
            return 1.0
        else:
            return 1.4

    def get_hevristic(self, enode):
        #曼哈顿距离
        # d = abs(self.pos[0] - enode.pos[0]) + abs(self.pos[1] - enode.pos[1])
        #欧几里得距离
        # d = math.sqrt((self.pos[0] - enode.pos[0])**2 + (self.pos[1] - enode.pos[1])**2)
        d = math.hypot(self.pos[0] - enode.pos[0], self.pos[1] - enode.pos[1])
        #对角线距离（切比雪夫距离）
        # dx = abs(self.pos[0] - enode.pos[0])
        # dy = abs(self.pos[1] - enode.pos[1])
        # min_xy = min(dx,dy)
        # d = dx + dy + (math.sqrt(2) - 2) * min_xy   
        w = 1.0
        # if d > 20:
        #     w = 3.0
        h = w*d
        return h

    def compute_fx(self, enode, father):
        if father == None:
            print('未设置当前节点的父节点！')
        #权重
        gx_father = father.gvalue
        #采用欧式距离计算父节点到当前节点的距离
        #gx_f2n = math.sqrt((father.pos[0] - self.pos[0])**2 + (father.pos[1] - self.pos[1])**2)
        gx_f2n = self.get_cost_easy(father)
        gvalue = gx_f2n + gx_father #加上父节点的g值
        #当前节点到终点的距离
        hvalue = self.get_hevristic(enode)
        fvalue = hvalue + gvalue
        return gvalue,hvalue,fvalue

    def set_fx(self, enode, father):
        self.gvalue, self.hvalue, self.fvalue = self.compute_fx(enode, father)
        self.father = father

    def update_fx(self, enode, father):
        gvalue, hvalue, fvalue = self.compute_fx(enode, father)
        if fvalue < self.fvalue:
            self.gvalue, self.hvalue, self.fvalue = gvalue, hvalue, fvalue
            self.father = father
            print("更新节点：",self.pos)

class Map(object):
    def __init__(self, filename):
        self.filename = filename
        self.map = read_csv_to_array(filename)

    def draw_map(self):
        draw_grid(self.map)

class AStar(object):
    def __init__(self,map, pos_sn, pos_en):
        self.map = map            #地图对象
        self.openlist, self.closelist = [], []
        self.snode = Node(pos_sn) #用于存储路径规划的起始节点
        self.enode = Node(pos_en) #用于存储路径规划的目标节点
        self.cnode = self.snode   #用于存储当前搜索到的节点
        self.count = 0            #用于记录搜索次数
    #计算路径
    def compute_path(self):
        self.openlist.append(self.snode)
        find_path = False
        while len(self.openlist) > 0:
            #获取f值最小的节点
            self.openlist.sort(key=lambda x:x.fvalue)
            self.cnode = self.openlist.pop(0)
            #将节点从openlist移动到closelist
            self.closelist.append(self.cnode)
            draw_map_dot(self.map, self.cnode.pos[0], self.cnode.pos[1], 'white')
            self.count += 1
            #判断是否到达终点
            if self.cnode.pos == self.enode.pos:
                self.enode.father = self.cnode.father
                print(self.cnode.gvalue,self.count)
                find_path = True
                break
            # 扩展当前fx最小的节点，并进入下一次循环搜索
            self.extend(self.cnode)
        return find_path
    #扩展节点
    def extend(self, cnode):
        nodes_neighbors = self.get_neighbors(cnode)
        # print("nodes_neighbors:",len(nodes_neighbors))
        for node in nodes_neighbors:
            #判断节点node是否在closelist，因为closelist中元素为Node类，所以要用map函数转换为坐标集合
            if node.pos in list(map(lambda x:x.pos, self.closelist)):
                continue
            else:
                if node.pos in list(map(lambda x:x.pos, self.openlist)):
                    node.update_fx(self.enode, cnode)
                    # print("update pos:",node.pos)
                else:
                    node.set_fx(self.enode, cnode)
                    self.openlist.append(node)
                    # print("add pos:",node.pos)
    #获取节点的邻居节点
    def get_neighbors(self, cnode):
        offsets = [(-1, 1),(0, 1),(1, 1),
                   (-1, 0),       (1, 0),
                   (-1,-1),(0,-1),(1,-1)]
        nodes_neighbors = []
        x, y = cnode.pos[0], cnode.pos[1]
        for os in offsets:
            x_new, y_new = x + os[0], y + os[1]
            pos_new = (x_new, y_new)
            #判断是否在地图范围内,超出范围跳过
            if x_new < 0 or x_new > len(self.map[0]) - 1 or y_new < 0 or y_new > len(self.map) - 1:
                continue
            #判断是否为障碍物
            if self.map[x_new][y_new] == isBlock:
                continue
            nodes_neighbors.append(Node(pos_new))
        return nodes_neighbors
    #获取路径
    def get_minroute(self):
        minroute = []
        current_node = self.enode
        while(True):
            minroute.append(current_node.pos)
            current_node = current_node.father
            if current_node.pos == self.snode.pos:
                break

        minroute.append(self.snode.pos)
        minroute.reverse()
        return minroute

def draw_route(map,minroute):
    for pos in minroute:
        x, y = pos[0], pos[1]
        draw_map_dot(map, x, y, 'red')

def main():
    init()
    map = Map("map.csv")
    map.draw_map()    
    # turtle.tracer(True)
    Astar = AStar(map.map, (59,59), (0,0))
    if(Astar.compute_path()):
        minroute = Astar.get_minroute()     
        # turtle.tracer(True)   
        draw_route(map.map,minroute)
    turtle.done()

if __name__ == '__main__':
    main()
import turtle
from ramdom_map import init
from ramdom_map import draw_grid

color_list = ["red","orange","olive","blue","purple","brown"]

#读取csv数据到array_2d中
def read_csv_to_array(file_name):
    array_2d = []
    with open(file_name, "r") as f:
        lines =  f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            line = line.strip()
            line = line.split(",")
            array_2d.append([])
            for j in range(0, len(line)):
                array_2d[i].append(int(line[j])) 
    return array_2d

def draw_dot(x,y,color):
    turtle.goto(x*10+5,y*10-5)
    turtle.dot(10,color)

def draw_map_dot(array_2d,x,y,color):
    draw_dot(x-len(array_2d)/2,y-len(array_2d[x])/2,color)

#广度优先遍历
def bfs(array_2d,start_x,start_y,color):
    queue = []
    queue.append((start_x,start_y))
    while len(queue) > 0:
        x,y = queue.pop(0)
        if array_2d[x][y] == 0:
            array_2d[x][y] = 2
            draw_map_dot(array_2d,x,y,color)
            if x > 0:
                queue.append((x-1,y))
            if x < len(array_2d)-1:
                queue.append((x+1,y))
            if y > 0:
                queue.append((x,y-1))
            if y < len(array_2d[0])-1:
                queue.append((x,y+1))

#深度优先遍历
def dfs(array_2d,start_x,start_y):
    stack = []
    stack.append((start_x,start_y))
    while len(stack) > 0:
        x,y = stack.pop()
        if array_2d[x][y] == 0:
            array_2d[x][y] = 2
            draw_map_dot(array_2d,x,y)
            if x > 0:
                stack.append((x-1,y))
            if x < len(array_2d)-1:
                stack.append((x+1,y))
            if y > 0:
                stack.append((x,y-1))
            if y < len(array_2d[0])-1:
                stack.append((x,y+1))

#遍历地图所有空白点，并画出
def bfs_all(array_2d):
    area_index = 0
    for x in range(0, len(array_2d)):
        for y in range(0, len(array_2d[x])):
            if array_2d[x][y] == 0:
                bfs(array_2d,x,y,color_list[area_index])
                print("area:",area_index)
                area_index += 1
                if area_index >= len(color_list):
                    area_index = 0
              
def main():
    init()
    # ramdom_map()
    array_2d = read_csv_to_array("map.csv")
    draw_grid(array_2d)
    bfs_all(array_2d)
    turtle.done()

if __name__ == '__main__':
    main()
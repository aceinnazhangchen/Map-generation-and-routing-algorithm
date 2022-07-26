import random
import time
import turtle

DIG = 0
BUILD = 1

square_size = 10
map_size = 100

def set_pen():
    turtle.pencolor("red")
    turtle.fillcolor("green")
    turtle.hideturtle()
    turtle.pensize(1)

def draw_square(x,y,filled):
    x = x*square_size
    y = y*square_size
    turtle.penup()
    turtle.goto(x, y)
    if filled:
        turtle.begin_fill()
    for i in range(1, 5):
        # turtle.pendown()
        turtle.forward(square_size)
        turtle.right(90)
    turtle.penup()
    if filled:
        turtle.end_fill()
    
#画格子
def draw_grid(array_2d):
    turtle.reset()
    set_pen()
    for i in range(0, len(array_2d)):
        for j in range(0, len(array_2d[i])):
            draw_square(i-len(array_2d)/2,j-len(array_2d[i])/2,array_2d[i][j])
    turtle.update()
    time.sleep(0.1)

#生成二维数组
def create_2d_array(w,h):
    array = []
    for i in range(0, w):
        array.append([])
        for j in range(0, h):
            array[i].append(random.randint(0,1))
    return array

#判断格子周围8个格子值为1的个数
def judge_around_8_grid(array_2d,x,y):
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if array_2d[x+i][y+j] == 1:
                count += 1
    return count

#判断格子周围8个格子值为1的个数
def judge_around_4_grid(array_2d,x,y):
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            if i == 0 or j == 0:
                if array_2d[x+i][y+j] == 1:
                    count += 1
    return count

#平滑格子
def smooth_grid(array_2d,dig_or_build,directions,threshold):
    if dig_or_build == DIG:
         print("dig hole ",directions,threshold)
    elif dig_or_build == BUILD:
         print("build wall ",directions,threshold)   
    count_list = []
    for i in range(1, len(array_2d)-1):
        for j in range(1, len(array_2d[i])-1):
            if directions == 4:
                count = judge_around_4_grid(array_2d,i,j)
            elif directions == 8:
                count = judge_around_8_grid(array_2d,i,j)
            count_list.append(count)
            if dig_or_build == DIG:
                if count <= threshold:
                    array_2d[i][j] = 0
            elif dig_or_build == BUILD:
                if count >= threshold:
                    array_2d[i][j] = 1
        # print(count_list)
        count_list.clear()

#平滑格子(加墙)
def smooth_grid_build_wall(array_2d,directions,threshold):
    smooth_grid(array_2d,BUILD,directions,threshold)

#平滑格子(挖洞)
def smooth_grid_dig_hole(array_2d,directions,threshold):
    smooth_grid(array_2d,DIG,directions,threshold)

#把四周围起来   
def enclosing_wall(array_2d):
    for i in range(0, len(array_2d)):
        array_2d[i][0] = 1
        array_2d[i][len(array_2d[0])-1] = 1
    for j in range(0, len(array_2d[0])):
        array_2d[0][j] = 1
        array_2d[len(array_2d)-1][j] = 1

def init():
    turtle.title("格子")
    turtle.bgcolor('lightgray')
    turtle.setup(800, 600, 0, 0)
    turtle.pencolor("red")
    turtle.fillcolor("green")
    turtle.hideturtle()
    turtle.pensize(1)
    turtle.tracer(False)    # 关闭绘图追踪
    turtle.speed(0)

#把格子数据写入csv中
def write_csv(array_2d):
    with open("map.csv", "w") as f:
        for i in range(0, len(array_2d)):
            for j in range(0, len(array_2d[i])):
                f.write(str(array_2d[i][j]))
                if j != len(array_2d[i])-1:
                    f.write(",")
            f.write("\n")

def ramdom_map():
    init()
    array_2d = create_2d_array(map_size,map_size)
    enclosing_wall(array_2d)
    # draw_grid(array_2d)
    smooth_grid_dig_hole(array_2d,8,3)
    # draw_grid(array_2d)
    smooth_grid_build_wall(array_2d,8,5)
    # draw_grid(array_2d)
    for i in range(2):
        smooth_grid_dig_hole(array_2d,4,1)
        # draw_grid(array_2d)
        smooth_grid_build_wall(array_2d,4,3)
        # draw_grid(array_2d)
    write_csv(array_2d)
    draw_grid(array_2d)

def main():
    ramdom_map()
    turtle.done()

if __name__ == '__main__':
    main()


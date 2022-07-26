import pygame,sys
from load_map import read_csv_to_array
from A_Star import AStar
from JPS import JPS

CELL_SIZE = 5 #单元格尺寸
HALF_CELL = CELL_SIZE/2
IS_BLOCK = 0

#显示文字
def show_text(screen, text, pos, font_color=(255, 0, 0), font_size=16, font_type='微软雅黑'):
    font = pygame.font.SysFont(font_type, font_size)
    text_surface = font.render(text, True, font_color)
    screen.blit(text_surface, pos)

#绘制单元格
def draw_cell(screen, pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x, y, CELL_SIZE-1, CELL_SIZE-1))

#绘制地图单元格
def draw_map(screen, map_data):
    rows = len(map_data)
    cols = len(map_data[0])
    for y in range(rows):
        for x in range(cols):
            if map_data[y][x] == IS_BLOCK:
                draw_cell(screen, (x * CELL_SIZE, y * CELL_SIZE), pygame.Color(128, 128, 128))
            else:
                draw_cell(screen, (x * CELL_SIZE, y * CELL_SIZE), pygame.Color(0, 255, 0))


#以格子为单位画线
def draw_line_by_grid(screen, start_pos, end_pos, color):
    x1, y1 = start_pos
    x2, y2 = end_pos
    pygame.draw.line(screen, color, (x1 * CELL_SIZE + HALF_CELL, y1 * CELL_SIZE+ HALF_CELL), (x2 * CELL_SIZE+ HALF_CELL, y2 * CELL_SIZE+ HALF_CELL))

#在格子中绘制圆点
def draw_circle_in_grid(screen, pos, color):
    x, y = pos
    pygame.draw.circle(screen, color, (x * CELL_SIZE + HALF_CELL, y * CELL_SIZE + HALF_CELL), HALF_CELL)

#绘制网格
def draw_grid_by_line(screen, rows, cols, color):
    for x in range(0, (rows+1) * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, color, (x, 0), (x, CELL_SIZE * cols))
    for y in range(0, (cols+1) * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, color, (0, y), (CELL_SIZE * rows, y))

#调用A*算法
def A_star_find_path(screen, map_data, start_pos, end_pos):
    a_star = AStar(map_data, start_pos, end_pos)
    if(a_star.compute_path()):
        route = a_star.get_minroute()
        for pos in route:
            draw_circle_in_grid(screen, pos, pygame.Color(255, 0, 0))

def JPS_find_path(screen, map_data, start_pos, end_pos):
    jps = JPS(map_data, start_pos, end_pos)
    if jps.search():
        close_list = list(map(lambda x:x.pos, jps.closelist))
        for pos in close_list:
            draw_circle_in_grid(screen, pos, pygame.Color(255, 0, 0))
        open_list = list(map(lambda x:x.pos, jps.openlist))
        for pos in open_list:
            draw_circle_in_grid(screen, pos, pygame.Color(255, 255, 255))
        route = jps.get_minroute()
        for pos in route:
            draw_circle_in_grid(screen, pos, pygame.Color(0, 0, 0))
            if route.index(pos) != 0:
                draw_line_by_grid(screen, route[route.index(pos)-1], pos, pygame.Color(0, 0, 0))

if __name__ == '__main__':
    map_data = read_csv_to_array("map.csv")
    rows = len(map_data)
    cols = len(map_data[0])
    pygame.init()
    screen = pygame.display.set_mode((cols*CELL_SIZE, rows*CELL_SIZE), 0, 32)
    pygame.display.set_caption("Map")
    screen.fill((255, 255, 255))    
    draw_map(screen, map_data)   
    start_pos = (0, 0)
    end_pos = (cols - 51, rows - 51)
    draw_circle_in_grid(screen, start_pos, pygame.Color(0, 0, 255))
    draw_circle_in_grid(screen, end_pos, pygame.Color(255, 0, 0))
    # A_star_find_path(screen, map_data, start_pos, end_pos)
    JPS_find_path(screen, map_data, start_pos, end_pos)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
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
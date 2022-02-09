import numpy as np
import matplotlib.pyplot as plt

def rule(cell1,cell2,cell3):
    if cell1 == 0:
        if cell2 == 0:
            if cell3 == 0:
                return 0
            elif cell3 == 1:
                return 1
        elif cell2 == 1:
            if cell3 == 0:
                return 1
            elif cell3 == 1:
                return 0
    elif cell1 == 1:
        if cell2 == 0:
            if cell3 == 0:
                return 0
            elif cell3 == 1:
                return 1
        elif cell2 == 1:
            if cell3 == 0:
                return 0
            elif cell3 == 1:
                return 1


# セルオートマトンの実行 
num_cell = 17 # セルの数 
steps = 10000 # 何ステップまで計算するか
gosa = 1000
kyoukaiL = 0
kyoukaiR = 1
cell_list = []# 各世代のセルの情報を記録するリスト 
cell = np.random.randint(0, 2, num_cell) # セルの値をランダムに生成
print("セルオートマトンの初期値")
print(cell)
cell_list.append(cell)
cell_path = str(cell)

point_x = 0
#for q in range(0,num_cell,1):
#    point_x += cell[q] * (2**(-q-1))
#print(float(point_x))
#ファイル書き込み
file_name = "./166.txt"
file = open(file_name, 'w')


for t in range(steps):
    cell_tmp = np.ones(num_cell,dtype=int)
    cell_tmp[0] = rule(cell[num_cell-1],cell[0],cell[1])
    cell_tmp[num_cell-1] = rule(cell[num_cell-2],cell[num_cell-1],cell[0])
    for i in range(1,num_cell-1,1):
        cell_tmp[i] = rule(cell[i-1],cell[i],cell[i+1])
    for q in range(0,num_cell,1):
        point_x += cell[q] * (2**(-q-1))
        # ここ
    cell = np.copy(cell_tmp)
    cell_list.clear()
    cell_list.append(cell)
    file.write(str(float(point_x)) )
#   file.write(str(cell_list))
    #if not t == steps-gosa:
    #    file.write('\n')
    point_x = 0
#    if q == num_cell - 1:
#        file.write(repr(.rstrip()))
file.close()
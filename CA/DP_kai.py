import numpy as np
import matplotlib.pyplot as plt
import sys


ruleNum = int(input('ルール番号を入力：'))
if ruleNum > 256 or 0 > ruleNum:
    print('0 〜 256までの整数を入力してください')
    print('処理終了')
    sys.exit() #ファイルまるごと exit


ruleNumToBinary = format(ruleNum, '08b') # 10 進数 to 2 進数（8桁）
print('2進数：' + str(ruleNumToBinary) + '\n') # 2 進数表記


def rule(cell1, cell2, cell3, binary):

    if cell1 == 0:
        if cell2 == 0:
            if cell3 == 0:
                return binary[7]
            elif cell3 == 1:
                return binary[6]

        elif cell2 == 1:
            if cell3 == 0:
                return binary[5]
            elif cell3 == 1:
                return binary[4]

    elif cell1 == 1:
        if cell2 == 0:
            if cell3 == 0:
                return binary[3]
            elif cell3 == 1:
                return binary[2]

        elif cell2 == 1:
            if cell3 == 0:
                return binary[1]
            elif cell3 == 1:
                return binary[0]


# セルオートマトンの実行 
kyoukaiL = 0
kyoukaiR = 1
steps = 100 # 何ステップまで計算するか
kyoukai_bit = int(5)

# num_cell = 401 # セルの数 
# cell_bit_org = int(101)
# cell_bit_dif = int(101)
num_cell = 101 # セルの数 
cell_bit_org = int(17)
cell_bit_dif = int(17)

cell_list = []# 各世代のセルの情報を記録するリスト 
# cell = np.zeros(num_cell,dtype=int) # セルの初期化 全部 0
cell = np.random.randint(0, 2, num_cell, dtype='l') # セルの値をランダムに生成
cell_tmp_a = cell

cell[int((cell_bit_org/2)-0.5)-1] = 1 # セルに1を代入 
cell[int((cell_bit_org/2)-0.5)] = 1 # セルに1を代入 
cell[int((cell_bit_org/2)-0.5)+1] = 1 # セルに1を代入 

for i in range(5):
    cell[int(cell_bit_org+i)] = 3 # 一つのセルだけに 3 を代入 

cell[int((cell_bit_org + kyoukai_bit + (cell_bit_org/2)-0.5) -1)] = 1
cell[int((cell_bit_org + kyoukai_bit + (cell_bit_org/2)-0.5) +1)] = 1

for j in range(5):
    cell[cell_bit_org + cell_bit_dif + kyoukai_bit + j] = 3 # 一つのセルだけに1を代入 

for k in range(0,17,1): #1段目の差分
    cell[cell_bit_org + cell_bit_dif + 2*kyoukai_bit + k] = cell[k] ^ cell[k+cell_bit_org + kyoukai_bit]

cell_list.append(cell)


#初期値の反転箇所を識別させるために2段目だけ計算させた
# cell_tmp = cell_tmp_a
cell_tmp = np.zeros(num_cell,dtype=int)
for num in cell_tmp_a:
    print(str(cell_tmp[num]) + ' ' + str(cell_tmp_a[num]))
    cell_tmp[num] = cell_tmp_a[num]
cell_tmp[0] = rule(kyoukaiL,cell[0],cell[1],ruleNumToBinary)
cell_tmp[cell_bit_org-1] = rule(cell[cell_bit_org-2],cell[cell_bit_org-1],kyoukaiR,ruleNumToBinary)
cell_tmp[cell_bit_org + kyoukai_bit] = rule(kyoukaiL,cell[cell_bit_org + kyoukai_bit],cell[cell_bit_org + kyoukai_bit + 1],ruleNumToBinary)
cell_tmp[cell_bit_org + kyoukai_bit + cell_bit_dif -1] = rule(cell[cell_bit_org + kyoukai_bit + cell_bit_dif -2],cell[cell_bit_org + kyoukai_bit + cell_bit_dif -1],kyoukaiR,ruleNumToBinary)

for l in range(1,cell_bit_org-1,1):
    cell_tmp[l] = rule(cell[l-1],cell[l],cell[l+1],ruleNumToBinary)

for m in range(cell_bit_org + kyoukai_bit + 1, cell_bit_org + kyoukai_bit + cell_bit_dif -1,1):
    cell_tmp[m] = rule(cell[m-1],cell[m],cell[m+1],ruleNumToBinary)

for n in range(0,cell_bit_org,1):
    cell_tmp[n + cell_bit_org + cell_bit_dif + 2*kyoukai_bit] = cell_tmp[n] ^ cell_tmp[n+cell_bit_org+kyoukai_bit]

for o in range(5):
    cell[int(cell_bit_org + o)] = 3 # 一つのセルだけに 3 を代入 

for p in range(5):
    cell[cell_bit_org + cell_bit_dif + kyoukai_bit + p] = 3 # 一つのセルだけに1を代入 

cell[int((cell_bit_org + kyoukai_bit + (cell_bit_org/2)-0.5))] = 2 #初期値を反転させた場所に色をつけるため
cell = np.copy(cell_tmp)
cell_list.append(cell)


#3段目以降の計算
for t in range(steps-1):
    cell_tmp[0] = rule(kyoukaiL,cell[0],cell[1],ruleNumToBinary) #オリジナルの左端
    cell_tmp[cell_bit_org-1] = rule(cell[cell_bit_org-2],cell[cell_bit_org-1],kyoukaiR,ruleNumToBinary) #オリジナルの右端
    cell_tmp[cell_bit_org + kyoukai_bit] = rule(kyoukaiL,cell[cell_bit_org + kyoukai_bit],cell[cell_bit_org + kyoukai_bit + 1],ruleNumToBinary) #反転パターンの左端
    cell_tmp[cell_bit_org + kyoukai_bit + cell_bit_dif -1] = rule(cell[cell_bit_org + kyoukai_bit + cell_bit_dif -2],cell[cell_bit_org + kyoukai_bit + cell_bit_dif -1],kyoukaiR,ruleNumToBinary) #反転パターンの右端

    for u in range(1,cell_bit_org-1,1):
        cell_tmp[u] = rule(cell[u-1],cell[u],cell[u+1],ruleNumToBinary)

    for v in range(cell_bit_org + kyoukai_bit + 1, cell_bit_org + kyoukai_bit + cell_bit_dif -1,1):
        cell_tmp[v] = rule(cell[v-1],cell[v],cell[v+1],ruleNumToBinary)

    for w in range(0,cell_bit_org,1):
        cell_tmp[w + cell_bit_org + cell_bit_dif + 2*kyoukai_bit] = cell_tmp[w] ^ cell_tmp[w+cell_bit_org+kyoukai_bit]

    for x in range(5):
        cell[int(cell_bit_org + x)] = 3 # 一つのセルだけに 3 を代入 

    for y in range(5):
        cell[cell_bit_org + cell_bit_dif + kyoukai_bit + y] = 3 # 一つのセルだけに1を代入 
    cell = np.copy(cell_tmp)
    cell_list.append(cell)

"""
#差分抽出
differencepattern = []
cell_dp = np.zeros(17,dtype=int)
cell_dp_tmp = np.zeros(17,dtype=int)
for z in range(steps):
    for g in range(0,cell_bit_org,1):
        cell_dp_tmp[g] = cell[g] ^ cell[g + cell_bit_org + kyoukai_bit]
    
    cell_dp = np.copy(cell_dp_tmp)
    differencepattern.append(cell_dp)
"""

save_path = './dp/' + str(ruleNum) + '_dp.png'

plt.figure()
plt.tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.imshow(cell_list, cmap="gray")
plt.savefig(save_path)
plt.show()
plt.close()
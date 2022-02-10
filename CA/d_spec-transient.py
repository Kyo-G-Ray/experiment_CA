import numpy as np
import matplotlib.pyplot as plt
import sys
import math



ruleNum = int(input('ルール番号を入力：'))
if ruleNum > 256 or 0 > ruleNum:
    print('0 〜 256までの整数を入力してください')
    print('処理終了')
    sys.exit() #ファイルまるごと exit

fixedOrNot = input('固定境界→ f，周期境界→ p を入力：')
if fixedOrNot != 'f' and fixedOrNot != 'p':
    print('f or p を入力してください')
    print('処理終了')
    sys.exit() #ファイルまるごと exit


randomOrNot = input('初期ステップ random → r，not random → n を入力：')
if randomOrNot != 'r' and randomOrNot != 'n':
    print('r or n を入力してください')
    print('処理終了')
    sys.exit() #ファイルまるごと exit


ruleNumToBinary = format(ruleNum, '08b') # 10 進数 to 2 進数（8桁）
print('2進数：' + str(ruleNumToBinary) + '\n') # 2 進数表記
print('001 → ' + ruleNumToBinary[6])
print('010 → ' + ruleNumToBinary[5])
print('100 → ' + ruleNumToBinary[3] + '\n')


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
num_cell = 101 # セルの数 
# num_cell = 17 # セルの数 
t_transient = 1000 # 過渡状態 Ttransient = 1000
t_sample = 100 # Tsample = 100 とする
cell_list = [] # 各世代のセルの情報を記録するリスト
cell_list_all = [] # 全世代のセルの情報を記録するリスト
d_array = [0] * t_sample # 各ステップの密度を示す配列 d_array
d_spectrum_sum = 0 # d-spectrum の ＃1(x)
h = [0] * num_cell # 異なる密度がいくつあるか示す配列 h 
τ = 0 # 配列 h の 0 ではない数値を数える（何種類あるか）


# 初期値固定の場合
if randomOrNot == 'n':
    cell = [0] * num_cell # すべて 0 の配列定義
    cell_center = math.ceil(num_cell / 2) - 1 # 配列の中央を求める
    cell[cell_center] = 1

# 初期値ランダムの場合
elif randomOrNot == 'r':
    cell = np.random.randint(0, 2, num_cell) # セルの値をランダムに生成

print("セルオートマトンの初期値")
print(str(cell) + '\n')
cell_list.append(cell)
# cell_list_all.append(cell)
cell_path = str(cell)




if fixedOrNot == 'f':
    if randomOrNot == 'n':
        save_path = './fig_transient/' + str(ruleNum) + '_fixed_ranNo.eps'
        save_path = './fig_transient/' + str(ruleNum) + '_fixed_ranNo.png'
    elif randomOrNot == 'r':
        save_path = './fig_transient/' + str(ruleNum) + '_fixed_ran.eps'
        save_path = './fig_transient/' + str(ruleNum) + '_fixed_ran.png'

elif fixedOrNot == 'p':
    if randomOrNot == 'n':
        save_path = './fig_transient/' + str(ruleNum) + '_periodic_ranNo.eps'
        save_path = './fig_transient/' + str(ruleNum) + '_periodic_ranNo.png'
    elif randomOrNot == 'r':
        save_path = './fig_transient/' + str(ruleNum) + '_periodic_ran.eps'
        save_path = './fig_transient/' + str(ruleNum) + '_periodic_ran.png'


file_name = './data/' + str(ruleNum) + '.txt' # (ルール番号).txt
file = open(file_name, 'w')


for t in range(t_transient + t_sample):
    cell_tmp = np.ones(num_cell, dtype=int)

    # ----- 境界 -----
    # 固定境界条件
    if fixedOrNot == 'f':
        cell_tmp[0] = rule(kyoukaiL, cell[0], cell[1], ruleNumToBinary)
        cell_tmp[num_cell-1] = rule(cell[num_cell-2], cell[num_cell-1], kyoukaiR, ruleNumToBinary)

    # 周期境界条件
    elif fixedOrNot == 'p':
        cell_tmp[0] = rule(cell[num_cell-1], cell[0], cell[1], ruleNumToBinary)
        cell_tmp[num_cell-1] = rule(cell[num_cell-2], cell[num_cell-1], cell[0], ruleNumToBinary)
    # -----------------


    # ---境界以外（内側）---
    for i in range(1, num_cell-1, 1):
        cell_tmp[i] = rule(cell[i-1], cell[i], cell[i+1], ruleNumToBinary)
    # ----------------------


    # d-spectrum の値計算
    for q in range(0, num_cell, 1):
        d_spectrum_sum += cell_tmp[q]


    cell = np.copy(cell_tmp)
    # cell_list.clear()
    cell_list.append(cell)


    if t >= t_transient: # 過渡状態後 (1000 to 1099)
        if d_spectrum_sum != 0:
            d_array[t - t_transient] = d_spectrum_sum # 密度配列に密度追加
            h[d_spectrum_sum] += 1 # 異なる密度を数える配列の d_spectrum 番目をインクリメント
        cell_list_all.append(cell) # グラフ出力用
        # file.write(str(cell_list) + '  ' + str(d_spectrum_sum) + '\n')
    d_spectrum_sum = 0 # 初期化


for x in range(num_cell):
    if h[x] != 0:
        τ += 1


print('各ステップの密度配列')
print(str(d_array) + '\n')
print('異なる密度の数を示す配列')
print(str(h) + '\n')
print('分類識別子τ = ' + str(τ))


plt.figure()
plt.tick_params(labelbottom=False, labelleft=False, bottom=False, left=False)
# plt.imshow(cell_list, cmap="binary")
plt.imshow(cell_list_all, cmap="binary")
plt.savefig(save_path)
plt.show()
plt.close() #大量のグラフを生成する場合、必要

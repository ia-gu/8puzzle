import copy
import sys
'''幅優先アルゴリズム'''
'''盤面は手動生成'''
class OpenList:                          # クラスを定義し，そのオブジェクトを持ったリストで探索する
    def __init__(self,depth,S,pre):
        self.S = S                       # パズルの盤面
        self.pre=pre                     # ひとつ前のオブジェクト（後の配列で用いる）

    def upmove(self,i,j):                # 空洞を上に移動させる関数
        if(self.S[i][j]==0):
            tmp = self.S[i][j]
            self.S[i][j]=self.S[i-1][j]
            self.S[i-1][j]=tmp

    def downmove(self,i,j):              # 空洞を下に移動させる関数
        if(self.S[i][j]==0):
            tmp = self.S[i][j]
            self.S[i][j]=self.S[i+1][j]
            self.S[i+1][j]=tmp

    def leftmove(self,i,j):              # 空洞を左に移動させる関数
        if(self.S[i][j]==0):
            tmp = self.S[i][j]
            self.S[i][j]=self.S[i][j-1]
            self.S[i][j-1]=tmp

    def rightmove(self,i,j):             # 空洞を右に移動させる関数
        if(self.S[i][j]==0):
            tmp = self.S[i][j]
            self.S[i][j]=self.S[i][j+1]
            self.S[i][j+1]=tmp

SIZE = 3
GOAL = [[1,2,3],[8,0,4],[7,6,5]]         # 完成形の定義(0は空洞を表す)
sample = []
print("盤面を入力してください(空洞は０)")   # 問題の手動入力
for i in range(SIZE):
    sample.append([])
for i in range(SIZE):
    sample[i]=list(map(int,input().split()))

tmp=0;cnt=0;num=0;tmp_list=[];goal=[]    # 問題が解決可能か判定する
for i in range(SIZE):
    for j in range(SIZE):
        if(sample[i][j]==0):
            tmp += abs(i-1)+abs(j-1)     # 空洞同士のシティブロック距離を求める
        tmp_list.append(sample[i][j])
        goal.append(GOAL[i][j])
for i in range(len(tmp_list)):
    if(tmp_list[i]!=goal[i]):
        for j in range(len(tmp_list)):   # 入れ替えの場合何手で解決できるかを求める
            if(tmp_list[j]==goal[i]):
                x=tmp_list[i]
                tmp_list[i]=tmp_list[j]
                tmp_list[j]=x
                cnt+=1
if(tmp%2!=cnt%2):                        # 左記の二つの偶奇が異なる場合，8パズルは解けないため終了
    print(f"{sample}は解けません")
    sys.exit()

openlist = [OpenList(0,sample,0)]        # オブジェクト生成
openlist[0].pre = copy.deepcopy(openlist[0])
closedlist = copy.deepcopy(openlist[0])  # append()ではアドレスが共有されてしまうのでdeepcopy()したものを操作する．
already = []                             # すでに出た盤面を保存
times=0

print("探索開始")
while(closedlist.S!=GOAL):
    already.append(closedlist.S)                   # closedlistとalreadyのアドレスが共有されてしまうので，
    closedlist=copy.deepcopy(openlist[0])          # deepcopyで上書きする
    print(f"{times}回目：{closedlist.S}") # 途中経過の表示
    for row in range(SIZE):
        for column in range(SIZE):
            if(closedlist.S[row][column]==0):      # 空洞を探す
                if(row!=0):
                    closedlist.upmove(row,column)            # 空洞を上へ移動させる
                    closedlist.pre = copy.deepcopy(openlist[0])
                    openlist.append(closedlist)              # closedlistとopenlistのアドレスが共有されてしまうので，
                    closedlist=copy.deepcopy(openlist[0])    # deepcopyで上書きする
                if(row!=2):
                    closedlist.downmove(row,column)          # 空洞を下へ移動させる
                    closedlist.pre = copy.deepcopy(openlist[0])
                    openlist.append(closedlist)
                    closedlist=copy.deepcopy(openlist[0])
                if(column!=0):
                    closedlist.leftmove(row,column)          # 空洞を左へ移動させる
                    closedlist.pre = copy.deepcopy(openlist[0])
                    openlist.append(closedlist)
                    closedlist=copy.deepcopy(openlist[0])
                if(column!=2):
                    closedlist.rightmove(row,column)         # 空洞を右へ移動させる
                    closedlist.pre = copy.deepcopy(openlist[0])
                    openlist.append(closedlist)
                    closedlist=copy.deepcopy(openlist[0])
                break
        else:
            continue
        break
    openlist.pop(0)                      # 探索を終えた先頭要素をリストから除外
    while(openlist[0].S in already):     # 盤面が既出の時は探索を飛ばす
        openlist.pop(0)
    closedlist=copy.deepcopy(openlist[0])
    times+=1

print(f"{times}回目で探索終了：{closedlist.S}")
pre=copy.deepcopy(closedlist)

process = []                   # 操作の過程を保持する配列
while(pre.S!=sample):
    process.append(pre.S)     
    pre=copy.deepcopy(pre.pre) # OpenListオブジェクトのpreに保存された，ひとつ前の盤面を渡す
process.append(pre.S)
for i in range(len(process)):  # 最後に，操作の過程を表示する
    print(f"{i}手目：{process[len(process)-1-i]}")
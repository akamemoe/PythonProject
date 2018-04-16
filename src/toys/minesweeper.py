#coding=utf-8

import random
import sys

class Minesweeper():

    def __init__(self):
        super().__init__()
        self._dir = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        self._dd = [(0,1),(0,-1),(1,0),(-1,0)]
        self.MINE = 9 #雷
        self.mine_map = []

        self.CLOSE = 0 #不展示
        self.OPEN = 1 #展示
        self.FLAG = 2 #标记
        
        self.closed = 0 #所有未打开的数目
        self.mine_num = 0

    def _increment(self):
        self.mine_num+=1
        return True

    def _open(self,i,j):
        if self.mark_map[i][j] != self.OPEN:
            self.mark_map[i][j] = self.OPEN
            self.closed-=1

    def _genarate_mine_map(self):
        '生成雷图'
        self.mine_num = 0
        for n in range(self.size):
            self.mine_map.append([self.MINE if random.random() < self.rate and self._increment() else 0 for x in range(self.size)])

    def _check_range(self,ii,jj):
        '检查坐标范围'
        return (ii>=0 and ii<self.size) and (jj>=0 and jj<self.size)

    def _count(self,i,j):
        '计算i,j周围雷的数目'
        for d in self._dir:
            ii = i + d[0]
            jj = j + d[1]
            if self._check_range(ii,jj) and self.mine_map[ii][jj] == self.MINE:
                self.mine_map[i][j] += 1


    def _calc_number(self):
        '计算雷图的数字'
        for i in range(self.size):
            for j in range(self.size):
                if self.mine_map[i][j] != self.MINE:
                    self._count(i,j)

    def _open_around(self,i,j):
        '如果这个地方雷为0,则直接打开周边的地区'
        for d in self._dir:
            ii,jj = i+d[0],j+d[1]
            if self._check_range(ii,jj) and self.mark_map[ii][jj] != self.OPEN:
                # self.mark_map[ii][jj] = self.OPEN
                self._open(ii,jj)
                # print('ropen',ii,jj)
                if self.mine_map[ii][jj] == 0:
                    # print('rdfs',ii,jj)
                    self._dfs(ii,jj)

    def _dfs(self,i,j):
        '深度优先搜索查找附近为0区域'
        self._open_around(i,j)
        for d in self._dd:
            ii,jj = i+d[0],j+d[1]
            if self._check_range(ii,jj) and self.mine_map[ii][jj] == 0 and self.mark_map[ii][jj]!=self.OPEN: 
                # self.mark_map[ii][jj] = self.OPEN
                self._open(ii,jj)
                if self.mine_map[ii][jj] == 0:
                    self._open_around(ii,jj)
                # print('dfs',ii,jj)
                self._dfs(ii,jj)


    def init(self,size=9,rate=0.3):
        'size:地图大小 rate:雷的概率'
        self.size = size
        self.rate = rate
        self.mine_map.clear()
        self._genarate_mine_map()
        self.closed = size*size-self.mine_num
        print(self.mine_num)
        self._calc_number()
        self.mark_map = [[self.CLOSE for y in range(self.size)] for x in range(self.size)]

    def click(self,x,y):
        '点击'
        if self.mine_map[x][y] == self.MINE:
            print('GAME OVER!!!YOU LOSE!!!')
            self.print_mine_map()
            sys.exit(0)
        elif self.mine_map[x][y] == 0:
            # self.mark_map[x][y] = self.OPEN
            self._open(x,y)
            self._dfs(x,y)
        self._open(x,y)
        if self.closed == 0:
            print('GAME OVER!!!YOU WIN!!!')
            sys.exit(0)


    def flag(self,x,y):
        '标记'
        if self.mark_map[x][y] != self.OPEN:
            self.mark_map[x][y] = self.FLAG

    def print_mine_map(self):
        '打印雷图'
        # print(self.mine_map)
        for row in self.mine_map:
            for x in row:
                if x == self.MINE:
                    print('B ',end='')
                else:
                    print(str(x)+' ',end='')
            print()

    def print_mark_map(self):
        '打印标记图'
        # print(self.mark_map)
        for row in self.mark_map:
            for x in row:
                if x == self.OPEN:
                    print('O ',end='') #已经被点开
                elif x == self.FLAG:
                    print('F ',end='') #标记
                else:
                    print('X ',end='') #未打开
            print()

    def print_all(self):
        '综合输出雷图的表示：F(被标记),X(未打开),数字0-8(雷的数量),B(雷)'
        for i in range(self.size):
            for j in range(self.size):
                if self.mark_map[i][j] == self.FLAG:
                    print('F ',end='')
                elif self.mark_map[i][j] == self.OPEN:
                    if self.mine_map[i][j] == self.MINE:
                        print('B ',end='')
                    else:
                        print(str(self.mine_map[i][j])+' ',end='')
                else:
                    print('X ',end='')
            print()

if __name__ == '__main__':
    mine = Minesweeper()
    mine.init(9,0.3)
    while True:
        mine.print_all()
        s = input('>>>').split(' ')
        if s[0] == 'exit':
            break
        else:
            c,x,y = s
            if c == 'click':
                mine.click(int(x),int(y))
            elif c == 'flag':
                mine.flag(int(x),int(y))
            elif c == 'init':
                mine.init(int(x),float(y))
            else:
                print('unknow command.("exit","init $size $rate","click $x $y","flag $x $y")')
# 一些Python小玩具 #

### 1.扫雷(minesweeper.py) ###

- #### 使用：
	在minesweeper.py所在的目录下面打开命令行输入：`python minesweeper.py`,游戏开始运行。默认初始化的地图大小为9\*9，雷出现的概率为0.3。
	游戏运行后你也可以输入命令`init 12 0.4`将地图修改为12\*12，雷概率为0.4。
	输入命令`click x y`来点击对应的点(*0<=x,y<size*)。
	输入命令`flag x y`来标记该点。
	输入`exit`来退出游戏。
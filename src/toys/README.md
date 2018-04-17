# 一些Python小玩具 #

### 1.扫雷(minesweeper.py) ###

- #### 使用：
	在`minesweeper.py`所在的目录下面打开命令行输入：`python minesweeper.py`,游戏开始运行。默认初始化的地图大小为9\*9，雷出现的概率为0.3。  
	游戏运行后你也可以:  
	输入命令`init $size $rate`来重新初始化地图，将地图修改为size\*size大小，雷概率为$rate。例如:`init 12 0.2`;  
	输入命令`click $x $y`来点击对应的点(*0<=x,y<size*)，例如:`click 3 5`;  
	输入命令`flag $x $y`来标记点(x,y)，例如:`flag 4 6`;  
	输入命令`exit`来退出游戏;  
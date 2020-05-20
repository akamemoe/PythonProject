import cv2
import numpy as np


def decete_circle():
    im_origin = cv2.imread('screen.png')
    im_gray = cv2.cvtColor(im_origin,cv2.COLOR_BGR2GRAY)

    print(im_origin.shape)
    #霍夫变换圆检测
    '''
    参数：
    image:　输入图像　必须是灰度图像
    method:检测方法,常用CV_HOUGH_GRADIENT
    dp:检测内侧圆心的累加器图像的分辨率于输入图像之比的倒数，
        如dp=1，累加器和输入图像具有相同的分辨率，如果dp=2，
        累计器便有输入图像一半那么大的宽度和高度
    minDist: 两个圆心之间的最小距离
    param1: 默认100, 是method方法的参数
        在CV_HOUGH_GRADIENT表示传入canny边缘检测的阈值
    param2： 默认100,method的参数， 
        对当前唯一的方法霍夫梯度法cv2.HOUGH_GRADIENT，
        它表示在检测阶段圆心的累加器阈值，
        它越小，就越可以检测到更多根本不存在的圆，
        而它越大的话，能通过检测的圆就更加接近完美的圆形了
    minRadius:默认值0，圆半径的最小值
    maxRadius:默认值0，圆半径的最大值
    '''
    circles= cv2.HoughCircles(im_gray,cv2.HOUGH_GRADIENT,1,100,param1=120,param2=100,minRadius=20,maxRadius=80)

    #输出返回值，方便查看类型
    print('circles:',circles)

    #输出检测到圆的个数
    print("检测出{0}个圆".format(len(circles[0])))
    for c in circles[0]:
        x=int(c[0])
        y=int(c[1])
        r=int(c[2])
        im_origin = cv2.circle(im_origin,(x,y),r,(0,0,255),-1)

    cv2.imshow("img",im_origin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def decete_rectangle():
    im_origin = cv2.imread('screenshot.jpg')
    im_gray = cv2.cvtColor(im_origin,cv2.COLOR_BGR2GRAY)

if __name__ == '__main__':
    decete_circle()


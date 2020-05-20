import matplotlib.pyplot as plt
import numpy as np
import cv2

def main():
    img = cv2.imread('a.jpg')
    hist_cv = cv2.calcHist([img],[1],None,[256],[0,256])
    plt.subplot(121),plt.imshow(img,'gray')
    plt.subplot(122),plt.plot(hist_cv)
    plt.show()

def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    processed_img =  cv2.Canny(processed_img, threshold1 = 100, threshold2=150)
    return processed_img

def test():

    cap = cv2.VideoCapture('H:/nothing/a.mp4')

    ret, last_frame = cap.read()

    if last_frame is None:
        exit()

    while(cap.isOpened()):
        ret, frame = cap.read()

        if frame is None:
            break



        cv2.imshow('frame', frame)
        cv2.imshow('window', process_img(frame))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        last_frame = frame

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test()
    # print(chr(25))
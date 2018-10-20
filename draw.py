# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tkinter.filedialog
from tkinter import *
import re

root = Tk()
label = np.zeros([1, 1], np.uint8)
img1 = np.zeros([1, 1], np.uint8)
img2 = np.zeros([1, 1], np.uint8)
img3 = np.zeros([1, 1], np.uint8)
drawing = False
keeping = False
ix, iy = -1, -1
r, g, b = 0, 0, 0

def drawevent(event, x, y, flags, param):
    global ix, iy, drawing, keeping, img1, img2, img3, label, r, g, b
    operator = cv2.getTrackbarPos('type', "operator")
    thin = cv2.getTrackbarPos('thin', "operator")
    r = cv2.getTrackbarPos('R', "operator")
    g = cv2.getTrackbarPos('G', "operator")
    b = cv2.getTrackbarPos('B', "operator")
    if operator > 1 and (not keeping):
        img2 = img1.copy()
        keeping = True

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        if operator < 2:
            img2 = img1.copy()
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if operator < 2:
                img1 = img2.copy()
            if operator == 0:
                cv2.rectangle(img1, (ix, iy), (x, y), (r, g, b), 1)
            elif operator == 1:
                cv2.circle(img1, (int((ix+x)/2), int((iy+y)/2)), int(((ix-x)**2+(iy-y)**2)**0.5/2), (r, g, b), 1)
            elif operator == 2:
                cv2.rectangle(img1, (x-thin, y-thin), (x+thin, y+thin), (r, g, b), -1)
                cv2.rectangle(label, (x-thin, y-thin), (x+thin, y+thin), (r, g, b), -1)
            elif operator == 3:
                cv2.circle(img1, (x, y), thin, (r, g, b), -1)
                cv2.circle(label, (x, y), thin, (r, g, b), -1)
            elif operator == 4:
                img1[y-thin: y+thin, x-thin:x+thin] = img3[y-thin: y+thin, x-thin:x+thin]
                label[y-thin: y+thin, x-thin:x+thin] = 255
        elif operator > 1:
            img1 = img2.copy()
            if operator == 2:
                cv2.rectangle(img1, (x - thin, y - thin), (x + thin, y + thin), (r, g, b), -1)
            elif operator == 3:
                cv2.circle(img1, (x, y), thin, (r, g, b), -1)
            elif operator == 4:
                img1[y-thin: y+thin, x-thin:x+thin] = img3[y-thin: y+thin, x-thin:x+thin]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        keeping = False
        if operator == 0:
            cv2.rectangle(img1, (ix, iy), (x, y), (r, g, b), cv2.FILLED)
            cv2.rectangle(label, (ix, iy), (x, y), (r, g, b), cv2.FILLED)
        elif operator == 1:
            cv2.circle(img1, (int((ix+x)/2), int((iy+y)/2)), int(((ix-x)**2+(iy-y)**2)**0.5/2), (r, g, b), -1)
            cv2.circle(label, (int((ix+x)/2), int((iy+y)/2)), int(((ix-x)**2+(iy-y)**2)**0.5/2), (r, g, b), -1)
        ix, iy = -1, -1


def emptyfunc(x):
    pass


def process(img, filename):
    global img1, label, img3
    cv2.namedWindow("origin")
    cv2.namedWindow("operator")
    cv2.namedWindow("label")
    cv2.createTrackbar('R', "operator", 0, 255, emptyfunc)
    cv2.createTrackbar('G', "operator", 0, 255, emptyfunc)
    cv2.createTrackbar('B', "operator", 0, 255, emptyfunc)
    cv2.createTrackbar('type', "operator", 0, 4, emptyfunc)  #0:rectangle,1:circle,2:brush,3:brush(circle),4:erase
    cv2.createTrackbar('thin', "operator", 0, 10, emptyfunc)
    img1 = img.copy()
    img3 = img
    label = np.ones(img.shape, np.uint8)*255
    while(1):
        cv2.imshow("origin", img1)
        cv2.imshow("label", label)
        cv2.setMouseCallback("origin", drawevent)
        k = cv2.waitKey(1)
        print(k)
        if k == 107:    #k
            p = re.compile(r'\.\w+$')
            newfilename = p.sub('_label.png', filename)
            cv2.imwrite(newfilename, label)
            break
        elif k == 113:  #q
            break
    cv2.destroyAllWindows()


def initial(filename=''):
    if filename == '':
        print("don't choose file")
    else:
        img = cv2.imread(filename)
        process(img, filename)


def xz():
    filenames = tkinter.filedialog.askopenfilenames()
    if len(filenames) != 0:
        for i in range(0, len(filenames)):
            initial(filenames[i])


lb = Label(root, text='')
lb.pack()
btn = Button(root, text="choose file", command=xz)
btn.pack()
root.mainloop()



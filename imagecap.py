#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import numpy as np
import cv2
import Tkinter as tk
import Image
import ImageTk


cam = cv2.VideoCapture(0)
brightness_init = cam.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)
contrast_init   = cam.get(cv2.cv.CV_CAP_PROP_CONTRAST)
saturation_init  = cam.get(cv2.cv.CV_CAP_PROP_SATURATION)
brightness = brightness_init
contrast   = contrast_init  
saturation = saturation_init
print "brightness init : " + str(brightness)
print "contrast   init : " + str(contrast)
print "saturation init : " + str(saturation)

def quit_(root):
	root.destroy()


def OnPressEnter(event):
	global brightness, contrast, saturation
	brightness = float(root.entry.get())
	contrast = float(root.entry2.get())
	saturation = float(root.entry3.get())
	cam.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,brightness)
	cam.set(cv2.cv.CV_CAP_PROP_CONTRAST,contrast)
	cam.set(cv2.cv.CV_CAP_PROP_SATURATION,saturation)
	print "brightness : " + str(brightness)
	print "contrast   : " + str(contrast)
	print "saturation : " + str(saturation)

def update_image(image_label, cam):
	ret, frame = cam.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	a = Image.fromarray(gray)
	b = ImageTk.PhotoImage(image=a)
	image_label.configure(image=b)
	image_label._image_cache=b
	hist = cv2.calcHist([gray],[0],None,[256],[0,256])
	root.update()

def update_all(root,image_label,cam):
	update_image(image_label,cam)
	root.after(20, func=lambda: update_all(root, image_label, cam))

def reset_value():
	global brightness, contrast, saturation
	brightness = brightness_init
	contrast   = contrast_init
	saturation = saturation_init
	entryVariable.set(brightness)
	entry2.set(contrast)
	saturationVar.set(saturation)
	cam.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,brightness)
	cam.set(cv2.cv.CV_CAP_PROP_CONTRAST,contrast)
	cam.set(cv2.cv.CV_CAP_PROP_SATURATION,saturation)
	

if __name__ == "__main__":
	root = tk.Tk()
	entryVariable=tk.DoubleVar()
	entry2 = tk.DoubleVar()
	saturationVar = tk.DoubleVar()
	root.entry = tk.Entry(root,text="brightness",textvariable=entryVariable)
	entryVariable.set(str(brightness_init))
	root.entry.pack()
	root.entry.bind("<Return>",OnPressEnter)
	root.entry = tk.Entry(root,textvariable=entry2)
	root.entry.pack()
	entry2.set(contrast_init)
	root.entry.bind("<Return>",OnPressEnter)
	root.entry = tk.Entry(root,textvariable=saturationVar)
	root.entry.pack()
	saturationVar.set(saturation_init)
	root.entry.bind("<Return>",OnPressEnter)
	image_label = tk.Label(master=root)
	image_label.pack()
	image_hist = tk.Label(master=root)
	image_hist.pack()
	reset_button = tk.Button(master=root,text='Reset',command=reset_value)
	reset_button.pack()
	quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))
	quit_button.pack()
	root.after(0, func=lambda: update_all(root,image_label,cam))
	root.mainloop()

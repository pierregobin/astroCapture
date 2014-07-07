#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import numpy as np
import cv2
import Tkinter as tk
import Image
import ImageTk


cam = cv2.VideoCapture(0)

class CamParam:
	def __init__(self,widget,camera,param,name) :
		self.initValue = camera.get(param)
		print "Init : " + name + " = " + str(self.initValue)
		self.value = self.initValue
		self.cam = camera
		self.param = param
		self.name = name
		self.variable = tk.DoubleVar()
		self.entry = tk.Entry(widget,textvariable=self.variable)
		self.entry.pack()
		self.variable.set(self.value)
		self.entry.bind("<Return>",self.OnPressEnter)
	def OnPressEnter(self,event):
		self.value = float(self.entry.get())
		self.cam.set(self.param,self.value)
		print self.name + " : " + str(self.value)
	def reset(self):
		self.value = self.initValue
		self.variable.set(self.value)
		self.cam.set(self.param,self.value)
		print "reset : " + self.name + " to " + str(self.value)
	



def quit_(root):
	root.destroy()

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
	brightness.reset()
	contrast.reset()
	saturation.reset()

	

if __name__ == "__main__":
	root = tk.Tk()
	menubar = tk.Menu(root)
	menubar.add_command(label="Capture")
	menubar.add_command(label="Save")
	brightness=CamParam(root,cam,cv2.cv.CV_CAP_PROP_BRIGHTNESS,"brightness")
	saturation=CamParam(root,cam,cv2.cv.CV_CAP_PROP_SATURATION,"saturation")
	contrast=CamParam(root,cam,cv2.cv.CV_CAP_PROP_CONTRAST,"contrast")
	image_label = tk.Label(master=root)
	image_label.pack()
	reset_button = tk.Button(master=root,text='Reset',command=reset_value)
	reset_button.pack()
	quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))
	quit_button.pack()
	root.after(0, func=lambda: update_all(root,image_label,cam))
	root.mainloop()

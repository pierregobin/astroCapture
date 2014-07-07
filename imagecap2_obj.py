#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import numpy as np
import cv2
import Tkinter as tk
import Image
import ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


cam = cv2.VideoCapture(0)
f = Figure(figsize=(5,4), dpi=100)
asub=f.add_subplot(111)
t=np.arange(0.0,3.0,0.01)
s=np.sin(2*np.pi*t)
asub.plot(t,s)

captureStreamCount=0
amountCapture=0
failedCapture=0
maxCaptureStream=20
imageStream=[]
session = 0
record = False

class ButtonOnOff:
	def __init__(self,widget):
		self.root=widget
		self.butOnOff=tk.Button(self.root,text='off',command=self.setOnOff)
		self.butOnOff.pack()
	def setOnOff(self):
		global record
		if self.butOnOff['text']=='on':
			self.butOnOff['text']='off'
			record = False
		else:
			self.butOnOff['text']='on'
			record = True
			global session,captureStreamCount
			session = session+1
			captureStreamCount = 0

class CamParam:
	i=0
	def __init__(self,widget,camera,param,name,minVal,maxVal) :
		self.initValue = camera.get(param)
		self.minVal = minVal
		self.maxVal = maxVal
		self.value = self.initValue
		self.cam = camera
		self.param = param
		self.name = name
		self.label_name = tk.Label(widget,text=name).grid(column=CamParam.i,row=0)

		self.variable = tk.DoubleVar()
		self.entry = tk.Entry(widget,text=self.name,textvariable=self.variable)
		self.entry.grid(column=CamParam.i,row=1)
		self.s  = tk.Scale(widget, from_=0,to=100,orient=tk.HORIZONTAL, command= self.update_value)
		self.s.set(int((self.initValue-self.minVal)/
                               (self.maxVal - self.minVal)*100.0))
		self.s.grid(column=CamParam.i,row=2)
		CamParam.i = CamParam.i + 1
		self.variable.set(self.value)
		self.entry.bind("<Return>",self.OnPressEnter)
		print "Init : " + name + " = " + str(self.initValue)
	def update_value(self,v):
		self.value = self.minVal + 0.01*float(v)*(self.maxVal-self.minVal)
		self.variable.set(self.value)
		self.cam.set(self.param,self.value)
	def OnPressEnter(self,event):
		self.value = float(self.entry.get())
		self.cam.set(self.param,self.value)
		print self.name + " : " + str(self.value)
	def reset(self):
		self.value = self.initValue
		self.s.set(int((self.initValue-self.minVal)/
                               (self.maxVal - self.minVal)*100.0))
		self.variable.set(self.value)
		self.cam.set(self.param,self.value)
		print "reset : " + self.name + " to " + str(self.value)
	



def quit_(root):
	root.destroy()

def update_image(image_label, cam):
	ret, frame = cam.read()
	global amountCapture
	amountCapture = amountCapture + 1
	if ret :
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		global captureStreamCount, imageStream, record, session
		if record:
			captureStreamCount += 1
			cv2.imwrite(filename.get()+"_"+"%03d"%(session)+"_"+"%04d"%(captureStreamCount)+".bmp",frame)
			print "session : "+str(session)+" record : " + str(captureStreamCount)
			
		a = Image.fromarray(frame)
		b = ImageTk.PhotoImage(image=a)
		image_label.configure(image=b)
		image_label._image_cache=b
	else:
		global failedCapture
		failedCapture = failedCapture + 1
	
	root.update()

def update_all(root,image_label,cam):
	update_image(image_label,cam)
	root.after(1, func=lambda: update_all(root, image_label, cam))

def reset_value():
	brightness.reset()
	contrast.reset()
	saturation.reset()
	gain.reset()
	hue.reset()



if __name__ == "__main__":
	root = tk.Tk()
	w1 = tk.Label(master=root)
	w1.pack()
	brightness=CamParam(w1,cam,cv2.cv.CV_CAP_PROP_BRIGHTNESS,"brightness",0.0, 1.0)
	saturation=CamParam(w1,cam,cv2.cv.CV_CAP_PROP_SATURATION,"saturation",0.0,.5)
	contrast=CamParam(w1,cam,cv2.cv.CV_CAP_PROP_CONTRAST,"contrast",0.0,.5)
	gain=CamParam(w1,cam,cv2.cv.CV_CAP_PROP_GAIN,"gain",0.0,1.0)
	hue=CamParam(w1,cam,cv2.cv.CV_CAP_PROP_HUE,"hue",0.0,1.0)
	filename=tk.StringVar()
	fileEntry=tk.Entry(root,text="filename",textvariable=filename)
	fileEntry.pack()
	enregistre=ButtonOnOff(root)
	image_label_parent = tk.Label(master=root)
	image_label_parent.pack()
	image_label=tk.Label(master=image_label_parent)
	image_label.grid(row=0,column=0)
	
	print "image_label - ok"
	reset_button = tk.Button(master=root,text='Reset',command=reset_value)
	reset_button.pack()
	print "reset_button - ok"
	quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))
	quit_button.pack()
	print "quit_button - ok"
	root.after(0, func=lambda: update_all(root,image_label,cam))
	root.mainloop()
	print "total capture  = " + str(amountCapture)
	print "failed capture = " + str(failedCapture)

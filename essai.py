#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import numpy as np
import cv2
import Tkinter
import Image
import ImageTk

MyString="OOOO"
cap = cv2.VideoCapture(0)

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()

		self.entryVariable=Tkinter.StringVar()
		self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
		self.entry.grid(column=0,row=0,sticky='EW')
		self.entry.bind("<Return>",self.OnPressEnter)

		button = Tkinter.Button(self,text=u"Click me!", command=self.OnButtonClick)
		button.grid(column=1,row=0)
		button1 = Tkinter.Button(self,text=u"Quit!", command=quit)
		button1.grid(column=2,row=0)
		label = Tkinter.Label(self, anchor="w", fg="white", bg="blue")
		label.grid(column=0,row=1,columnspan=2,sticky='EW')
		self.grid_columnconfigure(0,weight=1)
		self.grid_columnconfigure(1,weight=1)
		self.grid_columnconfigure(2,weight=1)
		canvas = Tkinter.Canvas(self,width=640,height=480)
		canvas.grid(column=0,row=2,columnspan=3)
		canvas.create_line(0, 0, 200, 100)
		canvas.create_rectangle(50,50,160,80, fill="blue")
		ret, frame = cap.read()
		image=Image.fromarray(frame)
		image=ImageTk.PhotoImage(image)
		canvas.create_image(0,0,image)

	def OnButtonClick(self):
		print "button clicked"
	def OnPressEnter(self,event):
		print "Enter"
		global MyString
		MyString = self.entryVariable.get()

def update_all():
	print MyString
	app.after(100, update_all)
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('mon appli')
	app.after(100,  update_all)
	app.mainloop()


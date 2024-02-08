from tkinter import *  
from PIL import ImageTk,Image  


class App:

	def __init__(self, master):
		self.master=master
		master.title("Visualization for tabular format")

	def main(self):
		# initializing widget
		self.im = Image.open("currElement.png")
		self.render = ImageTk.PhotoImage(self.im)
		top = Toplevel()
		self.myImage = Label(top, image=self.render, text="Hello")
		self.myImage.pack()  


root = Tk()  
myapp = App( master=root)
myapp.main()	
root.mainloop()

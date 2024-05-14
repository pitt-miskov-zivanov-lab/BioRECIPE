from graphviz import Digraph
from tkinter import *
from tkinter import filedialog
import pandas as pd
import argparse


root = Tk()

_COLNAMES = [
	# Provenance attributes
	'Source', 'Reader', 'Evidence', 'Evidence Index', 'Notes',
	# Element variable and attributes
	'Element Variable',
	'Element Name', 'Element Text', 'Element Database', 'Element ID', 'Element Type',
	'Element Agent', 'Element Patient',
	'Element ValueJudgment', 'Element Scope',
	'Element Level', 'Element Change', 'Element Degree',
	'Element Location', 'Element Timing',
	# Interaction function and attributes
	'Interaction Function', 
	'Interaction Name', 'Interaction Text', 'Interaction ID', 'Interaction Type', 
	'Interaction Degree',
	'Interaction Location', 'Interaction Timing',
	# Regulator variable and attributes
	'Regulator Variable',
	'Regulator Name', 'Regulator Text', 'Regulator Database', 'Regulator ID', 'Regulator Type',
	'Regulator Agent', 'Regulator Patient',
	'Regulator ValueJudgment', 'Regulator Scope',
	'Regulator Level', 'Regulator Change', 'Regulator Degree',
	'Regulator Location', 'Regulator Timing',
	# Scoring metrics
	'Reader Count', 'Source Count', 'Evidence Count',
	'Total Score', 'Kind Score', 'Match Level', 'Epistemic Value', 'Belief'
	]


def visualize(element):

	print(element)
	for key, value in element.items():
		if isinstance(value,float):
			element[key] = ''

	dot = Digraph(format='svg')
	dot.attr(rankdir='LR', label=element.get('Evidence'))

	with dot.subgraph(name='cluster_1') as c:
		c.node_attr.update(style='filled')
		c.edge(element.get('Element Text'), element.get('Element Change'), len='1.00', arrowhead='normal') if element.get('Element Change') else print()
		c.edge(element.get('Element Text'), element.get('Element Location'), len='1.00', arrowhead='normal') if element.get('Element Location') else print()
		c.edge(element.get('Element Text'), element.get('Element Timing'), len='1.00', arrowhead='normal') if element.get('Element Timing') else print()
		c.edge(element.get('Element Text'), element.get('Element Degree'), len='1.00', arrowhead='normal') if element.get('Element Degree') else print()
		c.attr(label='Element')
		c.attr(color='blue')

	with dot.subgraph(name='cluster_2') as c:
		c.node_attr.update(style='filled')
		c.edge(element.get('Regulator Text'), element.get('Regulator Change'), len='1.00', arrowhead='normal') if element.get('Regulator Change') else print()
		c.edge(element.get('Regulator Text'), element.get('Regulator Location'), len='1.00', arrowhead='normal') if element.get('Regulator Location') else print()
		c.edge(element.get('Regulator Text'), element.get('Regulator Timing'), len='1.00', arrowhead='normal') if element.get('Regulator Timing') else print()
		c.edge(element.get('Regulator Text'), element.get('Regulator Degree'), len='1.00', arrowhead='normal') if element.get('Regulator Degree')	else print()	
		c.attr(label='Regulator')
		c.attr(color='red')


	dot.edge(element.get('Regulator Text', 'none'), element.get('Element Text', 'none'), label=element.get('Interaction Text', 'NA'), penwidth='3.0')
	dot.node_attr.update(style='filled')
	dot.node(element.get('Regulator Text', 'none'), shape='rectangle')
	dot.node(element.get('Element Text', 'none'), shape='rectangle')


	dot.view()

	

def main():

	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Vizualize standard format (for DySE model assembly or extension).',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='standard format input to be visualized')
	parser.add_argument('viz_options', type=str, choices=['one','all'],
						help='One or multiple DAG visualizations')
	parser.add_argument('index', type=int, help='row index of the element')
	args = parser.parse_args()


	# Command line selection
	if args.viz_options == 'one':
		# get data
		data = pd.read_excel(args.input_file)
		data_dicts = data.to_dict(orient='index')
		#visualize
		visualize(data_dicts[args.index])

	# GUI
	elif args.viz_options == 'all':
		myapp = App( master=root)
		myapp.master.title("Visualization for tabular format")
		myapp.master.minsize(640, 320)
		myapp.mainloop()		
	
	else:
		raise InputError('Unrecognized input format')


class App(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.row = 0
		
		# defining all widgets
		self.returnButton = None
		self.chooseButton = None
		self.previous = None
		self.next = None
		self.returnButton = None
		self.searchbar = None
		self.submit = None
		
		# defining all search variab;es
		self.search_key = None
		self.query_result = []
		self.query_index = 0

		# initializing widget
		self.grid(sticky="nsew")
		self.homePage()

	def homePage(self):
		# Text box
		self.title = Label(self, text="Welcome to the translation visualizer!")
		self.title["font"] = ["calibri", 16, "normal"]
		self.title.grid(row=0, column=0, padx=20)

		# File Select Button
		self.chooseButton = Button(self)
		self.chooseButton["text"] = "Select File"
		self.chooseButton["command"] = self.selectFile
		self.chooseButton["width"] = 10
		self.chooseButton["height"] = 3
		self.chooseButton["border"] = 3
		self.chooseButton["font"] = ["calibri", 24, "bold"]
		self.chooseButton["anchor"] = "center"
		self.chooseButton.grid(row=0, column=1, padx=50, pady=80)

		
	def navigation(self):

		# if returning from query
		if self.returnButton:
			self.returnButton.destroy()
			self.searchbar.destroy()
			self.submit.destroy()

		# previous vis
		self.previous = Button(self)
		self.previous["text"] = "Previous"
		self.previous["command"] = self.previousViz
		self.previous["width"] = 10
		self.previous["height"] = 3
		self.previous["border"] = 3
		self.previous["font"] = ["calibri", 24, "bold"]
		self.previous["anchor"] = "center"
		self.previous.grid(row=1, column=0, padx=30, pady=30)

		# next vis
		self.next = Button(self)
		self.next["text"] = "Next"
		self.next["command"] = self.nextViz
		self.next["width"] = 10
		self.next["height"] = 3
		self.next["border"] = 3
		self.next["font"] = ["calibri", 24, "bold"]
		self.next["anchor"] = "center"
		self.next.grid(row=1, column=1, padx=30, pady=30)

		#Search Button
		self.search = Button(self, text="Search",
						   command=self.searchViz, width=10, height=3,
						   border=3, font=["calibri",24,"bold"])
		self.search.grid(row=0, column=1, padx=30, pady=30)

	def previousViz(self):
		if self.row != 0:
			self.row -=1
			visualize(self.data_dicts[self.row])
			self.title['text'] = "Now showing row "+str(self.row)+"\n"
		else:
			self.title['text'] = "Too far, go the other way or quit!"


	def nextViz(self):
		if self.row < self.length-1:
			self.row +=1
			visualize(self.data_dicts[self.row])
			self.title['text'] = "Now showing row "+str(self.row)+"\n"
		else:
			self.title['text'] = "Too far, go the other way or quit!"

	def searchViz(self):
		# entering from navigation window
		self.next.destroy()
		self.previous.destroy()
		self.search.destroy()

		self.returnButton = Button(self,text="back", command=self.navigation, width=10, height=3, border=3)
		self.returnButton["font"] = ["calibri", 24, "bold"]
		self.returnButton.grid(row=0,column=1,padx=30, pady=30)

		self.searchbar = Entry(self)
		self.searchbar.grid(row=1,column=0,padx=30, pady=30)

		self.submit = Button(self, text="submit query", command=self.queryViz,width=10, height=3, border=3)
		self.submit["font"] = ["calibri", 24, "bold"]
		self.submit.grid(row=1,column=1,padx=30, pady=30)


	def queryViz(self):
		if self.search_key == self.searchbar.get():
			print("next item in search")
			self.query_index +=1
			# resets index value if too high
			if self.query_index >= len(self.query_result):
				self.query_index = 0
			# displaying first item of results
			if self.query_result:
				self.row = self.query_result[self.query_index][1]
				visualize(self.query_result[self.query_index][0])
				self.title['text'] = "Now showing row "+str(self.row)+"\n"
			else:
				self.title['text'] = "No matches found"

		else:
			self.search_key = self.searchbar.get()
			self.query_index = 0;
			self.query_result = []
			# creating results list
			element_index = 0
			for row, element in self.data_dicts.items():
				element_index +=1
				print(element)
				for key, value, in element.items():
					if isinstance(value,float):
						self.data_dicts[row][key] = ''
					if self.search_key in self.data_dicts[row][key]:
						print("hey I found something")
						self.query_result.append((self.data_dicts[row],element_index))
						break
			# displaying first item of results
			if self.query_result:
				print(self.query_result)
				self.row = self.query_result[0][1]
				visualize(self.query_result[0][0])
				self.title['text'] = "Now showing row "+str(self.row)+"\n"
			else:
				self.title['text'] = "No matches found"


	def selectFile(self):
		# Ask for a file to read
		filePath = filedialog.askopenfilename()
		if '.xlsx' in filePath:
			# get data
			data = pd.read_excel(filePath)
			self.data_dicts = data.to_dict(orient='index')
			self.length = len(self.data_dicts)
			try:
				visualize(self.data_dicts[0])
				# update gui
				self.title['text'] = "Now showing row 0"
				self.chooseButton.destroy()
				self.navigation()
			except KeyError:
				self.title['text'] = "File is empty, please select another"
				self.chooseButton.pack(side="top", padx=30, pady=30, fill="both")

		else:
			self.title['text'] = "File is not a spreadsheet, please select another"
			self.chooseButton.pack(side="top", padx=30, pady=30, fill="both")




if __name__ == '__main__':
	main()
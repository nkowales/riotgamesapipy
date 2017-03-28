from Tkinter import *
from id2name import NAME2ID
from id2name import ID2NAME
from nicknames2names import NICKNAMES2NAMES
import tkMessageBox
import dbfuncs
pos = ['supp', 'bot', 'mid', 'jungle', 'top']
posnn = {'support' : 'supp', 'sup' : 'supp', 'adc' : 'bot', 'bottom' : 'bot', 'middle' : 'mid', 'solomid' : 'mid', 'jung' : 'jungle', 'jun' : 'jungle', 'j' : 'jungle'}
top = Tk()
F0 = Frame(top)
F1 = Frame(F0)
F2 = Frame(F0)
F3 = Frame(F0)
F0.pack(side = TOP)
F1.pack( side = TOP )
F2.pack()
F3.pack( side = BOTTOM )
def helloCallBack():
	try:
		if E2.get() not in NAME2ID:
			if E2.get() in ID2NAME:
				tempname = ID2NAME[E2.get()]
			elif E2.get().lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[E2.get().lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = E2.get()
		if E3.get().lower() not in pos:
			if E3.get().lower() not in posnn:
				raise Exception('invalid position')
			else:
				postemp = posnn[E3.get().lower()]
		else:
			postemp = E3.get().lower()
		results = dbfuncs.suggestion(tempname, E1.get(), postemp)
		tkMessageBox.showinfo( "Suggested Champions", str(results))
		
	except Exception as e:
		tkMessageBox.showinfo("Suggested Champions", str(e))

L1 = Label(F1, text="Summoner Name")
L1.pack( side = LEFT)
E1 = Entry(F1, bd =5)
E1.pack(side = RIGHT)
L2 = Label(F2, text="Opponent Champion")
L2.pack( side = LEFT)
E2 = Entry(F2, bd =5)
E2.pack(side = RIGHT)
L3 = Label(F3, text="Position")
L3.pack( side = LEFT)
E3 = Entry(F3, bd =5)
E3.pack(side = RIGHT)
B = Button(top, text ="Submit", command = helloCallBack)
B.pack()
top.mainloop()

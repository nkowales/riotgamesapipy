from Tkinter import *
import tkMessageBox
import dbfuncs
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
	#try:
	results = dbfuncs.suggestion(E2.get(), E1.get(), E3.get())
	tkMessageBox.showinfo( "Suggested Champions", str(results))
	#except:
		#tkMessageBox.showinfo("Suggested Champions", "Error")

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

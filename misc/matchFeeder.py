import mysql.connector
import dbfuncs
from id2name import NAME2ID

with open('goldresults.txt', 'r') as infile:
	lines=[]
	winner=0
	for line in infile:
		lines.append(line)
		if len(lines) == 11:
			matchID = lines[0]
			roledict = {}
			roledict2 = {}
			for i in range(5):
				try: 
					role, champ, win = lines[i+1].split()
					if win == "True":
						winner="1"
					else:
						winner="0"
					roledict[role] = champ
				except ValueError:
					role, champ1, champ2, win = lines[i+1].split()
					roledict[role] = champ1 + ' ' + champ2
			for j in range(5):
				try:
					role, champ, win = lines[j+6].split()
					roledict2[role] = champ
				except ValueError:
					role, champ1, champ2, win = lines[j+6].split()
					roledict2[role] =  champ1 + ' ' + champ2

			dbfuncs.insertgame(matchID, NAME2ID[roledict["TOP"]], NAME2ID[roledict2["TOP"]], NAME2ID[roledict["JUNGLE"]], NAME2ID[roledict2["JUNGLE"]], NAME2ID[roledict["MIDDLE"]], NAME2ID[roledict2["MIDDLE"]], NAME2ID[roledict["ADCARRY"]], NAME2ID[roledict2["ADCARRY"]], NAME2ID[roledict["SUPPORT"]], NAME2ID[roledict2["SUPPORT"]], winner)
			lines = []
	

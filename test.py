import mysql.connector
import dbfuncs
from id2name import ID2NAME
#f = open("testing.txt", 'w')
#f.write('test2')
#f.close()
#stuff = dbfuncs.findrates('top', '64')
#dbfuncs.insertgame('2455304400', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '1')
#print dbfuncs.suggestion('Zac','Null 11 Ordo', 'top')
#print ID2NAME['114']
#stuff = dbfuncs.findbest('top', '24')
#print str(stuff)
print str(dbfuncs.findsvb('Null 11 Ordo', 'Ashe'))

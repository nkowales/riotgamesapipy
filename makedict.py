import riotgamesapipy
from info import API_KEY
import time

#create dictionaries of champion names to champion ids and champion ids to champion names

rito = riotgamesapipy.riotgamesapipy(API_KEY)
f = open('id2name.py', 'w')
st = 'NAME2ID = {'

champs = rito.getChampionData()

for key in champs['data']:
	st = st +'"' + str(champs['data'][key]['name']) + '" : "' + str(champs['data'][key]['id']) + '", '

st = st + "}\n"
st = st.replace(", }\n", "}\n")
f.write(st)
st2 = 'ID2NAME = {'

for key in champs['data']:
	st2 = st2 + '"' + str(champs['data'][key]['id']) + '" : "' + str(champs['data'][key]['name']) + '", '

st2 = st2 + '}\n'
st2 = st2.replace(', }\n', '}\n')
f.write(st2)
f.write('\n')
f.close()


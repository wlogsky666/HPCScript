import json


Node = {'node'+str(i) for i in range(1, 45)}
Node.update({'bigmem'+str(i) for i in range(1, 7)})
Node.update({'gpu'+str(i) for i in range(1, 3)})

nnnnn = dict()

for n in Node:
	nnnnn[n] = 0

with open('SendTimes', 'w') as st:
	json.dump(nnnnn, st)


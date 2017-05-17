import json
import os

Node = { node.strip() for node in os.popen('pbsnodes -l all | cut -d" " -f1')}
NodeTemp = dict()

for n in Node:
        NodeTemp[n] = 0

NodeTemp['oss1'] = 0
NodeTemp['oss2'] = 0
NodeTemp['mds']  = 0


with open('SendTimes.json', 'w') as st:
        json.dump(NodeTemp, st)

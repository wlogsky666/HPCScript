import json
import os

Node = { node.strip() for node in os.popen('pbsnodes -l all | cut -d" " -f1')}
Node.update(['oss1', 'oss2', 'mds'])
NodeTemp = dict()

for n in Node:
        NodeTemp[n] = 0

with open('SendTimes.json', 'w') as st:
        json.dump(NodeTemp, st)

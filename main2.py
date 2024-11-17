import json
import re

f = open('/home/jordina/Desktop/datathon24/datathon_participants.json')

data = json.load(f)
n = len(data)

count = 0
for i in data:
    # print("person ", count)
    s = i["objective"]

    print(s)
    print()
    count += 1


f.close()
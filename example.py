from rich import print
import pandas as pd

from participant import load_participants

data_path = "data/datathon_participants.json"
participants = load_participants(data_path)[:20]

def format_habilities(df):
  dif_habilities = set([k for s in df['programming_skills'] for k in s.keys() ])
  num_habilities = len(dif_habilities)
  mydict = {}
  cnt = 0
  for hab in dif_habilities:
    mydict[hab] = cnt
    cnt += 1
  totalLlistes = []
  for p in df['programming_skills']:
    newVec = [0]*num_habilities
    for h, l in p.items():
      newVec[mydict[h]] = l
    totalLlistes.append(newVec)
  df['programming_skills'] = totalLlistes

def calc_weights(v1, v2):
  n = len(v1)
  d = sum([max(v1[i], v2[i]) for i in range(n)])
  return d/(5*n)

df = pd.DataFrame(data=[[p.id, p.programming_skills] for p in participants], 
                         columns=['id', 'programming_skills'])
print(df)
format_habilities(df)
print(df)

for i in range(20):
	for j in range(i+1, 20):
		print(calc_weights(df['programming_skills'][i], df['programming_skills'][j]))







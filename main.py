import json, re, string
import numpy as np

f = open('/home/jordina/Desktop/datathon24/datathon_participants.json')

data = json.load(f)
n = len(data)

# dic = {"prize-hunting" : ["crush it", "take home the top prize", "come out on top", "ready to take on the competition", "outsmart and outwork", "bring home the win", "laser-focused on winning", "thrill of victory", "game-changing solution", "competing against the best", "ready to push myself to the limit", "outshine the competition", "competing to win" , "bring it on","win", "i'm here to win","skils", "challange", "push myself", "first place", "winner", "come out on top", "trophy", "winning", "competition", "compete", "prize", "gold", "prize-worthy", "top spot"],
#        "portfolio-building": ["build", "portfolio", "sweet new techniques", "machine learning", "demonstrate my growth", "tangible projects", "fun projects", "refining my skills"],
#        "learning new skills" : ["growth", "learn", "learning", "skills", "learn from others", "mentorship sessions", "new technologies", "better programmer", "exposed to ideas"],
#        "meeting new people": ["meet", "awesome new friends", "connections", "community", "vibing", "sharing stories", "picking brains", "try new things", "walk away with memories", "meaningful connections"]}

dic = {
    "prize-hunting" : [ 
        "come out on top", "trophy", "competition", 
        "prize", "gold", "victory",
        "come out on top", "outsmart and outwork",
        "game changing solution", "bring it on", "win", "push myself", "first place", "trophy",
        "compete", "competing", "crush", "all in", "gold", "contender", "top spot", 
        "champion" ,"victorious", "crown", 
        "laser focus",
    ],
    "portfolio-building": [
        "portfolio", "techniques", "machine learning", "projects", "abilities", 
        "hands-on experience", "applications", "show off",
        "projects that stand out", "expand my toolkit", "solutions"
    ],
    "learning new skills" : [
        "growth", "learn", "skill",
        "better programmer",
        "mentorship sessions", "technologies", 
        "better programmer", "exposed to ideas",  "push my limits", "tool", 
        "expand my knowledge", "level up", "challenges", "improve my coding", 
        "expertise", "step up my game", "absorb knowledge", 
        "refine my techniques"
    ],
    "meeting new people": [
        "meet", "vibes", "awesome new friends", "connections", "community", "vibing", "sharing stories", "picking brains", 
        "try new things", "memories", "networking", "collaborating", 
        "conversation", "expand my network", "work with talented people", "sharing ideas", "work with others", 
        "friends", "team building", "meeting fellow coders", "building relationships", 
        "find a coding buddy", "gather new perspectives", "friendship", "socializing", "hang out", "buddy"
    ]
}

vector = []

def remove_punctuation(s):
    ans = ""
    for c in s:
        if 'a' <= c <= 'z' or c == "'" or c == ' ':
            ans += c
    return ans

count = 0
for i in data:
    # if i["name"] == 'Rita Silva':
    # print("person ", count)
    v = [0, 0, 0, 0]
    s = i["objective"].lower()
    sentences = re.split(r'(?<=[.!?,]) +', s)
    # print(s)
    for j in sentences:
        j = remove_punctuation(j)
        # print(j)
        # print(v)

        if "not" in j or "n't" in j:
            flag = False
        else:
            flag = True
        
        if flag:
            for i in range(len(j)):
                for expr in dic['prize-hunting']:
                    if(j[i: i+len(expr)] == expr):
                        # print(j[i:i+len(expr)])
                        v[0] += 1
                for expr in dic['portfolio-building']:
                    if(j[i: i+len(expr)] == expr):
                        v[1] += 1
                for expr in dic['learning new skills']:
                    if(j[i: i+len(expr)] == expr):
                        v[2] += 1
                for expr in dic['meeting new people']:
                    if(j[i: i+len(expr)] == expr):
                        v[3] += 1

        # if not flag and "win" in j:
        #     v[0] = 0
    
    # print(v)
    # if v[0] >= 4:
    # print(s)
    # print(v)
    norma = np.linalg.norm(v)
    v[0] /= norma
    v[1] /= norma
    v[2] /= norma
    v[3] /= norma


    vector.append(v)


for i, person in enumerate(data):
    person['objective'] = vector[i]

f.close()

with open('/home/jordina/Desktop/datathon24/datathon_participants_updated.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
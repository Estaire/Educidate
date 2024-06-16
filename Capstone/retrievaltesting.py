import json
proxy="awsdwac"
#f = open('Codes.json')\
exists= False

with open('Users.json','r+') as f:
    data = json.load(f)
    for x in data['Users']:
        if x['username'] == "wsdaczx":
            print(x['courses'])
            x['courses']= ["COPMP1127","COMP1126"]
            f.seek(0)
            json.dump(data,f,indent = 4)
            f.truncate()            
    
f.close()
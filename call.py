import requests,sys,json
from datetime import datetime,timedelta

def tell(text):
    print(text)
    import requests
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {'text': text}
    requests.post("http://gobbelz.shack/say/",
            data=json.dumps(data), headers=headers)

# alert 1 day before
alert_offset= timedelta(days=1)
# latest call is at 9AM
last_call= timedelta(hours=9)
ret= requests.get('http://openhab.shack/muellshack/gelber_sack').json()
next_date = datetime.strptime(ret['gelber_sack'],'%Y-%m-%d') + last_call
now = datetime.now() # + timedelta(days=int(sys.argv[1]))

if next_date - alert_offset < now  < next_date:
    tell('Your attention please.This is a public service announcement.')
    tell('It is yellow trashbag day, please bring out the trash! Thank you.' )
else:
    # works, haha
    #print('es ist kein gelber sack tag')
    pass

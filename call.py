import requests,sys,json
from datetime import datetime,timedelta
import json

cfg_file="./tell.json"
try:
    pw = json.load(open(cfg_file))["client-mpd-pw"]
except:
    print("cannot load config file {}".format(cfg_file))
    sys.exit(1)

def tell(text):
    print(text)
    import requests
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {'text': text}
    print(requests.post("http://gobbelz.shack/say/",
            data=json.dumps(data), headers=headers))

import paramiko, base64
key = paramiko.RSAKey(data=base64.decodestring(b"AAAAB3NzaC1yc2EAAAADAQABAAABAQCxn9siIjgrMngz3GXGgeujq74PM8t/2S8G98P4M/vJ1fwULJCw01TxmhVF699CrqRh040YYuUVlxtwbc0ZySO2M2phTNsJgfX3vnpTkI5AeQ6RQ7FbqXLheqwnfgQoXLQWftzQWtzUGnqqcf3uicJ2No2XoNG+UrYaKU8Xq6crhTSrhjwR9ijJcpoajXgUr6xiVamal+l5oZjvOUjfYZrrDKtA1BORYA5spzb8/kHEhQ5Za6Wb+m2SJAJ5tBL0xxdpOLJ6fUoned0+n3/f217cUcWOlKMVG5ujaGkye43sXmPhN5sNwWd5tCD7XVv7iKgEFjIUibqguH6WyD9qkzTl"))

def tell_mpd(text):
    print(text)
    client = paramiko.SSHClient()
    client.get_host_keys().add('client.lounge.mpd.shack', 'ssh-rsa', key)
    client.connect('client.lounge.mpd.shack', username='root', password=pw)
    stdin, stdout, stderr = client.exec_command('pkill ogg123; espeak "{}" -a 200 -s 150 -v de'.format(text))
    for line in stdout:
        print( '... ' + line.strip('\n'))
        client.close()



if __name__ == "__main__":
    # alert 1 day before
    alert_offset= timedelta(days=1)
    # latest call is at 9AM
    last_call= timedelta(hours=9)
    for i in ['gelber_sack','restmuell','papiermuell']:
        ret= requests.get('http://openhab.shack/muellshack/{}'.format(i)).json()
        next_date = datetime.strptime(ret[i],'%Y-%m-%d') + last_call
        now = datetime.now() # + timedelta(days=int(sys.argv[1]))
        txt = i.replace('_',' ').replace('ue','ü').capitalize()
        if next_date - alert_offset < now  < next_date:
            tell_mpd('Achtung morgen wird der {} abgeholt!'.format(txt))
            #tell('Your attention please.This is a public service announcement.')
            #tell('It is yellow trashbag day, please bring out the trash! Thank you.' )
        else:
            # works, haha
            print('es ist kein {} tag'.format(txt))
            tell_mpd('es ist kein {} tag'.format(txt))
            pass

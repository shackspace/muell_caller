#!/usr/bin/env python
"""usage: call-muell [options] [loop [TIMEOUT]]

Options:
    --cfg=FILE          Configuration file with the mpd pw [Default: ./tell.json]
    --mode=MODE         How to call the muell,can be "mpd" or "gobbelz" [Default: mpd]

When looping, the TIMEOUT is the time to wait in MINUTES before continuing,
defaults to 60
"""
import requests,sys,json
from datetime import datetime,timedelta
import json
import logging
import sys
import traceback

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.setLevel(logging.INFO)

def tell_gobbelz(text):
    print(text)
    import requests
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {'text': text}
    print(requests.post("http://gobbelz.shack/say/",
            data=json.dumps(data), headers=headers))


def tell_mpd(text,sshcfg):
    import paramiko, base64
    user = sshcfg["client-mpd-user"]
    pw = sshcfg["client-mpd-pw"]
    pubkey = paramiko.RSAKey(data=base64.decodestring(sshcfg['client-mpd-pubkey'].encode()))
    log.info("tell_mpd: " + text)

    client = paramiko.SSHClient()
    client.get_host_keys().add('client.lounge.mpd.shack', 'ssh-rsa', pubkey)
    client.connect('client.lounge.mpd.shack', username=user, password=pw)
    # TODO: watch out for doublequotes and env vars
    stdin, stdout, stderr = client.exec_command('pkill ogg123; espeak "{}" -a 200 -s 150 -v de'.format(text))
    for line in stdout:
        log.info( '... ' + line.strip('\n'))
        client.close()


def do_call(mode,cfg):
    # alert 1 day before
    alert_offset= timedelta(days=1)
    # latest call is at 9AM
    last_call= timedelta(hours=9)
    for i in ['gelber_sack','restmuell','papiermuell']:
        ret= requests.get('http://openhab.shack/muellshack/{}'.format(i)).json()
        next_date = datetime.strptime(ret[i],'%Y-%m-%d') + last_call
        now = datetime.now()
        txt = i.replace('_',' ').replace('ue','ü').capitalize()
        if ret['main_action_done']:
            log.info('{} bereits herunter gebracht'.format(txt))
        elif next_date - alert_offset < now  < next_date:
            announcement = 'Achtung morgen wird der {} abgeholt!'.format(txt)
            if mode == "mpd":
                tell_mpd(announcement,cfg['ssh'])
            elif mode == "gobbelz":
                tell_gobbelz(announcement)
        else:
            # works, haha
            log.info('es ist kein {} tag'.format(txt))
            # tell_mpd('es ist kein {} tag'.format(txt))
            pass

def main():
    from docopt import docopt
    from time import sleep
    args = docopt(__doc__)
    loop = args['loop']
    mode = args['--mode']
    cfgfile = args['--cfg']
    try:
        cfg = json.load(open(cfgfile))
    except Exception as e:
        log.error("cannot load config file {}".format(cfgfile))
        sys.exit(1)

    while loop:
        timeout = int(args['TIMEOUT'] or 60)*60
        try:
            do_call(mode,cfg)
        except Exception as e:
            log.warn("Unable to make call, reason: {}".format(e))
            traceback.print_exc(file=sys.stderr)
        log.info("sleeping for another {} minutes".format(timeout/60))
        sleep(timeout)
    else:
        do_call(mode,cfg)

if __name__ == "__main__":
    main()

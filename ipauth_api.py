#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import abort
from logging.handlers import RotatingFileHandler
import sqlite3
import subprocess
import bcrypt

app = Flask(__name__)
# Remove the comments bellow to enable DEBUG mode
#app.debug = True

if ( app.debug ):
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication( app.wsgi_app, True )

@app.route("/auth/", methods=['GET'])
def authorized():

    try:
        username = request.args['username']
        key = request.args['key']
        skey = request.args['skey']
        #visitorip = request.remote_addr
        visitorip = request.headers.get('X-Real-IP')

    except:
        return abort(400)


    sql_query = 'SELECT key, skey FROM USERS WHERE user = ?'


    try:
        db = sqlite3.connect('.userDB.db')
        c = db.cursor()
        params = (username,)
        c.execute(sql_query, params)
        result = c.fetchone()
    except:
        return abort(403)

    if result is None:
        return abort(403)

    hashed_key = result[0]
    hashed_skey = result[1]

    if not (
        bcrypt.hashpw(key.encode('utf-8'), hashed_key.encode('utf-8')) == hashed_key and
        bcrypt.hashpw(skey.encode('utf-8'), hashed_skey.encode('utf-8')) == hashed_skey
        ):
            return abort(403)

    sql_query = 'SELECT user, old_ip, current_IP FROM users WHERE user = ?'

    try:
        db = sqlite3.connect('.userDB.db')
        c = db.cursor()
        params = (username,)
        c.execute(sql_query, params)
        result = c.fetchone()
    except:
        return abort(403)

    if result is None:
        return abort(403)

    ip_old = result[1]
    ip_current = result[2]

    if ip_current == visitorip:
        return 'The IP still the same for the user {}'.format(username)

    try:
        sql_query = 'UPDATE users SET old_ip = ? WHERE user = ?'
        params = (ip_current, username)
        c.execute(sql_query, params)
        db.commit()
    except Exception as e:
        db.rollback()

    try:
        sql_query = 'UPDATE users SET current_IP = ? WHERE user = ?'
        params = (visitorip, username)
        c.execute(sql_query, params)
        db.commit()
    except Exception as e:
        db.rollback()

    try:
        #Add the new IP to iptables CHAIN IPAUTH-API
        iptables_opt_add = {'protocol': 'tcp', 'port': 20981, 'ipsource': visitorip}
        iptables_add = '/usr/bin/sudo /sbin/iptables -I IPAUTH-API -s {ipsource} -p {protocol} --dport {port} -j ACCEPT'.format(**iptables_opt_add)
        p = subprocess.Popen(iptables_add.split(' '))
        p.communicate()
        p.wait()
    except subprocess.CalledProcessError as e:
        abort(500)

    if ip_old is not None:
        try:
            #Remove the old_IP from iptables CHAIN IPAUTH-API
            iptables_opt_del = {'protocol': 'tcp', 'port': 20981, 'ipsource': ip_current}
            iptables_del = '/usr/bin/sudo /sbin/iptables -D IPAUTH-API -s {ipsource} -p {protocol} --dport {port} -j ACCEPT'.format(**iptables_opt_del)
            p = subprocess.Popen(iptables_del.split(' '))
            p.communicate()
            p.wait()
        except subprocess.CalledProcessError as e:
            abort(500)


    resp = '''Attention: This URL is only for authorized people. Details:<br />
    Username: <b>{}</b> has the IP <b>{}</b> whitelisted.
    '''.format(username, visitorip)

    return resp


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8081)

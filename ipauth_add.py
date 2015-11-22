#!/usr/bin/env python

import argparse
import sys
import os
import sqlite3
import binascii
import base64
import hashlib
import bcrypt
import random
import pwd
import logging
import datetime

LOG_FILE = 'log/ipauth-add.log'

def main(user,email):

    try:
        pwd.getpwnam(user)
    except KeyError:
        print '[!] Error: username {} was not found in the local system account!'.format(user)
        print 'The user must exists on the loca system account'
        sys.exit(1)

    db = sqlite3.connect('.userDB.db')
    c = db.cursor()

    sql_query = 'SELECT user FROM users WHERE user = ?'
    c.execute(sql_query, (user,))
    result = c.fetchone()
    if result is not None:
        print '[!] Error: Username already exist on database.'
        sys.exit(1)

    key = binascii.hexlify(os.urandom(24))
    skey = base64.b64encode(hashlib.sha256( str(random.getrandbits(256))
        ).digest(),
        random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])
        ).rstrip('==')

    salt = bcrypt.gensalt()

    try:
        sql_query = 'INSERT INTO users (user, mail, key, skey) VALUES (?, ?, ?, ?)'
        params = (user, email, bcrypt.hashpw(key.encode('utf-8'), salt),  bcrypt.hashpw(skey.encode('utf-8'), salt))
        c.execute(sql_query, params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
        sys.exit(1)
    finally:
        print "[+] User created! -> \nUser: {} \nE-mail: {} \nKey: {} \nSecret Key: {}".format(user, email, key, skey)
        print "[+] Bookmark the following link: http://yourserver.com/auth/?username={}&key={}&skey={}".format(user, key, skey)
        logger.info('User: {} created at {}.'.format(user, datetime.datetime.now()))
        db.close()


if __name__ == "__main__":

    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
    logger = logging.getLogger()

    parser = argparse.ArgumentParser(description='Add user on the whitelist IP for servers.')
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-m', '--mail', required=True)
    args = parser.parse_args()

    main(args.user, args.mail)

# hacker_diary_interface by Gabriele Musco (GabMus)
"""
Copyright (C) 2017 Gabriele Musco
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
"""
 
from urllib import urlencode
import requests
import time
import hashlib
import string
 
from random import choice
 
token=None
flags=dict()
 
def _makeRequest(server, uri, method, data, token):
    addr='http://'+server+uri
    if data and method=='POST':
        if token:
            r = requests.post(addr, data=data, headers={'Authorization': 'JWT '+token})
        else:
            r = requests.post(addr, data=data)
    else:
        if token:
            r = requests.get(addr, headers={'Authorization': 'JWT '+token})
        else:
            r = requests.get(addr)
    return r.json()
 
def _register(server, username, password, first_name=None, last_name=None, email=None):
    data={'username':username, 'password':password}
    if first_name:
        data['first_name']=first_name
    if last_name:
        data['last_name']=last_name
    if email:
        data['email']=email
    return _makeRequest(server, '/register/', 'POST', data, None)
 
def _login(server, username, password):
    data={'username': username, 'password': password}
    return _makeRequest(server, '/login/', 'POST', data, None)
 
def _getEntry(server, entryid, token):
    return _makeRequest(server, '/entries/'+str(entryid), 'GET', None, token)
 
def _entriesPost(server, token, entry):
    data={'entry': entry}
    return _makeRequest(server, '/entries/', 'POST', data, token)
 
def set_flag(host, port, flag):
    server=':'.join([host, port])
    username=hashlib.sha1(''.join(choice(string.ascii_letters + string.digits) for _ in range(20)).encode()).hexdigest()[:10]
    password=hashlib.sha1(''.join(choice(string.ascii_letters + string.digits) for _ in range(20)).encode()).hexdigest()[:10]
    _register(server, username, password)
    loginres=_login(server, username, password)
    token = loginres['token']
    entry = _entriesPost(server, token, flag)
    #flags[entry['hash']]=flag
    #print('*************** setted flag: '+flag)
    return {'flag_id': entry['id'], 'token': token}
 
def get_flag(host, port, flag_id, token):
    server=':'.join([host, port])
    #print('*************** gotten flag: '+flags[flag_id])
    entry = _getEntry(server, flag_id, token)
    return entry["entry"]
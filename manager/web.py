from flask import Flask, redirect
import flask_login
from helper import Account

accounts = dict()

app = Flask(__name__)

lookuptable = {
    'username': 0,
    'user_id': 1,
    'device_id': 3,
    'gdevice_id': 2,
    'interval': 4,
    'url': 5
}

def lookup(d, k):
    return d[lookuptable[k]]

with open('account.csv') as b:
    a = b.read().replace('\ufeff', '')
for i in a.split('\n'):
    if len(i) > 5:
        record = i.split(',')
        cur = lookup(record, 'user_id')
        tmp = dict()
        for k in lookuptable:
            tmp[k] = lookup(record, k)
        # print(tmp)
        accounts[cur] = Account(**tmp)

@app.route('/user/autostudy/<string:id>')
def setAutostudy(id):
    accounts[id].setAutostudy()
    return redirect('/user/%s' % id)

@app.route('/user/automove/<string:id>')
def setAutomove(id):
    accounts[id].setAutomove()
    return redirect('/user/%s' % id)

@app.route('/user/<string:id>')
def user(id):
    result = 'Auto Study: <a href="/user/autostudy/%s">' % id + \
        ('On' if accounts[id].autostudy else 'Off') + \
    '</a><br/>'

    result += 'Auto Move: <a href="/user/automove/%s">' % id + \
        ('On' if accounts[id].automove else 'Off') + \
    '</a><br/>'

    result += 'Target: %s <br/>' % accounts[id].aim

    result += str(accounts[id].status)
    result += "<br/><br/>"
    result += accounts[id].getLogs()
    return result

@app.route('/')
def index():
    web = ''
    for k in accounts:
        web += """
        <a href='/user/%s'>%s (Active: %s)</a>
        <br/>
        """ %(k, accounts[k].username,  'Y' if accounts[k].active else 'N')
    return web

app.run()

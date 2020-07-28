# uuid.uuid4().hex --> '8a0c1722b227489388497600ecf8dae9' // 32 chars

#######################################################
#    level    |               example                 #
# ------------| ------------------------------------- #
#1  CRITICAL  | logging.critical("erase database...") #
#2  ERROR     | logging.error("db is locked")         #
#3  WARNING   | logging.warning("detect launch dirb") #
#4  INFO      | logging.info("admin logout")          #
#5  DEBUG     | logging.debug(request.values())       #
# ----------- | ------------------------------------- #
#######################################################


from flask import Flask, request, render_template, redirect, url_for, flash
import logging as log
from tinydb import TinyDB, Query
from json import dumps as json_dumps
from uuid import uuid4

# killmeforthiscode ._. 
BAD_CHARS = ["'", '"', ';', '}', '{', '[', ']', ':', '%', '#', '<', '>']
#tmp_db = []
DB_PATH = 'db.json'
db = TinyDB(DB_PATH)
app = Flask(__name__)
app.secret_key = b'ChangeThisToken'
log.basicConfig(level=log.NOTSET, format='[%(levelname)s] %(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S', filename='notesApp_debug.log')

@app.route('/', methods=['GET', 'POST'])
def index():
    for i in request.form.values():
        for j in BAD_CHARS:
            if j in i:
                return redirect(url_for("nope"))
    if request.method == 'GET':
        if request.args.get('uuid'):
            __note_crypt_textarea = getNote(request.args.get('uuid'))
            if __note_crypt_textarea == None:
                return redirect(url_for("nope"))
            return render_template('text.html', crypt_textarea=__note_crypt_textarea, password=request.args.get('password'))
        #print(request.headers.get("Referer"))
        return render_template('index.html')
    if request.method == 'POST':
        if request.form.get("crypt_textarea") != '' and request.form.get("password") != '':
            __uuid, __password = create_note(request)
            if request.form.get("include_password") == 'on':
                flash(url_for('index', uuid=__uuid, password=__password, _external=True))
            else:
                flash('uuid: {}'.format(__uuid))
                flash('password: {}'.format(__password))
            return redirect(url_for('index'))
            #return redirect(f'/view/{request.form.get("uuid")}/{request.form.get("password")}')
        else:
            print(request.form)
            return "bad POST request"


def getNote(_uuid):
    try:
        __note = db.search(Query().uuid == _uuid)[0]
    except:
        return None
    if __note.get('need_delete') == 'on':
        db.remove(Query().uuid == _uuid)
    return __note.get('crypt_textarea')


def create_note(request):
    _request = request.form.to_dict()
    _request['uuid'] = uuid4().hex
    _password = _request.get('password')
    del(_request['password'])
    db.insert(_request)
    return _request.get('uuid'), _password

@app.route('/nope', methods=['GET', 'POST'])
def nope():
    '''
    _alert = dict(request.headers.values())
    _alert.update(dict(request.args.values()))
    #_args = [i for i in request.args.items()]
    #_headers.append(_args)
    #_alert = json_dumps(_headers, sort_keys=True)
    log.warning(_alert)
    #print(dir(request.headers))
    #print(request.headers.values())
    #print([i for i in request.headers.items()])
    '''
    return redirect(url_for("index"))


@app.route('/readme')
def readme():
    return render_template('README.html')


'''
for note in tmp_db:
        if note.uuid == uuid:
            if note.need_delete == False:
                log.info("read note")
                if note.password == password:
                    note.read = True
                    return render_template("view.html", note=note)
                else:
                    log.warning("incorrect password")
                    return redirect(url_for("index"))
            else:
                log.warning("attempted read deleted note")
                return redirect(url_for("index"))
        else:
            log.warning("incorrect uuid")
            return redirect(url_for("index"))
    return redirect(url_for("index"))
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    #app.run(debug=True, port=5001)

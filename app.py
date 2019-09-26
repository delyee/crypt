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


from flask import Flask, request, render_template, redirect, url_for
import logging as log
from tinydb import TinyDB, Query
from json import loads
from uuid import uuid4

tmp_db = []
DB_PATH = 'db.json'
db = TinyDB(DB_PATH)
app = Flask(__name__)
log.basicConfig(level=log.NOTSET, format='[%(levelname)s] %(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print(request.headers.get("Referer"))
        return render_template('index.html')
    if request.method == 'POST':
        if request.form.get("uuid") != '' and request.form.get("password") != '':
            return redirect(f'/view/{request.form.get("uuid")}/{request.form.get("password")}')
        else:
            return "bad POST request"

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')

    if request.method == 'POST':
        data = loads(request.data)
        print(data)

        db.insert({'uuid': uuid4().hex, 'enc_message': data.get('message') ,'hash_password': data.get('password')})
        return render_template('create_success.html', note=_, full_link=f"http://127.0.0.1:5000/view/{_.uuid}/{_.password}")
    else:
        return redirect(url_for('index'))


@app.route("/view/<string:uuid>/<string:password>")
def view(uuid, password):
    for note in tmp_db:
        if note.uuid == uuid:
            if note.read == False:
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
if __name__ == '__main__':
    app.run()

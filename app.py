from flask import Flask, request, render_template, redirect, url_for, flash
from string import ascii_letters, digits, punctuation
from json import loads as json_loads, dumps as json_dumps
from flask_redis import FlaskRedis
from random import choices
from loguru import logger
from uuid import uuid4
from config import *


app = Flask(__name__)
redis_client = FlaskRedis(app)
app.secret_key = ''.join(choices(ascii_letters + digits + punctuation, k=64))

logger.remove()
logger.add("crypt.log", format="{time} {message}", rotation="1 GB", compression="gz", enqueue=True)


@logger.catch
@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    for k, v in request.form.items():
        for bad_char in BAD_CHARS:
            if bad_char in k or bad_char in v:
                return redirect(url_for("nope"))

    # GET route
    if request.method == 'GET':
        if request.args.get('uuid'):
            __note_crypt_textarea = get_note(request.args.get('uuid'))
            if not __note_crypt_textarea:
                return redirect(url_for("nope"))
            else:
                return render_template('text.html', crypt_textarea=__note_crypt_textarea, password=request.args.get('password'))
        return render_template('index.html')

    # POST route
    if request.method == 'POST':
        if request.form.get("crypt_textarea", "") != "":
            __uuid = create_note(request)
            if request.form.get("include_password") == 'on':
                flash(url_for('index', uuid=__uuid, _external=True))
                # stats
                logger.info('Create quick note: {}'.format(__uuid))
            else:
                flash('uuid: {}'.format(__uuid))
                # stats
                logger.info('Create normal note: {}'.format(__uuid))
            return redirect(url_for('index'))
        else:
            print(request.form)
            return "bad POST request"

    # HEAD route
    if request.method == 'HEAD':
        return ''


@logger.catch
def get_note(_uuid):
    data = redis_client.get(_uuid)
    if not data:
        return None

    note = json_loads(data)

    if note.get('need_delete') == 'on':
        del redis_client[_uuid]
    return note.get('crypt_textarea')


@logger.catch
def create_note(request):
    _request = request.form.to_dict()
    _uuid = uuid4().hex
    _request['uuid'] = _uuid
    redis_client[_uuid] = json_dumps(_request)
    return _uuid


@logger.catch
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


@logger.catch
@app.route('/readme')
def readme():
    return render_template('README.html')


'''@app.route('/admin')
def readme():
    return render_template('admin.html')'''

# @app.route('/file/<uuid:uuid>')
'''@app.route('/file/<string:uuid>')
def file_download(uuid):
    # data:image/png;base64, iVBORw0KGgoAAAANSUhE
    _MimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    _MessageInBase64 = ''
    return redirect('data:{_MimeType};base64, {_MessageInBase64}'.format(_MimeType=_MimeType, _MessageInBase64=_MessageInBase64), code=302)
    # return redirect('data:{_MimeType};base64, {_MessageInBase64}'.format(_MimeType='image/png', _MessageInBase64='iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='), code=200)
'''


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
    app.run()
    #app.run(debug=True, port=5001)

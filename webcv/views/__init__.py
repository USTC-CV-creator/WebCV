from flask import (
    render_template, request, abort, jsonify,
    make_response, send_file, after_this_request
)
import urllib.parse
import re
import tempfile
import os
import subprocess
import functools

from .. import app, celery, config


def api(f):
    @functools.wraps(f)
    def g(*args, **kwargs):
        dct = f(*args, **kwargs)
        js = jsonify(dct)
        resp = make_response(js)
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'

        return resp
    g.is_api = True
    return g


@celery.task(name='pdf_gen')
def pdf_gen(html):
    fd, tmp_pdf = tempfile.mkstemp(suffix='.pdf', dir='./pdf_tmp/')
    os.close(fd)
    fd, tmp_html = tempfile.mkstemp(suffix='.html', dir='./pdf_tmp/')
    os.close(fd)
    with open(tmp_html, 'wt', encoding='utf8') as f:
        f.write(html)

    cmd = config['phantomjs']['cmd'] + [
        './pdf_conv/web2pdf.js',
        'file:///' + tmp_html,
        tmp_pdf,
    ]
    retcode = subprocess.call(cmd)
    if retcode == 0:
        os.remove(tmp_html)
        return {
            'status': 'success',
            'pdf': tmp_pdf,
        }
    else:
        os.remove(tmp_html)
        os.remove(tmp_pdf)
        return {
            'status': 'fail',
        }


@app.route('/cv/request_pdf', methods=['POST'])
@api
def cv_request_pdf():
    dct = request.json
    html = dct.get('html')
    if not html:
        abort(400)
    result = pdf_gen.apply_async((html,))
    return { 'task_id': result.task_id }


@app.route('/cv/task_status/<task_id>')
@api
def cv_task_status(task_id):
    res = pdf_gen.AsyncResult(task_id)
    if res.ready():
        ret = res.get()
        return { 'status': ret['status'] }
    else:
        return { 'status': 'wait' }


@app.route('/cv/get_pdf/<task_id>/<filename>.pdf')
def cv_get_pdf(task_id, filename):
    res = pdf_gen.AsyncResult(task_id)
    if res.ready():
        result = res.get()
        if result['status'] != 'success':
            abort(400)
        else:
            @after_this_request
            def remove_pdf(resp):
                try:
                    # BUG: does not work on windows
                    os.remove(result['pdf'])
                except:
                    pass
                finally:
                    return resp

            resp = send_file(result['pdf'], mimetype='application/pdf')
            # BUG: cross browser support
            # ref: http://stackoverflow.com/a/6745788
            resp.headers['Content-Disposition'] = (
                "attachment; filename*=UTF-8''"
                + urllib.parse.quote(filename + '.pdf'))

            return resp
    else:
        abort(400)


@app.route('/cv/<name>')
def cv_page(name):
    if not re.match('^[a-zA-Z0-9_-]+$', name):
        abort(404)
    from jinja2.exceptions import TemplateNotFound
    try:
        return render_template('cv/{}.html'.format(name))
    except TemplateNotFound:
        abort(404)


@app.route('/')
def index():
    return 'hello'

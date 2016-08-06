from flask import (
    render_template, request, abort, jsonify, url_for,
    make_response, send_file, after_this_request,
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
    fd, tmp_pdf = tempfile.mkstemp(suffix='.pdf', dir='./tmp/')
    os.close(fd)
    fd, tmp_html = tempfile.mkstemp(suffix='.html', dir='./tmp/')
    os.close(fd)
    with open(tmp_html, 'wt', encoding='utf8') as f:
        f.write(html)

    cmd = config['phantomjs']['cmd'] + [
        './scripts/web2pdf.js',
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

_png_gen_tasks = dict()

@celery.task(name='png_gen')
def png_gen(url, outfile):
    cmd = config['phantomjs']['cmd'] + [
        './scripts/web2png.js', url, outfile, '200',
    ]
    retcode = subprocess.call(cmd)
    return {
        'code': retcode,
        'file': outfile,
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
    # TODO: check for existence of task_id
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
            # BUG: need cross browser support
            # ref: http://stackoverflow.com/a/6745788
            resp.headers['Content-Disposition'] = (
                "attachment; filename*=UTF-8''"
                + urllib.parse.quote(filename + '.pdf'))

            return resp
    else:
        abort(400)


def check_cv_name(name):
    if not re.match('^[a-zA-Z0-9_-]+$', name):
        abort(404)
    if name.startswith('base_'):
        abort(404)


@app.route('/cv/templates/<name>')
def cv_page(name):
    check_cv_name(name)
    from jinja2.exceptions import TemplateNotFound
    try:
        return render_template('cv/{}.html'.format(name))
    except TemplateNotFound:
        abort(404)


@app.route('/cv/thumbnails/<name>.png')
def cv_thumbnail(name):
    check_cv_name(name)
    thumb_file = './tmp/{}.png'.format(name)
    thumb_file = os.path.abspath(thumb_file)    # send_file() must use absolute path
    template_file = '{}/{}/cv/{}.html'.format(app.root_path, app.template_folder, name)

    if not os.path.exists(template_file):
        print(template_file)
        abort(404)

    if os.path.exists(thumb_file):
        if os.path.getmtime(thumb_file) < os.path.getmtime(template_file):
            need_update = True
        else:
            need_update = False
    else:
        need_update = True

    if name in _png_gen_tasks and not _png_gen_tasks[name].ready():
        need_update = False

    if need_update:
        url = url_for('cv_page', name=name, _external=True)
        result = png_gen.apply_async((url, thumb_file))
        _png_gen_tasks[name] = png_gen.AsyncResult(result.task_id)

    if os.path.exists(thumb_file):
        return send_file(thumb_file)
    else:
        abort(404)


@app.route('/')
def index():
    pages = [ page for page in config['cv_pages'].values() if page['enabled'] ]
    return render_template('index.html', pages=pages)

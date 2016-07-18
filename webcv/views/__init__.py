from .. import app
from flask import render_template


@app.route('/cv/<name>')
def cv_page(name):
    # TODO: check input
    return render_template('cv/{}.html'.format(name))


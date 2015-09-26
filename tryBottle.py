__author__ = 'al'

from bottle import Bottle, route, run
from bottle import template


@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

run(host='localhost', port=8080, debug=True)
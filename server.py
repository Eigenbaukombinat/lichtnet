import logging
from flask import Flask, render_template
import dmxmodel

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


log = logging.getLogger('DMXWeb')


controller = dmxmodel.Controller()

controller.add_fixture('RGB1', 'rgb', 0, '192.168.21.118')
controller.add_fixture('RGB2', 'rgb', 4, '192.168.21.118')
controller.add_fixture('RGB3', 'rgb', 8, '192.168.21.118')

fixtures = {'r1': controller.get_fixture('RGB1'),
    'r2': controller.get_fixture('RGB2'),
    'r3': controller.get_fixture('RGB3')}

app = Flask(__name__)

app.wsgi_app = ReverseProxied(app.wsgi_app)


@app.route('/')
def mainpage():
    return render_template('index.html')

@app.route('/jquery.js')
def jquery():
    return render_template('jquery-3.1.1.min.js')

@app.route('/color.js')
def colorjs():
    return render_template('jqColorPicker.min.js')

@app.route('/index.css')
def css():
    return render_template('index.css')


def hex_to_int(h):
    return (int(h[0:2], 16),
        int(h[2:4], 16),
        int(h[4:6], 16))

@app.route('/color/<fixture>/<color>/<brightness>')
def color(fixture, color, brightness):
    fix = fixtures[fixture]
    fix.set_color(*hex_to_int(color))
    fix.set_main_brightness(int(brightness))
    controller.send_update()
    return 'OK'


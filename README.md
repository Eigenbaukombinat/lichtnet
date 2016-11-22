# lichtnet

Simple flask web app to set colors of artnet nodes.

To install/run:

```
virtualenv .
bin/pip install flask
FLASK_APP=server.py bin/flask run --host=0.0.0.0 --port=8080
```

Point your browser on your configured address and select some fancy colors.

To configure available light fixtures, you have to edit server.py for now.

I'll add configuration via .ini later.

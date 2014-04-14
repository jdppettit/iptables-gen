from flask import *

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello World!"

@app.route('/poop')
def poop():
	return "Poop page!"

@app.route('/template/')
@app.route('/template/<name>')
def template(name=None):
	return render_template('template.html',name=name)

with app.test_request_context():
	url_for('static', filename='style.css')

if __name__ == '__main__':
	app.run(host='0.0.0.0')

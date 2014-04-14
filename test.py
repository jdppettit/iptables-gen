from flask import *

app = Flask(__name__)

@app.route('/')
def index(rule=None):
	return render_template('index.html',rule=rule)

@app.route('/make-rule', methods=['POST'])
def make_rule():
	if request.method == 'POST':
		string = "You selected %s" % request.form['acceptdeny']
		return render_template('index.html',rule=string)
	else:
		return "You did something wrong"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

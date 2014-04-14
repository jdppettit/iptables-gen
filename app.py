from flask import *

app = Flask(__name__)

@app.route('/')
def index(rule=None):
	return render_template('index.html',rule=rule)

@app.route('/make-rule', methods=['POST'])
def make_rule():
	ruleString = ""
	try:
		if request.method == 'POST':
			
			try:
				if request.form['appendinsert'] == "append":
					ruleString += "iptables -A "
				else:
					ruleString += "iptables -I "
			except Exception ,e:
				print e

			try:
				if request.form['inputoutputforward'] == 'input':
					ruleString += "INPUT "
				elif request.form['inputoutputforward'] == 'output':
					ruleString += "OUTPUT "
				else: 
					ruleString += "FORWARD "
			except Exception, e:
				print e

			try:
				if request.form['appendinsert'] == "insert":
					ruleString += str(request.form['insertpos'])
					ruleString += " "
			except Exception, e:
				print e

			try:		
				if request.form['prototcp'] == "tcp" and request.form['protoudp'] == "udp":
					ruleString += "-p tcp,udp "
				elif request.form['prototcp'] == "tcp" and request.form['protoudp'] != "udp":
					ruleString += "-p tcp "
				elif request.form['prototcp'] != "tcp" and request.form['protoudp'] == "udp":
					ruleString += "-p udp "
			except Exception, e:
				print e

			try:
				if request.form['sourceip']:
					if request.form['sourceiptext']:
						ruleString += "-s %s " % str(request.form['sourceiptext'])
			except Exception, e:
				print e
			
			try:			
				if request.form['destip'] == "destip":
					if request.form.has_key['destiptext']:
						ruleString += "-o %s " % str(request.form['destiptext'])
			except Exception, e:
				print e

			try:
				if request.form['dport'] == "dport":
					if request.form.has_key['dporttext']:
						ruleString += "--dport %s " % str(request.form['dporttext'])
			except Exception, e:
				print e

			try:
				if request.form['sport'] == "sport":
					if request.form.has_key['sporttext']:
						ruleString += "--sport %s " % str(request.form['sporttext'])	
			except Exception, e:
				print e

			try:
				if request.form['new'] == "new" or request.form['established'] == "established" or request.form['related'] == "related":
					numStates = 0
					ruleString += "-m state --state "
			
					if request.form['new'] == "new":
						numStates += 1
					
					if request.form['established'] == "established":
						numStates += 1
					
					if request.form['related'] == "related":
						numStates += 1
					 
					if numStates == 3:
						numStates = 2

					if request.form['new'] == "new" and numStates > 0:
						numStates -= 1
						ruleString += "NEW,"
					else:
						ruleString += "NEW "
	
					if request.form['established'] == "established" and numStates > 0:
						numStates -= 1
						ruleString += "ESTABLISHED,"
					else:
						ruleString += "ESTABLISHED "

					if request.form['related'] == "related" and numStates > 0:
						numStates -= 1
						ruleString += "RELATED,"
					else:
						ruleString += "RELATED "
			except Exception, e:
				print e

			if request.form['acceptdeny'] == "accept":
				ruleString += "-j ACCEPT"
			elif request.form['acceptdeny'] == "deny":
				ruleString += "-j DROP"

			return render_template('index.html',rule=ruleString)
	
	except Exception, e:
		print e		
		print request.form
		return render_template('index.html',rule=ruleString)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

from flask import *

app = Flask(__name__)

@app.route('/')
def index(rule=None):
	return render_template('index.html',rule=rule)

@app.route('/make-rule', methods=['POST'])
def make_rule():
	ruleString = ""
	errorFlag = 0
	try:
		if request.method == 'POST':
			
			try:
				if request.form['appendinsert'] == "append":
					ruleString += "iptables -A "
				else:
					ruleString += "iptables -I "
			except Exception ,e:
				print e
				errorFlag = 1

			try:
				if request.form['inputoutputforward'] == 'input':
					ruleString += "INPUT "
				elif request.form['inputoutputforward'] == 'output':
					ruleString += "OUTPUT "
				else: 
					ruleString += "FORWARD "
			except Exception, e:
				print e
				errorFlag = 1

			try:
				if request.form['appendinsert'] == "insert":
					ruleString += str(request.form['insertpos'])
					ruleString += " "
					if not request.form['insertpos']:
						errorFlag = 1
						print "Error flag thrown"
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
					if not request.form['sourceiptext']:
						errorFlag = 1
			except Exception, e:
				print e
			
			try:			
				if request.form['destip'] == "destip":
					if request.form['destiptext']:
						ruleString += "-o %s " % str(request.form['destiptext'])
					if not request.form['destiptext']:
						errorFlag = 1
			except Exception, e:
				print e

			try:
				if request.form['dport'] == "dport":
					if request.form['dporttext']:
						ruleString += "--dport %s " % str(request.form['dporttext'])
					if not request.form['dporttext']:
						errorFlag = 1
			except Exception, e:
				print e

			try:
				if request.form['sport'] == "sport":
					if request.form['sporttext']:
						ruleString += "--sport %s " % str(request.form['sporttext'])	
					if not request.form['sporttext']:
						errorFlag = 1
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
			
			if errorFlag != 0:
				print "The IF statement evaluated as TRUE"
				ruleString += "*** THIS RULE IS NOT VALID *** Please make sure you entered information in the text field next to each option you checked!"
			
			return render_template('index.html',rule=ruleString)
	
	except Exception, e:
		print e		
		print request.form
		
		if errorFlag == 1:
	                ruleString += "*** THIS RULE IS NOT VALID *** Please make sure you entered information in the text field next to each option you checked!"

		return render_template('index.html',rule=ruleString)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

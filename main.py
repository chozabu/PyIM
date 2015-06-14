import sys  
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import QVariant, QTimer
import xmpp
	
"""Html snippet."""  
html = """ 
<html><body> 
	<center> 
	<script language="JavaScript"> 
	document.write('<p>Python ' + pyObj.pyVersion + '</p>') 
	</script> 
	<input name="login" type="text" maxlength="512" id="login" class="login"/>
	<input name="pass" type="text" maxlength="512" id="pass" class="pass"/>
	<button onClick="pyObj.uplink(login.value, pass.value)">Login</button> 
	<button onClick="getRoster()">contacts</button> 
	<div id="contacts">
	</div>
	<select name="clist" id="clist">
	</select>
	<input name="intext" type="intext" maxlength="512" id="intext" class="intext"/>
	<div id="output">
	</div>
	<script>
	login = document.getElementById('login')
	pass = document.getElementById('pass')
	contacts = document.getElementById("contacts")
	clist = document.getElementById("clist")
	output = document.getElementById("output")
	intext = document.getElementById("intext")
	login.value="username"
	pass.value="password"
	function addchat(author, text){
		output.innerHTML+="<br>";
		output.innerHTML+=author;
		output.innerHTML+=": ";
		output.innerHTML+=text;
	}
	function sendMessage(){
		pyObj.printit(clist.value);
		pyObj.printit(intext.value);
		pyObj.sendMessage(clist.value, intext.value);
		addchat("me", intext.value);
	}
	function getRoster(){
		pyObj.printit("grc")
		var roster = pyObj.getRoster()
		//contacts.innerHTML = roster;
		pyObj.printit("grc2")
		pyObj.printit(roster[0])
		pyObj.printit("grc2a")
		pyObj.printit(roster[1])
		pyObj.printit("grc3")
		for (var i = 0; i < roster.length; i++) {
			var option = document.createElement("option");
			option.value = roster[i];
			option.text = roster[i];
			clist.appendChild(option);
		}
		
		//contacts.innerHTML
	}
	</script>
	<button onClick="sendMessage()">Send</button> 
	<button onClick="pyObj.showMessage('Hello from WebKit')">Press me</button> 
	</center> 
</body></html> 
"""  
	
class StupidClass(QtCore.QObject):  
	"""Simple class with one slot and one read-only property."""  
	
	def minit(self):
		timer = QTimer()
		# Connect it to ml
		timer.timeout.connect(self.ml)
		# Call f() every 2 seconds
		timer.start(2000)
		self.t = timer
		print "usndfsndffdn"
		#self.minit("asdadnj")
	def ml(self):
		#self.mainframe.evaluateJavaScript("addchat('asd','qwe');")
		#self.mainframe.evaluateJavaScript("alert('asdqwe');")
		try:
			self.client.Process(1)
		except:
			print "passsed"
	
	@QtCore.pyqtSlot(str)  
	def showMessage(self, msg):  
		"""Open a message box and display the specified message."""  
		QtGui.QMessageBox.information(None, "Info", msg)  
	
	def _pyVersion(self):  
		"""Return the Python version."""  
		return sys.version  
	@QtCore.pyqtSlot(str, str)  
	def uplink(self, username, passwd):
		print username, passwd
		client = xmpp.Client('gmail.com')
		client.connect(server=('talk.google.com',5223))
		client.auth(username, passwd, 'botty')
		client.RegisterHandler('message', self.gotmsg)
		#client.RegisterHandler('chat', self.gotmsg)
		client.sendInitPresence()
		self.client = client
	def gotmsg(self,sess,mess):
		print 'MESSAGE'*10
		print "MESS", mess
		nick=mess.getFrom()
		print "NICK", nick
		text=mess.getBody()
		print "TEXT", text
		print "DATA", mess.getData()
		print "DATA", mess.getType()
		print "DATA", mess.getPayload()
		print "DATA", mess.getSubject()
		print "DATA", mess.getAttrs()
		print "DATA", mess.getCDATA()
		print "DATA", mess.getChildren()
		print "DATA", mess.getParent()
		print dir(mess)
		try:
			self.mainframe.evaluateJavaScript("addchat('asd','qwe');")
			self.mainframe.evaluateJavaScript("addchat('"+"123"+"','"+"123"+"');")
			self.mainframe.evaluateJavaScript("addchat('"+nick+"','"+"notext"+"');")
			self.mainframe.evaluateJavaScript("addchat('"+nick+"','"+text+"');")
		except:
			pass
	@QtCore.pyqtSlot(str, str)  
	def sendMessage(self, to, message):
		to=str(to)
		message=str(message)
		print "sending: ", message, " to ", to
		message = xmpp.Message(to, message)
		message.setAttr('type', 'chat')
		self.client.send(message)
		
	@QtCore.pyqtSlot(result=QVariant)  
	def getRoster(self):
		print "getting roster"
		roster =  self.client.getRoster()
		#for r in roster.keys():
		#	print r
		#	print roster[r]
		#	#print roster[r]['status']
		rkeys = [str(r) for r in roster.keys()]
		print "rkclass", rkeys.__class__.__name__
		print "rkclass", rkeys[0].__class__.__name__
		return QVariant(rkeys)
		
	@QtCore.pyqtSlot(str)  
	def printit(self, out):
		print out
	
	"""Python interpreter version property."""  
	pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)  
	
def main():  
	app = QtGui.QApplication(sys.argv)  
	
	myObj = StupidClass()  
	myObj.minit()
	
	webView = QtWebKit.QWebView()  
	# Make myObj exposed as JavaScript object named 'pyObj'  
	webView.page().mainFrame().addToJavaScriptWindowObject("pyObj", myObj)  
	myObj.mainframe=webView.page().mainFrame()
	webView.setHtml(html)  
	
	window = QtGui.QMainWindow()  
	window.setCentralWidget(webView)  
	window.show()  
	
	sys.exit(app.exec_())  
	
if __name__ == "__main__":  
	main()  
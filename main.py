import sys  
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtCore import QVariant, QTimer
import xmpp
from PyQt4.QtWebKit import QWebSettings
	
	
"""Html snippet."""  
html = """ 
<html><body> 
	<center> 
	<script language="JavaScript"> 
	//document.write('<p>Python ' + pyObj.pyVersion + '</p>') 
	
	</script> 


	<div id="contacts">
	</div>
	<select name="clist" id="clist">
	</select>
	<input name="intext" type="intext" maxlength="512" id="intext" class="intext"/>
	<div id="output">
	</div>
	<script>



	contacts = document.getElementById("contacts")
	clist = document.getElementById("clist")
	output = document.getElementById("output")
	intext = document.getElementById("intext")

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
		loadRoster(roster);
	}
	function loadRoster(roster){
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
	setInterval(getRoster,800);
		
		//contacts.innerHTML
	}
	</script>
	<button onClick="sendMessage()">Send</button> 
	<button onClick="pyObj.showMessage('Hello from WebKit')">Press me</button> 
	</center> 
</body></html> 
"""  
	
class QtJsBridge(QtCore.QObject):  
	"""connection between QT and Webkit."""  
	
	def minit(self):
		timer = QTimer()
		timer.timeout.connect(self.pTick)
		timer.start(1000)
		self.t = timer
	def pTick(self):
		#self.mainframe.evaluateJavaScript("addchat('asd','qwe');")
		try:
			self.client.Process(1)
		except:
			print "unable to process incoming data(disconnected?)"
	
	@QtCore.pyqtSlot(str)  
	def showMessage(self, msg):  
		"""Open a message box and display the specified message."""  
		QtGui.QMessageBox.information(None, "Info", msg)  
	
	def _pyVersion(self):  
		"""Return the Python version."""  
		return sys.version  
	@QtCore.pyqtSlot()  
	def uplinkButton(self):#unused
		self.mainframe.evaluateJavaScript("")
		pass
		
	def gotmsg(self,sess,mess):
		print 'MESSAGE'*3
		print "MESS", mess
		nick=str(mess.getFrom())
		print "NICK", nick
		text=str(mess.getBody())
		print text.__class__.__name__
		if text == None or text == "None":
			print "blank message, ignoring"
			return
		print "TEXT", text
		#print dir(mess)
		try:
			self.mainframe.evaluateJavaScript("addchat('"+nick+"','"+text+"');")
		except:
			print "could not issue message"
		#try:
		#	self.mainframe.evaluateJavaScript("alert('"+text+"');")
		#except:
		#	print "could not issue alert"
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
		
		#for r in roster.keys():
		#	print r
		#	print roster[r]
		#	#print roster[r]['status']
		
		#print "rkclass", rkeys.__class__.__name__
		#print "rkclass", rkeys[0].__class__.__name__
		return QVariant(self.rkeys)
		
	@QtCore.pyqtSlot(str)  
	def printit(self, out):
		print out
	
	"""Python interpreter version property."""  
	pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)  
	
def main():  
	
	


	app = QtGui.QApplication(sys.argv)  
	QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True);
	
	myObj = QtJsBridge()  
	myObj.minit()
	
	webView = QtWebKit.QWebView()  
	# Make myObj exposed as JavaScript object named 'pyObj'  
	webView.page().mainFrame().addToJavaScriptWindowObject("pyObj", myObj)  
	myObj.mainframe=webView.page().mainFrame()
	webView.setHtml(html)  
	
	window = QtGui.QMainWindow()  
	window.setCentralWidget(webView)  
	window.show()  
	
	server = 'talk.google.com'
	login2 = 'gmail.com'
	port = '5223'
	username = 'luke.stanley'
	passwd = 'tsushkwpcsqnntia'
	print username, passwd
	print login2
	print server
	print port
	client = xmpp.Client(login2)
	client.connect(server=(server,int(port)))
	client.auth(username, passwd, 'botty')
	
	
	client.RegisterHandler('message', myObj.gotmsg)
	#client.RegisterHandler('chat', self.gotmsg)
	client.sendInitPresence()
	#self.client = client
	myObj.client = client
	roster =  client.getRoster()
	QTimer.singleShot(1000, client.getRoster)
	myObj.rkeys = [str(r) for r in roster.keys()]
	
	sys.exit(app.exec_())  
	
if __name__ == "__main__":  
	main()  

#!/usr/bin/env python

## Syslog Server in Python.
##

HOST, PORT = "0.0.0.0", 514

OracleUser = ''
OraclePasswd = ''
OracleServerSid = "localhost/orclpdb1"
#
import sys
import cx_Oracle
import socketserver
import json
import threading

connection = cx_Oracle.connect(OracleUser, OraclePasswd, OracleServerSid, threaded = True)
cursor = connection.cursor()

def insert_logging(IP,PRIO,STAMP,HOST,APP,PID,MESS):
	"""
	Insert a row to the SYSLOG table
	:param IP:
	:param APP:
	:param STAMP:
	:param HOST:
	:param PID:
	:param PRIO:
	:param MESS:
	:return:
	"""
    # construct an insert statement that add a new row to the billing_headers table
	sql = ('insert into SYSLOG(REMOTEIP,APPNAME,ZEIT,HOSTNAME,PID,PRIORITY,MESSAGE) values (:IP,:APP,:STAMP,:HOST,:PID,:PRIO,:MESS)')
	try:
		cursor.execute(sql, [IP, APP, STAMP, HOST, PRIO, PID, MESS])
		connection.commit()
	except cx_Oracle.Error as error:
		print('Error occurred:')
		print(error)


class SyslogUDPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		fields = json.loads(str(data))
		insert_logging("%s" % self.client_address[0],fields["PRIO"].strip(),fields["TIME"],fields["HOST"],fields["APP"],fields["PID"].strip(),fields["MSG"])
		print("Recieved one request from {}".format(self.client_address[0]))
		print("Thread Name:{}".format(threading.current_thread().name))



if __name__ == "__main__":
	try:
		server = socketserver.ThreadingUDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever()
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")

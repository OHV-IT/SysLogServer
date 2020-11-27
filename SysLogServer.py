#!/usr/bin/env python

## Syslog Server in Python.
##

HOST, PORT = "0.0.0.0", 514

OracleUser = ''
OraclePasswd = ''
OracleServerSid = "localhost/orclpdb1"

#
# NO USER SERVICEABLE PARTS BELOW HERE...
#
import sys
import cx_Oracle
import config
import SocketServer
import json

connection = cx_Oracle.connect(OracleUser, OraclePasswd, OracleServerSid)

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
    sql = ('insert into SYSLOG(REMOTEIP,APPNAME,ZEIT,HOSTNAME,PID,PRIORITY,MESSAGE) '
        'values(:IP,:APP,:STAMP,:HOST,:PID,:PRIO,:MESS)')

    try:
        cursor.execute(sql, [IP, APP, STAMP, HOST, PRIO, PID, MESS])
        connection.commit()
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)


class SyslogUDPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		data = bytes.decode(self.request[0].strip())
		socket = self.request[1]
		print( "%s : " % self.client_address[0], str(data))
		fields = json.loads(str(data))
		insert_logging("%s" % self.client_address[0],fields["PRIO"].strip(),fields["TIME"],fields["HOST"],fields["APP"],fields["PID"].strip(),fields["MSG"])


if __name__ == "__main__":
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")

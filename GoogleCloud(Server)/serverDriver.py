import time
import sys
import glob
from predictor import Predictor
from socket import *
from rfidCloud import readCloud
import boto3
from botocore.exceptions import ClientError
import os

serverPort=12010
RFIDflag=0
pre = None

class server:
	def __init__(self):
		global serverPort
		self.serverName="172.30.142.222"
		self.serverSocket = socket(AF_INET,SOCK_STREAM)
		self.serverSocket.bind((self.serverName,serverPort))
		self.serverSocket.listen(1)
	


	def recvRFIDdata(self):
		print("Ready to receive RFID data : ")
		self.connSocket1,self.addr1 = self.serverSocket.accept()
		self.RFIDdata = self.connSocket1.recv(1024).decode()
		print("RFID  Data Rcvd : ",self.RFIDdata)
		id = self.RFIDdata[:13]
		text = self.RFIDdata[13:]
		print("ID : ",id)
		print("text : ",text)
		if len(text)==0:
			text="0" 
		self.rfidObj = readCloud(id,text)
		sentMail = self.rfidObj.send_email()
		self.connSocket1.send((str(sentMail)).encode())
		print("Sent Mail Status : ",sentMail)
		global RFIDflag
		RFIDflag =  sentMail

	def recvFrame(self):
		self.connSocket,self.addr = self.serverSocket.accept()
		self.flag = self.connSocket.recv(1024).decode()
		if self.flag=="true":
			os.system("./normal.sh")
		self.sendRecvdCmd()

	def sendRecvdCmd(self):
		global serverPort
		global pre
		global RFIDflag
		self.predictObj = Predictor()
		self.prediction = self.predictObj.predictFace()
		self.connSocket.send(("recvd:"+str(self.prediction)).encode())
		if self.prediction!=None and self.prediction!=13:
			pre=self.prediction
			RFIDflag=0
		self.deleteFrame()

	def deleteFrame(self):
		imagepaths = glob.glob("*.jpg")
		for image in imagepaths:
			os.remove(image)

def main():
	global serverPort
	while True:
		obj = server()

		if RFIDflag==1:
			obj.recvFrame()
		if RFIDflag==0:
			obj.recvRFIDdata()

		serverPort = serverPort + 1
		time.sleep(4)

main()

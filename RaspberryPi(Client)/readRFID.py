import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class RFID:
    def __init__(self):
        self.reader = SimpleMFRC522()
    def read(self):
        try:
                id, text = self.reader.read()
                count=0
                for i in text:
                    print("#"+i,end="")
        finally:
                pass
        
        return [id,text]
    
    



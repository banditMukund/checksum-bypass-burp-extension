

from burp import IBurpExtender
from burp import IHttpListener
import subprocess
import json
import sys
from base64 import b64decode, b64encode


class BurpExtender(IBurpExtender, IHttpListener):


    def encryption(self, p_data):
       
        print("encryption function")
        print("body in encryption function=",p_data.decode())
        data = subprocess.check_output(["python3", "<path to encrytion.py folder>/encryption.py", p_data.decode('utf-8')])

       
        print("hmac received from encryption file = ", data)

        return str(data)

    
    def registerExtenderCallbacks(self, callbacks):
        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("Encryption")
        
        callbacks.registerHttpListener(self)

    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            return


        requestBytes = messageInfo.getRequest()
        requestInfo = self._helpers.analyzeRequest(requestBytes)
        
        headers = requestInfo.getHeaders()
      
        bodyBytes = requestBytes[requestInfo.getBodyOffset():]

        if bodyBytes:
            bodyJson = self._helpers.bytesToString(bodyBytes)
            print("body in main=", bodyJson)
            print("headers = ", headers)
            try:
                
          
                newhmac = self.encryption(bodyJson)
                print("newhmac=",newhmac)
                newheader = "X-Auth: "+newhmac
                print("newheader=",newheader)
                indposition=0
                for i in range(len(headers)):
                    if('X-Auth' in headers[i]):
                        indposition=i
                headers[indposition] = newheader[:-1]
                print("modified headers = ", headers)
              
            except Exception as e:
                print(e)

      
        modifiedMessage = self._helpers.buildHttpMessage(headers, bodyBytes)

        messageInfo.setRequest(modifiedMessage)

        return

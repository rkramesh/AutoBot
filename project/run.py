import sys
sys.path.append("..")
from cred import *
from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
#from yowsup.env import YowsupEnv
import logging
logging.basicConfig(level=logging.DEBUG)

credentials = (phone, pw) # replace with your phone and password
#CREDENTIALS = DemosArgParser._getCredentials()

if __name__==  "__main__":
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
    stack.loop() #this is the program mainloop

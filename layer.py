from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity, \
    ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import ChatstateProtocolEntity, OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from PIL import Image
import time
import os
import random
import wikipedia


class EchoLayer(YowInterfaceLayer):

    def normalizeJid(self, number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number
    
    def doSendImage(self,filePath,url,to,ip=None):
      entity=ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath,url,ip,to)
      self.toLower(entity)


    ##

    def onRequestUploadResult(self, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, jid, path, oup):
        print("Request ok")
        #duplicate image will provide json data not found Exception error
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendImage(path,resultRequestUploadIqProtocolEntity.getUrl(),jid,resultRequestUploadIqProtocolEntity.getIp())
            mediaUploader = MediaUploader(jid, self.getOwnJid(), path,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, oup)
            print("Duplicate Image found....")
        else:
             #successFn = lambda filePath, jid, url: self.uploadOk(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
             mediaUploader = MediaUploader(jid, self.getOwnJid(), path,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, oup)
        mediaUploader.start()
        print("Request ok upload complete")

    def onRequestUploadError(self, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        print("Error requesting upload url")

    def onUploadSuccess(self, filePath, jid, url):
        # convenience method to detect file/image attributes for sending, requires existence of 'pillow' library
        print("Upload success")
        entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, jid)
        self.toLower(entity)
	entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, jid)
        self.toLower(entity)
		

    def onUploadError(self, filePath, jid, url):
        print("Upload file failed!")
        print(ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        print("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        print("Upload on  progress")
        
  ##
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        
    #send receipt otherwise we keep receiving the same message over and over
        
     if messageProtocolEntity.getType() == 'text':
        #self.onTextMessage(messageProtocolEntity)
         
        msgFrom = messageProtocolEntity.getFrom()
        msgText = messageProtocolEntity.getBody()
        msgType = messageProtocolEntity.getType()
	jid = self.normalizeJid(msgFrom)
        
    

        if True:
                        
            if 'Hi' in msgText:
                print 'hii from rk'
		outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Newbie' + " " +
                                                                            msgText,   
                                                                            to = msgFrom)
		self.toLower(outgoingMessageProtocolEntity)
	    elif 'Rk' in msgText:
		jid = self.normalizeJid(msgFrom)
		entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, jid)
                self.toLower(entity)
                print 'Hello Boss'
                #img = Image.open('rk.jpg')
                #img.show()
                #os.system("start C:\Windows\system32\cmd")
		outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Hello Boss' + "  " +
                                                                       msgText,
                                                                       to = msgFrom)
		self.toLower(outgoingMessageProtocolEntity)
	    elif 'cool' in msgText or 'Cool' in msgText :
                #Generating random Img from Folder 
                jid = self.normalizeJid(msgFrom)
                filec =  r"C:\Users\radhakrishnanr\Desktop\img"
                random_filename = random.choice([
                    x for x in os.listdir(filec)
                    if os.path.isfile(os.path.join(filec, x))
                ])
                
                path = 'C:/Users/radhakrishnanr/Desktop/img/'+random_filename
                iqEntity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE,
                                                     filePath=path)
                uploadOk = lambda successEntity, originalEntity: \
                   self.onRequestUploadResult(successEntity, originalEntity, jid, path, self.onUploadProgress)
                self._sendIq(iqEntity, uploadOk, self.onRequestUploadError)
                

                
            else:
                  print 'python message'
                  outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'send from python' + "  " +
                                                                       msgText,
                                                                       to = msgFrom)
                  self.toLower(outgoingMessageProtocolEntity)
                 

                 
        print("Message:%s|From:%s|Time:%s|" % (messageProtocolEntity.getBody(),
                                               messageProtocolEntity.getFrom(False),
                                               time.ctime()))
        
     elif messageProtocolEntity.getType() == 'media': 
        print "Media received"
        outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Media Not Suppported' + " " +
                                                                       time.ctime(),
                                                                       to = messageProtocolEntity.getFrom())
        self.toLower(outgoingMessageProtocolEntity)


     
     
     #send delivery receipt with time
     self.toLower(messageProtocolEntity.ack(True))
 
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt",entity.getType(), entity.getFrom())
        self.toLower(ack)
        
 

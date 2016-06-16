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
import sys
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
        #convenience method to detect file/image attributes for sending, requires existence of 'pillow' library
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
        msgText = messageProtocolEntity.getBody().lower()
        msgType = messageProtocolEntity.getType()
	jid = self.normalizeJid(msgFrom)
	textMsg = ' '
	modwiki = ' '
        if True:
            #msgText = msgText.encode('utf8')           
            if msgText == 'hi':
                print 'Hii from rk'
                #textMsg = ' '
                modwiki = 'Hii..Im Whatsapp Bot..Try me..'
                
	    elif msgText == 'rk':
		jid = self.normalizeJid(msgFrom)
		entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, jid)
                self.toLower(entity)
                print 'Hello Boss'
                #img = Image.open('rk.jpg')
                #img.show()
                #os.system("start C:\Windows\system32\cmd")
                textMsg = 'Hello Boss.. :)'
	    elif msgText == 'wiki':
                textMsg = 'Wiki Details:'
                modwiki = 'Add a word after wiki to get details.Eg: wiki eagle'                
	    elif 'wiki' in msgText:
                textMsg = 'Wiki Details:'
                #wikipedia.set_lang('ta')
                splitted = msgText.split()
                if splitted[1] == 'set-lang':         
                    try:
                        wikipedia.set_lang(splitted[2])
                        modwiki = 'Wiki language Changed to '+ splitted[2]
                    except:
                        modwiki = 'Unable to Set Language'
                elif splitted[1] == ' ':
                    modwiki ='Add a word after wiki to get details.Ex: wiki cool'
                     
		elif splitted[1] != 'set-lang':
		    #modwiki = wikipedia.summary(msgText.split(' ',1)[1]).encode('utf-8')#encoding to avoid unicode error
                    jid = self.normalizeJid(msgFrom)
                    entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, jid)
                    self.toLower(entity)
                    
                    print 'This is Wiki App'
                    try:
                        modwiki = wikipedia.summary(msgText.split(' ',1)[1]).encode('utf-8')#encoding to avoid unicode error
                    except ValueError:
                        modwiki = 'Sorry value erroe Page not Found!..Please try with different search term'
                    except wikipedia.exceptions.PageError:
                        modwiki = 'Sorry Page not Found!..Please try with different search term'
                    except wikipedia.exceptions.DisambiguationError as e:
                        # print (e.options)# this will print
                        modwiki = ', '.join(e.options)
                    except:
                        modwiki = 'Unknown Error Check with Rk'
                else:
                    modwiki ='Add a word after wiki to get details.Ex: wiki cool'
                
	    elif msgText == 'kabali':
                #Generating random Img from Folder 
                #jid = self.normalizeJid(msgFrom)
                filec =  r"C:\Users\radhakrishnanr\Desktop\kabali"
                random_filename = random.choice([
                    x for x in os.listdir(filec)
                    if os.path.isfile(os.path.join(filec, x))
                ])
                
                path = 'C:/Users/radhakrishnanr/Desktop/kabali/'+random_filename
                textMsg = 'Uploading kabali Image....'
                iqEntity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE,
                                                     filePath=path)
                uploadOk = lambda successEntity, originalEntity: \
                   self.onRequestUploadResult(successEntity, originalEntity, jid, path, self.onUploadProgress)
                self._sendIq(iqEntity, uploadOk, self.onRequestUploadError)
                

               
            else:
                  
                  print 'python message'
                  textMsg = 'Auto Reply:'+messageProtocolEntity.getBody()
                  msgFrom = '91999990099999999999900900'#disable Auto Reply

            
                  
                  
                  
            outgoingMessageProtocolEntity = TextMessageProtocolEntity( textMsg + " " +
                                                                            modwiki,   
                                                                            to = msgFrom)
	    self.toLower(outgoingMessageProtocolEntity)
                     

                 
        print("Message:%s|From:%s|Time:%s|" % (msgText,
                                               messageProtocolEntity.getFrom(False),
                                               time.ctime()))

        
       
        
     elif messageProtocolEntity.getType() == 'media': 
        print "Media received"
        try:
            
            outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Media Not Suppported' + " " +
                                                                       time.ctime(),
                                                                       to = messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)
        except ValueError:
            print 'audio not supported'
        '''
     elif message.getMediaType() == 'ptt': 
        print "Audio received"
        outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Audio Not Suppported' + " " +
                                                                       time.ctime(),
                                                                       to = messageProtocolEntity.getFrom())
        self.toLower(outgoingMessageProtocolEntity)
        '''

        
     elif messageProtocolEntity.getType() == 'vcard': 
        print "vcard received"
        outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'vcard Not Suppported' + " " +
                                                                       time.ctime(),
                                                                       to = messageProtocolEntity.getFrom())
        self.toLower(outgoingMessageProtocolEntity)

            


     
     
     #send delivery receipt with time
     self.toLower(messageProtocolEntity.ack(True))
     
     
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt",entity.getType(), entity.getFrom())
        self.toLower(ack)
        
 

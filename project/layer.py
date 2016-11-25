from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity, \
    ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import ChatstateProtocolEntity, OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from dlink import downloadlink 
from PIL import Image
import time
import os
import sys,platform
import random
import wikipedia
ypid= os.getpid()
import logging,config
logging.basicConfig(stream=sys.stdout, level=config.logging_level, format=config.log_format)
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
    def audio_send(self, path):
        path = r"C:\Users\radhakrishnanr\Downloads\yowsup-master-jli\yowsup-master\yowsup\demos\Project\test.mp3"
        entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)
        successFn = lambda successEntity, originalEntity: self.onRequestUploadResultAudio(jid, path, successEntity, originalEntity)
        errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
    def doSendAudio(self, filePath, url, mediaType, to, ip = None):
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, mediaType, ip, to)
        self.toLower(entity)
    def onRequestUploadResultAudio(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendAudio(filePath, resultRequestUploadIqProtocolEntity.getUrl(), "audio", jid,
                             resultRequestUploadIqProtocolEntity.getIp())
        else:
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccessAudio, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()
    def onRequestUploadResult(self, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, jid, path, oup):
        logging.info("Request ok")
        #duplicate image will provide json data not found Exception error
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendImage(path,resultRequestUploadIqProtocolEntity.getUrl(),jid,resultRequestUploadIqProtocolEntity.getIp())
            mediaUploader = MediaUploader(jid, self.getOwnJid(), path,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, oup)
            logging.warning("Duplicate Image found....")
        else:
             #successFn = lambda filePath, jid, url: self.uploadOk(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
             mediaUploader = MediaUploader(jid, self.getOwnJid(), path,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccess, self.onUploadError, oup)
        mediaUploader.start()
        logging.info("Request ok upload complete")
    def onRequestUploadError(self, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logging.info("Error requesting upload url")
    def onUploadSuccessAudio(self, filePath, jid, url):
        self.doSendAudio(filePath, url, "audio", jid)
    def onUploadSuccess(self, filePath, jid, url):
        #convenience method to detect file/image attributes for sending, requires existence of 'pillow' library
        logging.info("Upload success")
        entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, jid)
        self.toLower(entity)
	entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, jid)
        self.toLower(entity)
    def onUploadError(self, filePath, jid, url):
        logging.info("Upload file failed!")
        logging.info(ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, None, jid))
    def onUploadProgress(self, filePath, jid, url, progress):
        logging.info("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        logging.info("Upload on  progress")
    def sendState(self,jid):
        entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, jid)
        self.toLower(entity)
        
    
 
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
                logging.info ('Hii from rk')
                self.sendState(jid)
                textMsg = """ [*AutoBot*]
_Hii.. Im AutoBot,Please try below commands_
*Hi* -Try this!
*wiki eagle* -Get result from Wikipedia
*wiki set-lang ta* -Set language eg: ta=tamil,en=english
*Amazon Iphone* -Get results from Amazon
*Rk* -Try this !
*gsearch baby* -Get Image
*Kabali* -Try this!
*/help* -Show this message
*exit!* -Killing AutoBot
"""
             
	    elif msgText == 'rk':
		jid = self.normalizeJid(msgFrom)
		self.sendState(jid)
                textMsg = "Welcome Boss!"
            elif 'wiki' in msgText:
                textMsg = 'Wiki Details:'
                if len(msgText.split()) > 1:
                    if msgText.split(' ')[1] == 'set-lang':         
                        try:
                            wikipedia.set_lang(msgText.split(' ')[2])
                            modwiki = 'Wiki language Changed to '+ msgText.split(' ')[2]
                        
                        except:
                            modwiki = 'Unable to Set Language'
                    elif msgText.split(' ')[1] != 'set-lang':
                        #modwiki = wikipedia.summary(msgText.split(' ',1)[1]).encode('utf-8')#encoding to avoid unicode error
                        jid = self.normalizeJid(msgFrom)
                        self.sendState(jid)
                        logging.info ('This is Wiki App')
                        try:
                            modwiki = wikipedia.summary(msgText.split(' ',1)[1]).encode('utf-8')#encoding to avoid unicode error
                        except ValueError:
                            modwiki = 'Sorry value error Page not Found!..Please try with different search term'
                        except wikipedia.exceptions.PageError:
                            modwiki = 'Sorry Page not Found!..Please try with different search term'
                        except wikipedia.exceptions.DisambiguationError as e:
                            # print (e.options)# this will print
                            modwiki = ', '.join(e.options).encode('utf-8')
                        except :
                            modwiki = 'Unknown Error Check with Rk'
                else:
                         modwiki ='Add a word after wiki to get details.Ex: wiki cool'

	    elif msgText == 'kabali':
                #Generating random Img from Folder 
                #jid = self.normalizeJid(msgFrom)
                random_filename = random.choice([
                    x for x in os.listdir(config.media_storage_path)
                    if os.path.isfile(os.path.join(config.media_storage_path, x))
                ])
                path = config.media_storage_path+'/'+random_filename
                print path
                textMsg = 'Uploading kabali Image....'
                iqEntity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE,
                                                     filePath=path)
                uploadOk = lambda successEntity, originalEntity: \
                   self.onRequestUploadResult(successEntity, originalEntity, jid, path, self.onUploadProgress)
                self._sendIq(iqEntity, uploadOk, self.onRequestUploadError)
                self.send
            elif 'gsearch' in msgText:
                self.sendState(jid)
                query=msgText.split(' ',1)[1]
                durl=downloadlink(query,'windows')
                if durl.gsearch(query):
                    random_filename=query+".jpg"
                    path = random_filename
                    textMsg = 'Uploading '+query+' Image....'
                    iqEntity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE,
                                                         filePath=path)
                    uploadOk = lambda successEntity, originalEntity: \
                       self.onRequestUploadResult(successEntity, originalEntity, jid, path, self.onUploadProgress)
                    self._sendIq(iqEntity, uploadOk, self.onRequestUploadError)
                    self.send
                else:
                      modwiki='No Image found,Please try with different search term'
                      
            elif '/dload' in msgText:
                textMsg = 'Download Details:'
                if len(msgText.split()) > 1:
                    self.sendState(jid)
                    msg=msgText.split(' ',1)[1]
                    logging.info(msg)
                    durl=downloadlink(msg,'windows')
                    durl.dlink1(msg)
                    modwiki ='Download details.Ex:completed'
                    
                    
                else:
                     modwiki ='Download details.Ex: Amazon bag'
                      
            elif 'amazon' in msgText:
                textMsg = 'Amazon Details:'
                if len(msgText.split()) > 1:
                    self.sendState(jid)
                    msg=msgText.split(' ',1)[1]
                    durl=downloadlink(msg,'windows')
                    modwiki = (durl.amazon(msg))
                    os.remove('myfile.txt')
                else:
                     modwiki ='Add a word after Amazon to get details.Ex: Amazon bag'
            elif msgText == '/help':
                logging.info ('Sending Help Msg..')
                self.sendState(jid)
                textMsg = """ [HELP]
- Commands
*/help* - Show this message.
*Hi* - Try this!
*wiki eagle* - Gets Result from Wikipedia for search 'eagle'
*wiki set-lang ta* - Set Search language for wiki eg: ta=tamil ,en=english
*Amazon Iphone* - Fetched all displayed Prize and details for product 'Iphone'
*Rk* - Try this !
*gsearch baby* -Get Image
*Kabali* - Just Try typing 'Kabali' and see for yourself!!
*exit!* - killing AutoBot
"""
            elif messageProtocolEntity.getFrom(False) == config.botAdmin and msgText == 'exit!':#only botAdmin mentioned in config can exit Autobot
                 modwiki = 'kiiling bot..'
                 os.kill(ypid, 9)
            else:
                  logging.info ('Auto Reply Disabled')
                  msgFrom = 'nomsg'
            if  msgFrom != 'nomsg':
                outgoingMessageProtocolEntity = TextMessageProtocolEntity( textMsg + " " +
                                                                            modwiki,   
                                                                            to = msgFrom)
	        self.toLower(outgoingMessageProtocolEntity)
        logging.info("Message:%s|From:%s|Time:%s|" % (messageProtocolEntity.getBody().lower().encode('utf8'),
                                               messageProtocolEntity.getFrom(False),
                                               time.ctime()))
     elif messageProtocolEntity.getType() == 'media': 
        logging.warning ("Media received")
        try:
            outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Media Not Suppported' + " " +
                                                                       time.ctime(),
                                                                       to = messageProtocolEntity.getFrom())
            self.toLower(outgoingMessageProtocolEntity)
        except ValueError:
            logging.exception ('audio not supported')
     elif message.getMediaType() == 'ptt': 
        logging.info ("Audio received")
        outgoingMessageProtocolEntity = TextMessageProtocolEntity( 'Audio Not Suppported' + " " +
                                                                       time.ctime(),
                                                                       to = messageProtocolEntity.getFrom())
        self.toLower(outgoingMessageProtocolEntity)
     elif messageProtocolEntity.getType() == 'vcard': 
        logging.info ("vcard received")
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


from lolapy import LolaSDK
from lolapy import LolaContext
from lolakrakenpy import LolaKrakenServicesManager
from .onEvents.on_image_message import OnImageMessage
from .onEvents.on_notification import OnNotification
from .onEvents.on_command import OnCommand
from .onEvents.on_new_conversation import OnNewConversation
from .messages_config import MessagesConfig
from .cip.cip_Utils import CipUtils


class LolaCipSteps:
    
    
    def __init__(self, lola_kraken: LolaKrakenServicesManager, lola_sdk: LolaSDK, config):
        self.lola_kraken_services_manager = lola_kraken
        self.lola_sdk = lola_sdk
        self.events_onImageMessage = OnImageMessage(lola_kraken,config)
        self.notifications = OnNotification(lola_kraken,config)
        self.lola_messages = MessagesConfig(config) 
        self.newConversation = OnNewConversation(lola_kraken,config)
        self.events_onCommand = OnCommand(lola_kraken,config)
        self.lola_cip_utils = CipUtils(config)
        self.config = config
        
    def initAssitantCip(self,session,ctx:LolaContext):
        self.newConversation.initAssitant(session=session,ctx=ctx)
        allowed_documents = self.lola_cip_utils.transformDocumentCountryText()
        bank_name = self.config.get("bank_name")
        welcome_message = self.lola_messages.getWelcomeMessage().format(bank_name=bank_name)
        returnMessage = welcome_message + "\n".join(allowed_documents)
        return returnMessage
        
        
        
    def scanId(self,session,ctx:LolaContext,Url:str,msg):
        resulScanId = self.events_onImageMessage.onboardingScanId(session=session,ctx=ctx,url=Url)
        return resulScanId
    def selfie(self,session,ctx:LolaContext,Url:str,msg):
        resultSelfie = self.events_onImageMessage.onboardingScanSelfie(session=session,ctx=ctx,url=Url)
        completeCipMessage = self.lola_messages.getCompleteCipMessage()
        resultProccesSelfie = {
            "resultSelfie" : resultSelfie,
            "message" : completeCipMessage
        }
        
        return resultProccesSelfie
    def PooLife(self,session,ctx:LolaContext,Url:str,msg):
        eventsData = msg['data']['data']
        typeEvent = eventsData['type']
        if typeEvent == "response":
            statusEvent = eventsData['status']
            if statusEvent == "success":
                iproovData = msg['data']['data']['response']
                iproovLastFrame = iproovData['frame']
                try:
                    facematch = self.notifications.onProofOfLife(session,ctx,iproovLastFrame,iproovData)
                    messageFacematch = str(facematch["message"])
                    return messageFacematch
                    
                except Exception as error:
                    print(error)
                    return str(error)
    def stepNotDefined(self,session,ctx:LolaContext,Url:str,msg):
        result = {
            "message" : self.lola_messages.getImageNotValidMessage()
        }
        return result   
    def commandAddress(self,session,ctx:LolaContext,cmd):
        return self.events_onCommand.comandValidateAddress(session=session,ctx=ctx,cmd=cmd)
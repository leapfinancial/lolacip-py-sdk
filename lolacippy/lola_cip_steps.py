
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
    _instance = None

    

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LolaCipSteps, cls).__new__(cls)
            cls._instance.lola_kraken = kwargs.get('lola_kraken')
            cls._instance.lola_sdk = kwargs.get('lola_sdk')
            cls._instance.config = kwargs.get('config')
            cls._instance.events_onImageMessage = OnImageMessage(cls._instance.lola_kraken,cls._instance.config)
            cls._instance.notifications = OnNotification(cls._instance.lola_kraken,cls._instance.config)
            cls._instance.lola_messages = MessagesConfig(cls._instance.config) 
            cls._instance.newConversation = OnNewConversation(cls._instance.lola_kraken,cls._instance.config)
            cls._instance.events_onCommand = OnCommand(cls._instance.lola_kraken,cls._instance.config)
            cls._instance.lola_cip_utils = CipUtils(cls._instance.config)
        return cls._instance
           
        
        
    @staticmethod
    def getInstance():
        if not LolaCipSteps._instance:
            raise Exception("LolaCipSteps not initialized")
        return LolaCipSteps._instance
    @classmethod  
    def initAssitantCip(cls,session,ctx:LolaContext):
        cls._instance.newConversation.initAssitant(session=session,ctx=ctx)
        allowed_documents = cls._instance.lola_cip_utils.transformDocumentCountryText()
        bank_name = cls._instance.config.get("bank_name")
        welcome_message = cls._instance.lola_messages.getWelcomeMessage().format(bank_name=bank_name)
        returnMessage = welcome_message + "\n".join(allowed_documents)
        return returnMessage
        
        
    @classmethod
    def scanId(cls,session,ctx:LolaContext,Url:str,msg):
        resulScanId = cls._instance.events_onImageMessage.onboardingScanId(session=session,ctx=ctx,url=Url)
        return resulScanId
    @classmethod
    def selfie(cls,session,ctx:LolaContext,Url:str,msg):
        resultclsie = cls._instance.events_onImageMessage.onboardingScanclsie(session=session,ctx=ctx,url=Url)
        completeCipMessage = cls._instance.lola_messages.getCompleteCipMessage()
        resultProccesclsie = {
            "resultclsie" : resultclsie,
            "message" : completeCipMessage
        }
        
        return resultProccesclsie
    @classmethod
    def PooLife(cls,session,ctx:LolaContext,Url:str,msg):
        eventsData = msg['data']['data']
        typeEvent = eventsData['type']
        if typeEvent == "response":
            statusEvent = eventsData['status']
            if statusEvent == "success":
                iproovData = msg['data']['data']['response']
                iproovLastFrame = iproovData['frame']
                try:
                    facematch = cls._instance.notifications.onProofOfLife(session,ctx,iproovLastFrame,iproovData)
                    messageFacematch = str(facematch["message"])
                    return messageFacematch
                    
                except Exception as error:
                    print(error)
                    return str(error)
    @classmethod
    def default(cls,session,ctx:LolaContext,Url:str,msg):
        result = {
            "message" : cls._instance.lola_messages.getImageNotValidMessage()
        }
        return result 
    @classmethod  
    def commandAddress(cls,session,ctx:LolaContext,cmd):
        return cls._instance.events_onCommand.comandValidateAddress(session=session,ctx=ctx,cmd=cmd)
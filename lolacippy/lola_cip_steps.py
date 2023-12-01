
from lolapy import LolaSDK
from lolapy import LolaContext
from lolakrakenpy import LolaKrakenServicesManager
from .onEvents.on_image_message import OnImageMessage
from .messages_config import MessagesConfig

class LolaCipSteps:
    
    
    def __init__(self, lola_kraken: LolaKrakenServicesManager, lola_sdk: LolaSDK, config):
        self.lola_kraken_services_manager = lola_kraken
        self.lola_sdk = lola_sdk
        self.events_onImageMessage = OnImageMessage(lola_kraken,config)
        self.lola_messages = MessagesConfig(config) 
        
        
    def scanId(self,session,ctx:LolaContext,scanIdUrl:str):
        resulScanId = self.events_onImageMessage.onboardingScanId(session=session,ctx=ctx,url=scanIdUrl)
        return resulScanId
    def selfie(self,session,ctx:LolaContext,selfieUrl:str):
        resultSelfie = self.events_onImageMessage.onboardingScanSelfie(session=session,ctx=ctx,url=selfieUrl)
        completeCipMessage = self.lola_messages.getCompleteCipMessage()
        resultProccesSelfie = {
            "resultSelfie" : resultSelfie,
            "message" : completeCipMessage
        }
        
        return resultProccesSelfie
        pass
    def test3(self):
        pass
    def test4(self):
        pass
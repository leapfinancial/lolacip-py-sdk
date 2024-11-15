
from lolapy import LolaSDK
from lolapy import LolaContext
from lolakrakenpy import LolaKrakenServicesManager
import requests
from lolacippy.onEvents.util_events import UtilEvents
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
        self.util_events = UtilEvents(lola_kraken,config)
        self.config = config
        self.serverFrontEnd = config.get("SERVER_FRONTEND_URL")
        self.utilEvents = UtilEvents(lola_kraken,config)
        
    def initAssitantCip(self,session,ctx:LolaContext):
        self.newConversation.initAssitant(session=session,ctx=ctx)
        allowed_documents = self.lola_cip_utils.transformDocumentCountryText()
        bank_name = self.config.get("bank_name")
        allowed_documents = self.config.get("allowed_documents")
        welcome_message = self.lola_messages.getWelcomeMessage().format(bank_name=bank_name)
        returnMessage = welcome_message + "\n".join(allowed_documents)
        return returnMessage
        
        
        
    def scanId(self,session,ctx:LolaContext,Url:str,msg,language:str="en"):
        resulScanId = self.events_onImageMessage.onboardingScanId(session=session,ctx=ctx,url=Url,language=language)
        return resulScanId
    def selfie(self,session,ctx:LolaContext,Url:str,msg,language:str="en"):
        resultSelfie = self.events_onImageMessage.onboardingScanSelfie(session=session,ctx=ctx,url=Url)
        completeCipMessage = self.lola_messages.getCompleteCipMessage()
        resultProccesSelfie = {
            "resultSelfie" : resultSelfie,
            "message" : completeCipMessage
        }
        
        return resultProccesSelfie
    def PooLife(self,session,ctx:LolaContext,Url:str,msg,language:str="en"):
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
                    validate_pol = self.utilEvents.messageAndFlowStepPOL(session,ctx,language)
                    profile_pol = validate_pol.get("profile")                   
                    self.responseScanIdMessage = validate_pol["message"]
                    result_scan = {
                        "message" : self.responseScanIdMessage
                    }
                    return result_scan
    def SSNSelfie(self,session,ctx:LolaContext,Url:str,msg,language:str="en"):
        state = ctx.state.get()
        profile = state["profile"]
        exrtraDataSSN = profile['extraDataSSN']
        extraData = exrtraDataSSN['extradata']
        requestToken = extraData['requestToken']
        ItinToken = extraData['ssn_itin_token']
        
        endpoint = self.serverFrontEnd + "/complete-ssn-itin-signup"
        data = {
            "ssnItinToken": ItinToken,
            "selfieImageUrl": Url
        }
        headers = {'Request-Token': requestToken, 'Content-Type': 'application/json'}
        try:
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            message= self.lola_messages.getNiceSelfieMessage()
            result = {
                "message" : message
                
            }
            return result
        except Exception as error:
            print(error)
            raise ValueError(error)
        
        
    def SSNPOL(self,session,ctx:LolaContext,Url:str,msg,language:str="en"):
        state = ctx.state.get()
        profile = state["profile"]
        extraData = profile['extraDataSSN']
        requestToken = extraData['requestToken']
        ItinToken = extraData['ssn_itin_token']
        eventsData = msg['data']['data']
        typeEvent = eventsData['type']
        if typeEvent == "response":
            statusEvent = eventsData['status']
            if statusEvent == "success":
                iproovData = msg['data']['data']['response']
                iproovLastFrame = iproovData['frame']
                try:
                    endpoint = self.serverFrontEnd + "/complete-ssn-itin-signup"
                    data = {
                        "ssnItinToken": ItinToken,
                        "selfieImageB64": iproovLastFrame
                    }
                    headers = {'Request-Token': requestToken, 'Content-Type': 'application/json'}
                    response = requests.post(endpoint, headers=headers, json=data)
                    response.raise_for_status()
                    message= self.lola_messages.getNiceSelfieMessage()
                    result = {
                        "message" : message
                        
                    }
                    return result
                except Exception as error:
                    print(error)
                    raise ValueError(error)
                    
    
    
    def default(self,session,ctx:LolaContext,Url:str,msg,language:str="en"):
        result = {
            "message" : self.lola_messages.getImageNotValidMessage()
        }
        return result   
    def commandAddress(self,session,ctx:LolaContext,cmd):
        return self.events_onCommand.comandValidateAddress(session=session,ctx=ctx,cmd=cmd)
    def LolaMessages(self):
        return self.lola_messages
    def getConfigPOL(self):
        status = self.util_events.returnPOLStatus()
        return status
    def getIproovURL(self,session):
        return self.util_events.returnIprrovLink(session)
    
    
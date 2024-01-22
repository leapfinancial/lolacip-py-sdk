
from lolapy import LolaContext
from ..cip.cip_Bussines_Rules import Cip
from ..cip.cip_Utils import CipUtils
from ..messages_config import MessagesConfig
from lolakrakenpy import LolaKrakenServicesManager
from .util_events import UtilEvents

class OnImageMessage:
    def __init__(self,lola_kraken:LolaKrakenServicesManager,config):
        self.lola_cip_Bussines = Cip(lola_kraken,config)
        self.lola_cip_utils = CipUtils(config)
        self.lola_messages = MessagesConfig(config)
        self.utilEvents = UtilEvents(lola_kraken,config)
        self.faceMatchConfidence = 0.65
        str_ProofOfLife = config.get("proof_of_life","False")
        str_webhookActive = config.get("webhook_url_cip","False")
        str_faceMatchConfidence = config.get("face_match_confidence","0.65")
        str_validate_Adrress = config.get("validate_Address","False")

        self.proof_of_life :bool = str_ProofOfLife.lower() == 'true'
        self.webhookActive :bool = str_webhookActive.lower() == 'true'
        self.validate_Adrress :bool = str_validate_Adrress.lower() == 'true'
        self.faceMatchConfidence = float(str_faceMatchConfidence)
        self.responseScanIdMessage = ""
        
    def onboardingScanId(self,session,ctx:LolaContext,url):
        try:
            state = ctx.state.get()
            profile = state["profile"]
            validate_document = profile.get("validate_document",True)
            checkImageMessage = self.lola_messages.getCheckImageMessage()
            ctx.messanger.send_text_message(checkImageMessage, blend=True,appendToHistory=True)
            resultScanId = self.lola_cip_Bussines.scanId(session, url,validate_document)
            if resultScanId:
            
                ocrData = resultScanId['ocrData']
                ocrData = self.lola_cip_utils.prepareDataOcr(ocrData)
                profile = self.lola_cip_utils.prepareProfileCip(profile,ocrData)
                
                    
                checkImageWaitMessage = self.lola_messages.getCheckImageWaitMessage()
                userFirstName = profile["firstName"]
                ctx.messanger.send_text_message(f"Hey there {userFirstName}! {checkImageWaitMessage}", blend=True,appendToHistory=True)

                    
                state["profile"] = profile
                ctx.state.set(state)
                    
                resultFaceCrop = self.lola_cip_Bussines.faceCrop(session, url)
                face = resultFaceCrop["results"]["face"]
                ctx.session_store.set("ocrData", ocrData)
            
                ctx.session_store.set("faceCrop", face)
                ctx.session_store.set("documentUrl", url)
                
                if self.validate_Adrress:
                    address = ocrData.get("Address", None)
                    if address == None:
                        profile["flow_step"] = "ScanId"
                        state["ocrData"] = ocrData
                        profile["request_address"] = True
                        state["profile"] = profile
                        ctx.state.set(state)
                        messageRequestAddress = self.lola_messages.getRequestAddressMessage()
                        result_scan = {
                            "flow_step": profile["flow_step"],
                            "message" : messageRequestAddress
                        }
                        return result_scan
                    else:
                        profile["address"] = address
                
                validate_pol = self.utilEvents.messageAndFlowStepPOL(session,ctx)
                profile_pol = validate_pol.get("profile")                   
                self.responseScanIdMessage = validate_pol["message"]
                              
                state["profile"] = profile_pol
                state["ocrData"] = ocrData
                ctx.state.set(state)
                result_scan = {
                    "flow_step": profile["flow_step"],
                    "message" : self.responseScanIdMessage
                }
                return result_scan 
        except Exception as error:
            print(error)
            raise ValueError(error)
        
    def onboardingScanSelfie(self,session,ctx:LolaContext,url):
        try:
            state = ctx.state.get()
            profile = state["profile"]
            name = profile["firstName"]
            ocrData = ctx.session_store.get("ocrData")
            documentUrl = ctx.session_store.get("documentUrl")
            niceSelfieMessage = self.lola_messages.getNiceSelfieMessage()
            ctx.messanger.send_text_message(niceSelfieMessage+f" {name}! ✅! 🤩", blend=True,appendToHistory=True)
            imageCrop = ctx.session_store.get("faceCrop")
            resultFaceMatch = self.lola_cip_Bussines.faceMatch(session,imageCrop, url)
            identical = resultFaceMatch["identical"]
            confidence = resultFaceMatch["confidence"]
            #if identical and confidence > 0.95:
            status = resultFaceMatch["status"]
            
            if status == "success":
                if identical and confidence > 0.95:
                    realSelfieMessage = self.lola_messages.getRealSelfieMessage()
                    raise ValueError(realSelfieMessage)
                if identical:                                               
                    profile["flow_step"] = "finish"
                    profile["cip_finished"] = True
                    profile["selfie_uploaded"] = True
                    state["profile"] = profile
                    ctx.state.set(state)
                if self.webhookActive:
                    try:
                        sendData ={
                            "ocrData": ocrData,
                            "documentUrl": documentUrl,
                            "faceCrop": imageCrop,
                            "resultFaceMatch": resultFaceMatch,
                            "profile": profile
                        }
                        self.lola_cip_Bussines.sendDataWebhook(sendData)
                    except Exception as error:
                        print(error)
                        raise ValueError(str(error))
            else:
                raise ValueError("The face match status is not success")
        except Exception as error:
            print(error)
            raise ValueError(error)
    def ScanDocument(self,session,ctx:LolaContext,url):
        try:
            resultScanDocument = self.lola_cip_Bussines.scanDocument(session, url)
            print(resultScanDocument)
        except Exception as error:
            print(error)
            raise ValueError(error)
                 

from lolapy import LolaContext
from lolakrakenpy import LolaKrakenServicesManager
from ..cip.cip_Bussines_Rules import Cip
from ..cip.cip_Utils import CipUtils
from ..messages_config import MessagesConfig

class OnNotification:
    def __init__(self,lola_kraken:LolaKrakenServicesManager,config):
        self.lola_cip_Bussines = Cip(lola_kraken,config)
        self.lola_cip_utils = CipUtils(config)
        self.lola_messages = MessagesConfig(config)
        str_ProofOfLife = config.get("proof_of_life","False")
        str_webhookActive = config.get("webhook_url_cip","False")
        str_faceMatchConfidence = config.get("face_match_confidence","0.65")

        self.proof_of_life :bool = str_ProofOfLife.lower() == 'true'
        self.webhookActive :bool = str_webhookActive.lower() == 'true'
        self.faceMatchConfidence = float(str_faceMatchConfidence)
        self.responseScanIdMessage = ""

    def onProofOfLife(self,session,ctx:LolaContext,frameBase64,POLResult=None):
        try:
            state = ctx.state.get()
            profile = state["profile"]
            facecrop = ctx.session_store.get("faceCrop")
            ocrData = ctx.session_store.get("ocrData")
            documentUrl = ctx.session_store.get("documentUrl")
            faceMatch = self.lola_cip_Bussines.faceMatch(session,frameBase64,None, facecrop)
            faceMatchIdentical = faceMatch["identical"]
            faceMatchConfidence = faceMatch["confidence"]
            ctx.messanger.send_text_message("Face Match Result", isPrivate=True)
            ctx.messanger.send_text_message(str(faceMatch), isPrivate=True)
            faceMatchStatus = faceMatch["status"]
            imageCrop = ctx.session_store.get("faceCrop")
            message = ""
            if faceMatchStatus == "success" :
                if faceMatchIdentical:
                    if faceMatchConfidence > 0.95:
                        getRealSelfieMessage = self.lola_messages.getRealSelfieMessage()
                        message = getRealSelfieMessage                    
                    elif faceMatchConfidence >= self.faceMatchConfidence:
                        messageFinish = self.lola_messages.getCompleteCipMessage()
                        message = messageFinish
                        profile["flow_step"] = "finish"
                        profile["selfie_uploaded"] = True
                        profile["cip_finished"] = True
                        state["profile"] = profile
                        ctx.state.set(state)
                        if self.webhookActive:
                            try:
                                sendData ={
                                    "ocrData": ocrData,
                                    "documentUrl": documentUrl,
                                    "faceCrop": imageCrop,
                                    "resultFaceMatch": faceMatch,
                                    "profile": profile,
                                    "POLResult": POLResult,
                                    
                                }
                                self.lola_cip_Bussines.sendDataWebhook(sendData)
                            except Exception as error:
                                raise ValueError(error)
                    else:
                        raise ValueError("The face match confidence is less than 65 porcent")
                else:
                    raise ValueError("The face match is not identical")
            else:
                raise ValueError("The face match status is not success")
            response = {
                "faceMatchIdentical":faceMatchIdentical,
                "faceMatchConfidence":faceMatchConfidence,
                "faceMatchStatus":faceMatchStatus,
                "message":message
            }
            return response
            
        except Exception as error:
            raise ValueError(error)
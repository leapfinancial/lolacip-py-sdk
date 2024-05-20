from lolapy import LolaContext
from ..cip.cip_Bussines_Rules import Cip
from lolakrakenpy import LolaKrakenServicesManager
from ..messages_config import MessagesConfig

class UtilEvents:
    def __init__(self,lola_kraken:LolaKrakenServicesManager,config):
        
        str_ProofOfLife = config.get("proof_of_life","False")
        
        
        
        self.proof_of_life :bool = str_ProofOfLife.lower() == 'true'
        self.config = config
        self.lola_cip_Bussines = Cip(lola_kraken,config)
        self.lola_messages = MessagesConfig(config)
        self.responseScanIdMessage = ""
        
    def messageAndFlowStepPOL(self,session,ctx:LolaContext):
        try:
            state = ctx.state.get()
            profile = state["profile"]
            message = self.responseScanIdMessage
            profile["flow_step"] = "ProofOfLife"
            state["profile"] = profile
            polActive = state.get("polActive",None)
            print(polActive)
            if polActive is not None:
                if isinstance(polActive, str):
                    print("is string")                
                    if polActive.lower() == 'true':
                        polActive = True
                    else:
                        polActive = False    
                self.proof_of_life = polActive
            ctx.state.set(state)
            if self.proof_of_life:
                profile["flow_step"] = "ProofOfLife"
                profile["document_uploaded"] = True
                url_iproov = self.lola_cip_Bussines.getLinkIproov(session)
                url_iproov = url_iproov["url"]
                messageIproov = self.lola_messages.getMessageProofOfLife()
                messageIproov = messageIproov.replace('$link',url_iproov)
                message= messageIproov
                self.responseScanIdMessage = messageIproov
            else:                    
                profile["flow_step"] = "ScanSelfie"
                profile["document_uploaded"] = True
                self.responseScanIdMessage = self.lola_messages.getRequestSelfieMessage()
                message = self.lola_messages.getRequestSelfieMessage()
            
            result_POL = {
                "profile": profile,
                "message" : message
            }
            return result_POL
        except Exception as error:
            print(error)
            raise ValueError(error)
    def returnPOLStatus(self):
        return self.proof_of_life
from lolakrakenpy import LolaKrakenServicesManager
from lolapy import LolaContext
from ..cip.cip_Bussines_Rules import Cip
from ..cip.cip_Utils import CipUtils
from ..messages_config import MessagesConfig
from ..init_assitant import Init_assitant

class OnNewConversation:
    
    def __init__(self,lola_kraken:LolaKrakenServicesManager,config):
        self.lola_cip_Bussines = Cip(lola_kraken,config)
        self.lola_cip_utils = CipUtils(config)
        self.lola_messages = MessagesConfig(config)
        self.init_assitant = Init_assitant(config)
                
    def initAssitant(self,session,ctx:LolaContext):
        state = ctx.state.get()
                #profile init
        profile = self.init_assitant.getInitProfile()
        stateprofile = state["profile"]
        # unir profile y stateprofile
        if stateprofile is not None:
            profile.update(stateprofile)
            state["profile"] = profile
        else:
            state["profile"] = profile
                #allowed documents
        allowed_documents = self.init_assitant.getInitAllowedDocuments()
        state["allowed_documents"] = allowed_documents
        ctx.state.set(state)


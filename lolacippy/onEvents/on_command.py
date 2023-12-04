from lolapy import LolaContext
from lolakrakenpy import LolaKrakenServicesManager
from .util_events import UtilEvents
from ..messages_config import MessagesConfig
class OnCommand:
    def __init__(self,lola_kraken:LolaKrakenServicesManager,config):
        self.lola_kraken = lola_kraken
        self.config = config
        self.utilEvents = UtilEvents(lola_kraken,config)
        self.lola_messages = MessagesConfig(config)
    
    def comandValidateAddress(self,session,ctx:LolaContext,cmd):
        state = ctx.state.get()
        profile = state["profile"]
        requestAddress = profile.get("request_address",False)
        comandData = cmd.get("data")
        comandArguments = comandData.get("args")
        address = comandArguments.get("address")
        city = comandArguments.get("city")
        statename = comandArguments.get("state")
        zip_code = comandArguments.get("zip_code")
        if city == "":
            messageToUser = self.lola_messages.getMessageProvideCity()
            raise ValueError(messageToUser)
        if statename == "":
            messageToUser = self.lola_messages.getMessageProvideState()
            raise ValueError(messageToUser)
        if zip_code == "":
            messageToUser = self.lola_messages.getMessageProvideZipCode()
            raise ValueError(messageToUser)
        if requestAddress:
            addressfull = address + "," + city + "-" + statename + ",zip code" + zip_code
            try:
                
                validateAddress = self.utilValidateAddress(addressfull)
            
                isvalidAddress = validateAddress["isValid"]
            
                if not isvalidAddress:
                    raise self.lola_messages.getMessageAddressNotValid()
                    
                validateAddressData = validateAddress["data"]
                validateAddressData = validateAddressData["country"]
                validatePOL = self.utilEvents.messageAndFlowStepPOL(session,ctx)
                profile = validatePOL.get("profile")        
                profile["address"] = addressfull
                del profile["request_address"]                   
                state["profile"] = profile   
                ctx.state.set(state)
                messageToUser = validatePOL["message"]
                
                return messageToUser
                   
                       
            except Exception as error:
                print(error)
                raise ValueError(error)
       
        else:
            return self.lola_messages.getMessageAddressCustomerValid()
    
    
    def utilValidateAddress(self,address= None):
        validateAdressKraken = self.lola_kraken.utilsServices.validateAddress(address=address)
        return validateAdressKraken
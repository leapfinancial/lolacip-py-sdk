
import json
from lolakrakenpy import LolaKrakenServicesManager
from .cip_Utils import CipUtils
from .cip_messages_config import MessagesConfig
from lolapy import LolaContext
from time import sleep

class Cip:
    
    def __init__(self,lolaKrakenServicesManager: LolaKrakenServicesManager,config):
        self.lola_kraken = lolaKrakenServicesManager
        str_validateDocument_exp:str = config['validate_document_exp']
        allowed_documents = config["allowed_documents"]
        str_allowed_documents_country:str = config['allowed_document_country']
        str_development:str = config['Development']
        
        
        validate_document_exp:bool = str_validateDocument_exp.lower() == 'true'
        develoment:bool = str_development.lower() == 'true'
        allowed_documents = json.loads(allowed_documents)
        allowed_documents_country = json.loads(str_allowed_documents_country)
        
        self.validateDocument:bool = validate_document_exp
        self.allowed_documents:[] = allowed_documents
        self.allowed_documents_country:[] = allowed_documents_country
        self.cipUtils = CipUtils(config)
        self.develoment:bool = develoment
        self.url_return = config.get("return_url","https://www.google.com")
        
        
        self.cipMessagesConfig = MessagesConfig(config)
                
    def scanId(self,sesion,url:str,ctx:LolaContext,validateDocument:bool = True):
        self.lola_kraken.start(sesion)
            
        try:
            orcResult = self.lola_kraken.visionServices.scanGenericId(url=url)
            ctx.messanger.send_text_message("OCR Result", isPrivate=True)
            ctx.messanger.send_text_message(str(orcResult), isPrivate=True)
            ocrData = orcResult['data']
            expDate = ocrData['ExpDate']            
            IsimageManipulation = orcResult['IsimageManipulation']
            IsValidID = orcResult['IsValidID']
            print(f'oCRData: {ocrData}')
            documentValidate = self.cipUtils.documentExpirate(expDate)
            if validateDocument:
                if not IsValidID:
                    print(f'IsValidID: {IsValidID}')
                    isNotValidDocumentMessage = self.cipMessagesConfig.getImageNotValidMessage()
                    print('The document is not valid') 
                    raise ValueError(isNotValidDocumentMessage)
                if IsimageManipulation:
                    print(f'IsimageManipulation: {IsimageManipulation}')
                    IsimageManipulationMessage = self.cipMessagesConfig.getImageManipulationMessage()
                    print('The image is manipulated') 
                    raise ValueError(IsimageManipulationMessage)
            
            documentType = ocrData['DocumentType']
            documentName = ocrData['DocumentName']
            documentCountry = ocrData.get("Country2","")
            if documentCountry == "":
                documentCountryNotExistsMessage = self.cipMessagesConfig.getDocumentNotExistMessage()
                raise ValueError(documentCountryNotExistsMessage)
            if not documentValidate and self.validateDocument :
                print('The document is expired')
                documentExpirateMessage = self.cipMessagesConfig.getDocumentExpiredMessage() 
                raise ValueError(documentExpirateMessage)              
            
            if documentType in self.allowed_documents_country and (documentCountry in self.allowed_documents_country[documentType] or "All" in self.allowed_documents_country[documentType]):
                print("The document is allowed. in your documentCountry " + documentCountry)
                return {
                    "result":True,
                    "ocrData":ocrData
                }
            else:                
                allowed_documents = self.cipUtils.transformDocumentCountryText()      
                documentNotAlloewdMessage = self.cipMessagesConfig.getDocumentNorAllowedMessage()
                print("The document is not allowed.in your documentCountry " + documentCountry)
                raise ValueError(f"Oops! 🚫 {documentName} "+documentNotAlloewdMessage + "\n".join(allowed_documents))
           
        except Exception as error:
            print(error)
            raise ValueError(error)
        
    def faceCrop(self,sesion,url):
        self.lola_kraken.start(sesion)
        try:
            faceCropResult = self.lola_kraken.visionServices.extractFace(url=url)
            return faceCropResult
        except Exception as error:
            print(error)
            raise ValueError("Error en el servicio faceCrop")
    
    def faceMatch(self,sesion,image,url2,image2Base64=None):
        self.lola_kraken.start(sesion)
        try:
            faceMatchResult = self.lola_kraken.visionServices.faceMatch(image=image,url2=url2,image2=image2Base64)
            return faceMatchResult
        except Exception as error:
            print(error)
            raise ValueError("Error en el servicio faceMatch")
    def scanDocument(self,sesion,url):
        self.lola_kraken.start(sesion)
        try:
            scanDocumentResult = self.lola_kraken.visionServices.scanGenericId(url=url)
            return scanDocumentResult
        except Exception as error:
            print(error)
            raise ValueError("Error en el servicio scanDocument")
    def sendDataWebhook(self,data:json):
        try:
            response = self.cipUtils.sendWebhookCip(data)
            return response
        except Exception as error:
            print(error)
            raise ValueError(error)         
    def getLinkIproov (self,session,language:str="en"):
        try:
            self.theme = {}
            with open('iproovTheme.json') as json_file:
                self.theme = json.load(json_file)
            urlReturn = self.url_return
            print(urlReturn)
            print(str(self.theme))
            print(str(self.develoment))            
            retries = 0
            while retries < 3:
                try:                    
                    link = self.lola_kraken.iproovServices.claimLink(returnUrl=urlReturn, theme=self.theme, develoment=self.develoment, language=language)
                    print(link)
                    break
                except Exception as e:
                    retries += 1
                    sleep(1+(retries*2))                    
            if link != None:
                return link
            else:
                raise ValueError("error en el servicio getLinkIproov")
        except Exception as error:
            print(error)
            raise ValueError("error en el servicio getLinkIproov")
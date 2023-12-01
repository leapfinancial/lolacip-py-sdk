
from datetime import datetime
import json

import requests


class CipUtils:
    def __init__(self,config):
        str_allowed_documents_country:str = config['allowed_document_country']
        
        self.webhook_url_cip:str = config.get('WEBHOOK_URL_RESULT_CIP',"") 
        str_webhook_url_cip = config.get('webhook_url_cip',"False")
        self.webhook_url_cip_active:bool = str_webhook_url_cip.lower() == 'true'
        str_webhook_cip_headers = config.get('WEBHOOK_CIP_HEADERS','{"content-type": "application/json"}')
        
        str_webhook_cip_headers = str_webhook_cip_headers.replace("'", '"')
        str_development:str = config['Development']

        webhook_cip_headers = json.loads(str_webhook_cip_headers)
        allowed_documents_country = json.loads(str_allowed_documents_country)
        develoment:bool = str_development.lower() == 'true'
        
        self.allowed_documents_country:[] = allowed_documents_country
        self.webhook_cip_headers:[] = webhook_cip_headers
        self.develoment:bool = develoment
        
    def documentExpirate(self,expDate):
        #if expDate its str format 'yyyy' transform to 'yyyy-mm-dd' in the last day of the year
        if(len(expDate)==4):
            expDate = expDate+'-12-31'
        #if expDate its str format 'yyyy-mm' transform to 'yyyy-mm-dd' in the last day of the month
        elif(len(expDate)==7):
            expDate = expDate+'-31'
        #if expDate its str format 'yyyy-mm-dd' transform to 'yyyy-mm-dd'
        elif(len(expDate)==10):
            expDate = expDate
        else:
            raise ValueError('The date format is not correct')
        expDate = datetime.strptime(expDate, '%Y-%m-%d')
        expiration = expDate > datetime.now()
        return expiration
    def transformDocumentCountryText(self):
        allowed_document_country = self.allowed_documents_country
        allowed_documents = []
        for doc, countries in allowed_document_country.items():
            if "All" in countries:
                allowed_documents.append(f"- {doc}")
            else:
                for country in countries:
                    allowed_documents.append(f"- {doc} ({country})")
        return allowed_documents
    def prepareDataOcr(self,ocrData):
        firstName = ocrData["FirstName"]
        MiddleName = ocrData.get("MiddleName", "")
        lastName = ocrData["LastName"]
        secondLastName = ocrData.get("SecondLastName", "")
        if MiddleName =="":
            #contar la cantidad de palabras en el nombre
            words = len(firstName.split())
                        
            if words > 1:
                name_parts = firstName.split()
                MiddleName = "".join(name_parts[1:])
                firstName = firstName.split()[0]
            if secondLastName =="":
                #contar la cantidad de palabras en el nombre
                words = len(lastName.split())
                        
                if words > 1:
                    name_parts = lastName.split()
                    secondLastName = "".join(name_parts[1:])
                    lastName = lastName.split()[0]
        ocrData["FirstName"] = firstName
        ocrData["MiddleName"] = MiddleName
        ocrData["LastName"] = lastName
        ocrData["SecondLastName"] = secondLastName
        return ocrData
    
    def prepareProfileCip(self,profile,ocrData):
        firstName = ocrData["FirstName"]
        MiddleName = ocrData.get("MiddleName", "")
        lastName = ocrData["LastName"]
        secondLastName = ocrData.get("SecondLastName", "")
        profile["firstName"] = firstName
        profile["MiddleName"] = MiddleName
        profile["lastName"] = lastName
        profile["secondLastName"] = secondLastName
        return profile
    def sendWebhookCip(self,data:json):
        try:
            if not self.webhook_url_cip_active:
                print("The webhook_url_cip_active is False")
                return True
            if self.webhook_url_cip == "":
                print("The webhook_url_cip is empty")
                raise ValueError("The webhook_url_cip is empty")
            webhook_url_cip = self.webhook_url_cip
            
            
            response = requests.post(self.webhook_url_cip, headers=self.webhook_cip_headers,json=data)
            response.raise_for_status()
            return True
            
        except Exception as error:
            print(error)
                    
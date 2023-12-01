import json


class Init_assitant():
    def __init__(self,config):
        
        profile = config["profile"]
        allowed_documents = config["allowed_documents"]
                
        profile = json.loads(profile)
        allowed_documents = json.loads(allowed_documents)
         
        self.profile = profile
        self.allowed_documents = allowed_documents
        
        
        
    def getInitProfile (self):
        return self.profile
    def getInitAllowedDocuments (self):
        return self.allowed_documents
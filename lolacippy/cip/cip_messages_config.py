
class MessagesConfig:
    def __init__(self, config):
        self.config = config
        self.is_not_valid_document_message = config["is_not_valid_document_message"]
        self.is_image_manipulation_message = config["is_image_manipulation_message"]
        self.document_not_exist_message = config["document_not_exist_message"]
        self.document_expired_message = config["document_expired_message"]
        self.document_not_allowed_message = config["document_not_allowed_message"]
                    
    def getImageNotValidMessage(self):
        return self.is_not_valid_document_message
    def getImageManipulationMessage(self):
        return self.is_image_manipulation_message
    def getDocumentNotExistMessage(self):
        return self.document_not_exist_message
    def getDocumentExpiredMessage(self):
        return self.document_expired_message
    def getDocumentNorAllowedMessage(self):
        return self.document_not_allowed_message
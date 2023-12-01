
class MessagesConfig:
    def __init__(self, config):
        self.config = config
        self.welcome_message = config["welcome_message"]
        self.check_image_message = config["check_image_message"]
        self.check_image_wait_message = config["check_image_wait_message"]
        self.request_selfie_message = config["request_selfie_message"]
        self.nice_selfie_message = config["nice_selfie_message"]
        self.real_selfie_message = config["real_selfie_message"]
        self.complete_cip_message = config["complete_cip_message"]
        self.complete_image_cip_message = config["complete_image_cip_message"]
        self.image_not_valid_message = config["image_not_valid_message"]
        self.message_proof_of_life = config["message_proof_of_life"]   
        self.request_message_address = config["request_Address_message"]
        self.message_provide_city = config["message_provide_city"]
        self.message_provide_state = config["message_provide_state"]
        self.message_provide_zip_code = config["message_provide_zipcode"]
        self.message_address_not_valid = config["message_address_not_valid"]
        self.message_address_customer_valid = config["message_address_customer_valid"]
               
    def getWelcomeMessage(self):
        return self.welcome_message
    def getCheckImageMessage(self):
        return self.check_image_message
    def getCheckImageWaitMessage(self):
        return self.check_image_wait_message
    def getRequestSelfieMessage(self):
        return self.request_selfie_message
    def getNiceSelfieMessage(self):
        return self.nice_selfie_message
    def getRealSelfieMessage(self):
        return self.real_selfie_message
    def getCompleteCipMessage(self):
        return self.complete_cip_message
    def getCompleteImageCipMessage(self):
        return self.complete_image_cip_message
    def getImageNotValidMessage(self):
        return self.image_not_valid_message
    def getMessageProofOfLife(self):
        return self.message_proof_of_life
    def getRequestAddressMessage(self):
        return self.request_message_address
    def getMessageProvideCity(self):
        return self.message_provide_city
    def getMessageProvideState(self):
        return self.message_provide_state
    def getMessageProvideZipCode(self):
        return self.message_provide_zip_code
    def getMessageAddressNotValid(self):
        return self.message_address_not_valid
    def getMessageAddressCustomerValid(self):
        return self.message_address_customer_valid
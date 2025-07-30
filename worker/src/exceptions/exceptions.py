
class UnavailablePaymentProcessorException(Exception):
    def __init__(self, message="Payment processor is currently unavailable. Please try again later."):
        self.message = message
        super().__init__(self.message)
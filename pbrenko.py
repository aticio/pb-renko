# flake8: noqa
class PbRenko:
    """Renko initialization class
    """
    def __init__(self, percent, data):
        self.percent = percent
        self.data = data
    
    def create_pbrenko(self):
        print("works")
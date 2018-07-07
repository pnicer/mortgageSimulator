class Config:
    def __init__(self, data):
        self.type = data['type']
        self.period = data['period']
        self.required_funds = data['requiredFunds']
        self.starting_funds = data['startingFunds']
        self.wibor = data['wibor']
        self.interest_rate = data['interestRate']
        self.monthly_rate_inc = data['monthlyIncreasedRate']

from .calculator import Constant


class SimulatorResultsDiff:
    def __init__(self, sim_one, sim_two):
        self.starting_value = sim_two.config.starting_funds - sim_one.config.starting_funds
        self.value = sim_two.interests_value - sim_one.interests_value
        self.period = sim_two.config.period - sim_one.config.period
        self.rates_num = len(sim_two.rates) - len(sim_one.rates)
        self.rate_value = sim_two.rates[0].value - sim_one.rates[0].value

    def print(self):
        print('---- Diff -----')
        print(f'Starting funds: {self.starting_value}')
        print(f'Cost: {self.value}')
        print(f'Period: {self.period}')
        print(f'Rates number: {self.rates_num}')
        print(f'Rate diff: {self.rate_value}')


class SimulatorResults:
    def __init__(self, config, rates, mortgage_value):
        self.rates = rates
        self.config = config
        self.mortgage_value = mortgage_value
        self.total_value = 0
        self.interests_value = 0
        for rate in self.rates:
            self.total_value += rate.value
            self.interests_value += rate.interests

    def print(self, rates=False):
        if rates:
            print('---- Rates ----')
            for rate in self.rates:
                print(rate)
        print('----Summary----')
        print(f'Period: {self.config.period} months')
        print(f'Starting funds: {self.config.starting_funds}')
        print(f'Required funds: {self.config.required_funds}')
        print(f'Mortgage value: {self.mortgage_value}')
        print(f'Monthly increased rates: {self.config.monthly_rate_inc}')
        print(f'Interests value: {self.interests_value}')
        print(f'Total cost: {self.total_value}')
        print(f'First rate: {self.rates[0].value}')


class Simulator:
    def __init__(self, config):
        self.config = config
        self.mortgage_value = config.required_funds - config.starting_funds

        if self.config.type == 'constant':
            self.calculator = Constant(self.mortgage_value, config.period, config.interest_rate, config.wibor,
                                       config.monthly_rate_inc, config.additional_payments)
        else:
            self.calculator = Constant(self.mortgage_value, config.period, config.interest_rate, config.wibor,
                                       config.monthly_rate_inc, config.additional_payments)

    def simulate(self):
        rates = self.calculator.calc_rates()
        total_value = 0
        interests_value = 0
        for rate in rates:
            total_value += rate.value
            interests_value += rate.interests

        return SimulatorResults(self.config, rates, self.mortgage_value)

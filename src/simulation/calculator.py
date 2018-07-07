import abc


class Rate:
    def __init__(self, number, value, interests, loan_paid, monthly_rate_inc, left):
        self.value = value
        self.interests = interests
        self.loan_paid = loan_paid
        self.number = number
        self.monthly_rate_inc = monthly_rate_inc
        self.left = left

    def __repr__(self):
        return f'{self.number} total: {self.value} (+{self.monthly_rate_inc}),' \
               f' interests: {self.interests}, loan: {self.loan_paid}, left: {self.left}'


class Calculator(abc.ABC):
    def __init__(self, mortgage_value, period, interest_rate, wibor, monthly_rate_inc):
        self.mortgage_value = mortgage_value
        self.period = period
        self.interest_rate = interest_rate
        self.wibor = wibor
        self.monthly_rate_inc = monthly_rate_inc
        self.total_interests = (self.interest_rate + self.wibor) / 100

    @abc.abstractmethod
    def calc_rates(self):
        ...


class Constant(Calculator):
    def calc_rates(self):
        interests_per_month = self.total_interests / 12
        q = 1 + interests_per_month
        value = self.mortgage_value * q ** self.period * (q-1) / ((q ** self.period) - 1)
        rates = []
        loan_paid = 0
        mortgage_paid = False

        for i in range(0, self.period):
            month_interests = (self.mortgage_value - loan_paid) * interests_per_month
            month_loan_paid = value - month_interests + self.monthly_rate_inc

            loan_paid += month_loan_paid
            rate_value = value + self.monthly_rate_inc
            left = round(self.mortgage_value - loan_paid, 2)

            if loan_paid >= self.mortgage_value:
                month_loan_paid_diff = loan_paid - self.mortgage_value
                rate_value -= month_loan_paid_diff
                month_loan_paid = round(month_loan_paid - month_loan_paid_diff, 5)
                mortgage_paid = True
                left = 0

            rates.append(Rate(i + 1, rate_value, month_interests, month_loan_paid, self.monthly_rate_inc, left))

            if mortgage_paid:
                break

        return rates

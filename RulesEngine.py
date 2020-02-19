import yaml
import csv


class Person:
    def __init__(self, credit_score, state, county):
        self.credit_score = credit_score
        self.state = state
        self.county = county


class Product:
    def __init__(self, name, interest_rate):
        self.name = name
        self.interest_rate = interest_rate
        self.disqualified = False


class RulesEngine:

    def __init__(self, file_name):
        with open(file_name) as file:
            self.rules = yaml.load(file, Loader=yaml.FullLoader)

    def run_rules(self, engine_person, engine_product):
        if engine_person.state in self.rules['disqualifying_states']:
            engine_product.disqualified = True
            engine_product.name = 'Disqualified'
            engine_product.interest_rate = None
            return engine_product

        if engine_person.credit_score >= self.rules['promo_credit_score']:
            engine_product.interest_rate -= float(self.rules['interest_promo_amount'])

        if engine_person.credit_score < self.rules['penalty_credit_score']:
            engine_product.interest_rate += float(self.rules['interest_penalty_amount'])

        if engine_product.name == self.rules['sub_product_name']:
            reduction_factor = 1
            if engine_person.county in self.rules['sub_product_regulated_counties']:
                reduction_factor = 0.5
            engine_product.interest_rate += reduction_factor*(float(self.rules['sub_product_penalty_amount']))

        return engine_product


rules_engine = RulesEngine(r'rules.yaml')

reader = csv.DictReader(
    open("test_data.csv"),
    fieldnames=['credit_score', 'state', 'product_name', 'county', 'expected_result'])

next(reader)

for row in reader:
    person = Person(int(row['credit_score']), row['state'], row['county'])
    product = Product(row['product_name'], 5.0)
    rules_result = rules_engine.run_rules(person, product)
    if rules_result.interest_rate:
        test_passed = rules_result.interest_rate == float(row['expected_result'])
    else:
        test_passed = (not rules_result.interest_rate) and (row['expected_result'] == 'None')
    print("Name: ", rules_result.name, "  Interest Rate: ", rules_result.interest_rate, "   DQ: ",
          rules_result.disqualified, "Test Passed: ", test_passed)

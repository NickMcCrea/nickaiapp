import random
from datetime import datetime, timedelta

class ProductGenerator:
    def __init__(self):
        self.products = [
      ('Fixed Income', 'Bond', 'Exchange Traded', 'Futures Contract', 'Credit Risk', (365*3, 365*30)),
    ('Equity', 'Stock', 'OTC', 'Options Contract', 'Market Risk', (1, 365*3)),
    ('Derivative', 'Future', 'Exchange Traded', 'Futures Contract', 'Market Risk', (30, 365)),
    ('Derivative', 'Option', 'OTC', 'Options Contract', 'Operational Risk', (30, 365*3)),
    ('Fixed Income', 'Bond', 'Exchange Traded', 'Futures Contract', 'Credit Risk', (365*3, 365*30)),
    ('Fixed Income', 'MBS', 'Private Placement', 'Forwards Contract', 'Liquidity Risk', (365*10, 365*30)),
    ('Derivative', 'Swap', 'OTC', 'Swap Contract', 'Interest Rate Risk', (365, 365*30)),
    ('Equity', 'Stock', 'Public Market', 'Options Contract', 'Equity Risk', (1, 365*3)),
    ('Commodity', 'Future', 'Commodities Market', 'Futures Contract', 'Commodity Risk', (30, 365)),
    ('Currency', 'Future', 'Forex Market', 'Futures Contract', 'Foreign Exchange Risk', (30, 365)),
    ('Real Estate', 'REIT', 'Public Market', 'Forwards Contract', 'Real Estate Risk', (1, 365*3)),
    ('Fixed Income', 'Bond', 'Fixed Income Market', 'Futures Contract', 'Interest Rate Risk', (365*3, 365*30)),
    ('Equity', 'ETF', 'Exchange Traded', 'Options Contract', 'Market Risk', (1, 365*3)),
    ('Equity', 'Mutual Fund', 'Public Market', 'Forwards Contract', 'Market Risk', (1, 365*3)),
    ('Derivative', 'Warrant', 'OTC', 'Options Contract', 'Operational Risk', (30, 365)),
    ('Fixed Income', 'CDO', 'Private Placement', 'Forwards Contract', 'Credit Risk', (365*5, 365*10)),
        ]

    def get_random_product(self):
        product = random.choice(self.products)
        product_type, instrument_type, market_type, contract_type, risk_type, (min_maturity, max_maturity) = product

        start_date = datetime.now() - timedelta(days=random.randint(0, 365))
        maturity_date = start_date + timedelta(days=random.randint(min_maturity, max_maturity))
        
        return product_type, instrument_type, market_type, contract_type, risk_type, start_date, maturity_date

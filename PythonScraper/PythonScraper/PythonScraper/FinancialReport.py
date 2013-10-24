class FinancialReport:
    DEFAULT_VALUE = -0.000000000000000001

    def __init__(self):
    	self.date = ''
    	self.report_type = ''
    	self.revenue_from_sale_of_merchandise_and_raw_materials = self.DEFAULT_VALUE
    	self.profit_from_operating_activities = self.DEFAULT_VALUE
    	self.gross_profit = self.DEFAULT_VALUE
    	self.net_profit = self.DEFAULT_VALUE
    	self.net_flow = self.DEFAULT_VALUE
    	self.net_operating_flow = self.DEFAULT_VALUE
    	self.net_investments_flow = self.DEFAULT_VALUE
    	self.net_financial_flow = self.DEFAULT_VALUE
    	self.assets = self.DEFAULT_VALUE
    	self.liabilities_and_provision_for_liabilities = self.DEFAULT_VALUE
    	self.non_current_liabilities = self.DEFAULT_VALUE
    	self.current_liabilities = self.DEFAULT_VALUE
    	self.owners_equity = self.DEFAULT_VALUE
    	self.share_capital = self.DEFAULT_VALUE
    	self.number_of_shares = self.DEFAULT_VALUE
    	self.book_worth_per_share = self.DEFAULT_VALUE
    	self.profit_per_share = self.DEFAULT_VALUE
    	self.diluted_number_of_shares = self.DEFAULT_VALUE
    	self.diluted_book_worth_per_share = self.DEFAULT_VALUE
    	self.diluted_profit_per_share = self.DEFAULT_VALUE
    	self.dividend_per_share = self.DEFAULT_VALUE
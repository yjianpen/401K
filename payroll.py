default_taxpayer_status ={"Marriage":"Single","Resident":"True","Child_num":"0"}

class tax_flat:
	def __init__(self,tax_rate,name):
		self.tax_rate = tax_rate
		self.name = name

	def CountTax(self,income):
		tax_rate = self.tax_rate
		taxable_income = income
		tax_paid = taxable_income * tax_rate
		print("Total " +self.name +" paid: ",tax_paid, " Overall " + self.name +" rate: ",tax_rate)
		return tax_paid

class tax_cumulative:
	def __init__(self,brackets,name):
		## brackets: an array of
		## sample brackets: {(0,1000):0.15,(1000,2000):0.3,(2000,inf):0.4}
		## sort brackets by the first element of each interval 

		self.brackets = {income:tax_rate for income, tax_rate in sorted(brackets.items(), key=lambda item: item[0][0])}
		self.name = name
		if list(self.brackets.keys())[-1][-1]!=float('inf'):
			raise ValueError("Invalid brackets! Missing INF point!")
		if list(self.brackets.keys())[0][0]!=0:
			raise ValueError("Invalid brackets! The first left interval should be zero!")
		

	def CountTax(self,income):
		taxable_income = income
		tax_paid = 0
		brackets = self.brackets
		if income ==0:
			print("Total" +self.name +" paid",0, "Overall tax rate",None)
			return 0
		for tax_interval in brackets.keys():
			
			tax_rate = brackets[tax_interval]

			if taxable_income <= tax_interval[1]:
				tax_paid += (taxable_income - tax_interval[0]) * tax_rate
				print("Total " +self.name +" paid: ",tax_paid, " Overall " + self.name +" rate: ",tax_paid/income)
				return tax_paid
			else:
				tax_paid += (tax_interval[1] - tax_interval[0]) * tax_rate
'''			
class tax_submit_query:
	def __init__(self,taxable_income,State_tax,Federal_tax,Fica_tax):
		self.taxable_income = taxable_income
		self.State_tax = State_tax
		self.Federal_tax = Federal_tax
		self.Fica_tax = Fica_tax

	def CountTotalTax(self):
		total_tax = self.State_tax.CountTax(self.taxable_income) + self.Federal_tax.CountTax(self.taxable_income) + Fica_tax.CountTax(self.taxable_income)
		print("Total paid tax: ",total_tax,"Total overall rate: ",total_tax/self.taxable_income)
		return total_tax 
'''
class pretax_account:
	def __init__(self,balance = 0):
		self.balance = balance
		self.name = "pretax"

	def deposit(self,deposit_amount):
		self.balance += deposit_amount

	def withdrawl(self,withdrawl_amount):
		if withdrawl_amount > self.balance:
			raise ValueError("Insuffientt balance to withdrawl")
		self.balance -= withdrawl_amount

class roth_account:
	def __init__(self,balance = 0):
		self.balance = balance
		self.name = "roth"

	def deposit(self,deposit_amount):
		self.balance += deposit_amount

	def withdrawl(self,withdrawl_amount):
		if withdrawl_amount > self.balance:
			raise ValueError("Insuffientt balance to withdrawl")
		self.balance -= withdrawl_amount

class four_zero_oneK:
	## param contribution: total contribution to four_zero_oneK in USD
	## distribution: ratios in pre-tax and roth accounts
	def __init__(self,contribution,distribution):
		self.distribution = distribution
		self.pretax_acc = pretax_account(distribution["pretax"]*contribution)
		self.pretax_acc = pretax_account(distribution["pretax"]*contribution)
	## To be continued

class taxpayer:
	## status: a bunch of status such as immigration and marriage status
	def __init__(self,name,status=default_taxpayer_status,salary=0,bonus=0):
		self.status = status
		self.name = name
		self.taxable_income = 0
		self.bonus = 0
		self.salary = salary

	def add_total_income(self,income):
		self.taxable_income += income

	def BaseSalaryTax(self,State_tax,Federal_tax,Fica_tax):
		tax_paid = 0
		if self.status["Resident"] == "True":
			tax_paid+=Fica_tax.CountTax(self.taxable_income)

		tax_paid+=State_tax.CountTax(self.taxable_income)

		tax_paid+=Federal_tax.CountTax(self.taxable_income)

		print("Base salary paid tax: ",tax_paid,"Base salary tax rate: ",tax_paid/self.taxable_income)

		return tax_paid

	def BonusTax(self):
		'''
		To be continued
		'''
		return

	def deposit401K(self):
		'''
		To be continued
		'''
		return


Federal_income_tax = tax_cumulative({(0,9950):0.1,(9951,40525):0.12,(40526,86375):0.22,(86376,164925):0.24,(164926,209425):0.32,(209416,523600):0.35,(523601,float('inf')):0.37},"Fed base salary tax")
Ca_income_tax= tax_cumulative({(0,9325):0.01,(9326,22107):0.02,(22108,34892):0.04,(34893,48435):0.06,(48436,61214):0.08,(61215,212686):0.093,(312687,375221):0.103,(375222,625369):0.113,(625370,float('inf')):0.123},"Ca base salary tax")
Fica_income_tax = tax_flat(0.0765,"FICA base salary tax")
taxpayer1 = taxpayer("Gavin")
taxpayer1.add_total_income(152000)
taxpayer1.BaseSalaryTax(Federal_income_tax,Ca_income_tax,Fica_income_tax)
##print(Federal_tax.CountTax(200000))
##print(Ca_tax.CountTax(200000))
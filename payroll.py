default_taxpayer_status ={"Marriage":"Single","Resident":"True","Child_num":"0"}
class tax_combined:
	def __init__(self,taxes):
		self.taxes = taxes

	def CountTax(self,income):
		tax_paid = 0
		for tax in self.taxes:
			tax_paid += tax.CountTax(income)
		return tax_paid

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
	def __init__(self,contribution,pretax_part,roth_part):
		if abs(pretax_part + roth_part - contribution)>1:
			raise ValueError("Roth balance and pretax balance do not add up to total contribution")
		self.pretax_acc = pretax_account(pretax_part)
		self.roth_acc = roth_account(roth_part)


	## To be continued

class taxpayer:
	## status: a bunch of status such as immigration and marriage status
	def __init__(self,name,status=default_taxpayer_status,salary=0,bonus=0):
		self.status = status
		self.name = name
		self.salary = 0
		self.bonus = 0
		self.total_income = 0


	def add_salary(self,income):
		self.salary += income
		self.total_income += income

	def add_bonus(self,income):
		self.bonus += income
		self.total_income += income
	def BaseSalaryTax(self,State_tax,Federal_tax,Fica_tax):
		tax_paid = 0
		if self.status["Resident"] == "True":
			tax_paid+=Fica_tax.CountTax(self.salary)

		tax_paid+=State_tax.CountTax(self.salary)

		tax_paid+=Federal_tax.CountTax(self.salary)

		print("Base salary paid tax: ",tax_paid,"Base salary tax rate: ",tax_paid/self.salary)

		return tax_paid


	def BonusTax(self,State_tax,Federal_tax,Fica_tax):
		tax_paid = 0
		if self.status["Resident"] == "True":
			tax_paid+=Fica_tax.CountTax(self.bonus)

		tax_paid+=State_tax.CountTax(self.bonus)

		tax_paid+=Federal_tax.CountTax(self.bonus)

		print("Bonus paid tax: ",tax_paid,"Base bonus tax rate: ",tax_paid/self.bonus)

		return tax_paid

	def CountTax(self,State_salary_tax,Federal_salary_tax,Fica_tax,State_bonus_tax,Federal_bonus_tax):
		tax_paid = 0
		tax_paid += self.BaseSalaryTax(State_salary_tax,Federal_salary_tax,Fica_tax)
		tax_paid += self.BonusTax(State_bonus_tax,Federal_bonus_tax,Fica_tax)
		print("Overall paid tax: ",tax_paid,"Overall tax rate: ",tax_paid/(self.salary+self.bonus))
		return tax_paid


	def deposit401K(self,from_account,to_account):
		'''
		To be continued
		'''
		valid_from_accounts = ["salary","bonus"]
		valid_to_accounts = ["pretax","roth"]
		if from_account not in valid_from_accounts:
			raise ValueError("from_account must be listed here: ",valid_from_account)
		if to_account not in valid_to_accounts:
			raise ValueError("to_account must be listed here: ",valid_to_account)

		return
Federal_bonus_tax=tax_cumulative({(0,100000):0.22,(100000,float('inf')):0.37},"Federal_bonus_tax")
Ca_bonus_tax=tax_flat(0.1023,"Ca_bonus_tax")
Wa_income_tax= tax_cumulative({(0,float('inf')):0},"Wa base salary tax")
SS_income_tax = tax_cumulative({(0,147000):0.062,(147001,float('inf')):0},"Social Security base salary tax")
Medicare_income_tax = tax_cumulative({(0,200000):0.0145,(200001,float('inf')):0.009},"Medicare base salary tax")
Federal_income_tax = tax_cumulative({(0,9950):0.1,(9951,40525):0.12,(40526,86375):0.22,(86376,164925):0.24,(164926,209425):0.32,(209416,523600):0.35,(523601,float('inf')):0.37},"Fed base salary tax")
Ca_income_tax= tax_cumulative({(0,9325):0.01,(9326,22107):0.02,(22108,34892):0.04,(34893,48435):0.06,(48436,61214):0.08,(61215,212686):0.093,(312687,375221):0.103,(375222,625369):0.113,(625370,float('inf')):0.123},"Ca base salary tax")
Fica_income_tax = tax_combined([SS_income_tax,Medicare_income_tax])
taxpayer1 = taxpayer("Gavin")
taxpayer1.add_salary(552000)
taxpayer1.add_bonus(101000)
taxpayer1.CountTax(Federal_income_tax,Ca_income_tax,Fica_income_tax,Ca_bonus_tax,Federal_bonus_tax)
##print(Federal_tax.CountTax(200000))
##print(Ca_tax.CountTax(200000))
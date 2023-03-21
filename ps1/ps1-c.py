# User input
annual_salary = float(input('Enter the starting salary: ' ))

# Given sets of assumption
month_salary = annual_salary/12
total_cost = 1000000
semi_annual_raise = 0.07
portion_down_payment = 0.25
current_savings = 0
investment_return = 0.04   # Annual investment interest rate of current savings 
down_payment = portion_down_payment * total_cost

#bisection search
steps = 0
low = 0
high = 10000
tolerance = down_payment/1000
guess = (low + high)//2.0

#calculating the max saving needed
def calcSavings(current_savings, month_salary, guess):   
    for month in range(36):
        if month % 6 == 0 and month > 0:
            month_salary = month_salary*(1+semi_annual_raise)
        current_savings = current_savings + month_salary*guess
    current_savings = current_savings * (1+0.04)
    return(current_savings)

#While loop in which the bisection works
while abs(down_payment - current_savings) >= 100:#less than 100 to make it easier
     
    current_savings = calcSavings(current_savings,month_salary,guess)
    
    if current_savings < down_payment:
        low = guess
        current_savings = 0 # reseting the value for each interation
    elif current_savings > down_payment + tolerance:
        high = guess
        current_savings = 0 #reseting the value for each interation
    if steps > 100:
        print("It's not possible to make the down payment in three years")
        exit()
    guess = (low+high)/2
    steps = steps +1
    
# simple else/if, wich determine if it's possible to make the downpayment in 3 years   
final_guess = round(guess,4)
if final_guess > 1:
    print("It is not possible to pay the down payment in three years")
else:    
    print("Best saving rate: ", final_guess)
    print("Steps in bisection search", steps)


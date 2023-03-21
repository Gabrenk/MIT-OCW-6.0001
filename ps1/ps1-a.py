def Main():
    total_cost = float(input("The total cost of your dream house: "))
    annual_salary = float(input("Your annual starting salary: "))
    portion_saved = float(input("The portion of your salary to be saved: "))
    
    annual_return = 0.04
    monthly_salary = annual_salary / 12
    portion_down_payment = total_cost/4 
    month_count = 0
    current_savings = 0.0

    while current_savings < portion_down_payment:
        month_count += 1
        current_savings += portion_saved*monthly_salary + current_savings*annual_return/12
        
    
    print(month_count)
Main()
    
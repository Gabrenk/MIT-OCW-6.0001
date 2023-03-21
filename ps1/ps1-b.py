def Main():
    total_cost = float(input("The total cost of your dream house: "))
    annual_salary = float(input("Your annual starting salary: "))
    portion_saved = float(input("The portion of your salary to be saved: "))
    semi_annual_raise = float(input("Enter your annual salary raise, as a decimal percentage"))
    
    annual_return = 0.04
    monthly_salary = annual_salary / 12
    portion_down_payment = total_cost/4 
    month_count = 0
    current_savings = 0.0

    while current_savings < portion_down_payment:
        month_count += 1
        current_savings += portion_saved*monthly_salary + current_savings*annual_return/12
        
        if month_count % 6 == 0:
            monthly_salary += semi_annual_raise*monthly_salary
            
    
    print("Number of months: ", month_count)
Main()



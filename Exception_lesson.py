total_sales = {"John_Doe" : ['three',4,3,2], "Jane_Doe" : [1,6,3,9], "Joe_Doe" : [5,7,2,"X"], "Jill_Doe" : [5,9,-55, 7]}


def yearly_total(list):
    try:
        result = sum(list)
        if result < 0:
            raise Exception("Verify Data.  Total sales should not be negative")
        return result
    except TypeError:
        return f"Error, Unable to total {list}"   



John_Doe_total = yearly_total(total_sales["John_Doe"])
Jane_Doe_total = yearly_total(total_sales["Jane_Doe"])
Joe_Doe_total = yearly_total(total_sales["Joe_Doe"])
Jill_Doe_total = yearly_total(total_sales["Jill_Doe"])



print("John's Total",John_Doe_total)
print("Jane's Total",Jane_Doe_total)
print("Joe's Total", Joe_Doe_total)    
print("Jill's Total", Jill_Doe_total)

#add
#fancycode2

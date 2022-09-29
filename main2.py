from amortization.amount import calculate_amortization_amount
from amortization.period import calculate_amortization_period
from amortization.schedule import amortization_schedule
from tabulate import tabulate


amount = calculate_amortization_amount(100000, 0.07, 300)

period = calculate_amortization_period(100000, 0.07, 706.78)



#print(amount)
def get_data_table(df):
    column_data = list(df.columns)
    row_data = df.to_records(index=False)
    print("row data", row_data, "col data", column_data)
    return column_data, row_data


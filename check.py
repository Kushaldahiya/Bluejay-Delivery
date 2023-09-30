import pandas as pd

def analyze_employee_shifts(input_file):
    df = pd.read_excel(input_file) 

    employee_records = {}
    consecutive_days_threshold = 7
    max_single_shift_hours = 14
    min_shift_gap_hours = 1
    max_shift_gap_hours = 10

    for index, row in df.iterrows():
        name = row['Employee Name']
        position = row['Position ID']
        time_in_str = row['Time']
        time_out_str = row['Time Out']

        try:
         
            time_in = pd.to_datetime(time_in_str, errors='coerce')
            time_out = pd.to_datetime(time_out_str, errors='coerce')

            if not pd.isna(time_in) and not pd.isna(time_out):
         
                shift_duration_hours = (time_out - time_in).total_seconds() / 3600
                #condition c
                if shift_duration_hours > max_single_shift_hours:
                    print(f"Employee: {name}, Position: {position}, Worked for more than 14 hours in a shift")

               #consecutive days check
                if name not in employee_records:
                    employee_records[name] = {'last_date': None, 'last_time_out': None, 'consecutive_days': 0}
                #condition b
                if not pd.isna(time_in):
                    date = time_in.date()
                    if date == employee_records[name]['last_date']:
                      
                        time_between_shifts_hours = (time_in - employee_records[name]['last_time_out']).total_seconds() / 3600
                        if min_shift_gap_hours < time_between_shifts_hours < max_shift_gap_hours:
                            print(f"Employee: {name}, Position: {position}, Less than 10 hours between shifts")

                        employee_records[name]['consecutive_days'] += 1
                    else:
                        employee_records[name]['consecutive_days'] = 1
                    employee_records[name]['last_date'] = date
                #condition a
                if employee_records[name]['consecutive_days'] >= consecutive_days_threshold:
                    print(f"Employee: {name}, Position: {position}, Worked for 7 consecutive days")

                if not pd.isna(time_out):
                    employee_records[name]['last_time_out'] = time_out

        except ValueError: #in this I handle error passing
            continue

if __name__ == "__main__":
    input_file = "Book1.xlsx"  
    analyze_employee_shifts(input_file)

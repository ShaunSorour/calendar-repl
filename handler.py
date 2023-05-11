import json
from datetime import datetime, timedelta


def calendar_generator(event, context):
    try:
        year = int(event['pathParameters']['year'])
        calendar = retail_calendar(year)
        response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(calendar, indent=4)
        }
    except:
        response = {
            'statusCode': 400,
            'body': f"Error in year format: {event['pathParameters'].get('year', 'Unknown')}"
        }

    return response


def retail_calendar(year):
    month_days = [
        ("Feb", 28),
        ("Mar", 28),
        ("Apr", 35),
        ("May", 28),
        ("Jun", 28),
        ("Jul", 35),
        ("Aug", 28),
        ("Sep", 28),
        ("Oct", 35),
        ("Nov", 28),
        ("Dec", 28),
        ("Jan", 35)
    ]
    
    calendar = {
        "FiscalYear": year,
        "Months": []
    }
    # using the start of 2022 retail year as a reference
    base_date = datetime(2021, 1, 30)
    days = 2022 - year

    # SET START
    start_date = base_date + timedelta(days=days)
    start_date = start_date.replace(year=year-1)

    for month_name, month_length in month_days: 
        # assuming every 5 years to add extra week
        month_length = check_53_week(year, month_name, month_length)  
        fiscal_month = {
            "FiscalMonth": month_name,
            "NumberOfWeeks": month_length // 7,
            "Weeks": []
        }
        # calculate weeks for the month
        week_number = 1
        for _ in range(fiscal_month["NumberOfWeeks"]):
            week = {
                "WeekNumber": week_number,
                "Days": []
            }
            # calculate days for the week
            for _ in range(7):
                day_str = start_date.strftime("%d/%m/%Y")
                week["Days"].append(day_str)
                if (day_str == "31/01/" + str(year-1)):
                    start_date = start_date.replace(year=year)
                if (day_str == "31/12/" + str(year)):
                    start_date = start_date.replace(year=year-1)
                start_date += timedelta(days=1)

            fiscal_month["Weeks"].append(week)
            week_number += 1

        calendar["Months"].append(fiscal_month)

    return calendar   


def check_53_week(year, month, days):
    # assuming extra week falls in Jan
    if month == "Jan" and year % 5 == 0:
        days = 42

    return days
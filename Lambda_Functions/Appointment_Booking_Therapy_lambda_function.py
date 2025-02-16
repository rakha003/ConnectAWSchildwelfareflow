import boto3
import json
from datetime import datetime
from zoneinfo import ZoneInfo 

# AWS Resources
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Appointments")

MST = ZoneInfo("America/Denver")

def lambda_handler(event, context):
    slots = event.get("Details", {}).get("Parameters", {})

    appointment_date = slots.get("appointmentDate")  # YYYY-MM-DD
    appointment_time = slots.get("appointmentTime")  # HH:MM (24-hour format)
    phone_number = slots.get("phoneNumber")

    if not appointment_date or not appointment_time or not phone_number:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing parameters"})}

    # Convert time to MST
    try:
        time_obj = datetime.strptime(appointment_time, "%H:%M")
        appointment_time_12hr = time_obj.strftime("%I:%M %p")  # Convert to 12-hour format
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid time format"})}

    # Check if time is within working hours (8 AM - 5 PM MST)
    if not (8 <= time_obj.hour < 17):  # 17 = 5 PM (exclusive)
        return {
            "statusCode": 410,
            "body": json.dumps({
                "status": "unavailable",
                "message": "Appointments can only be booked between 8 AM and 5 PM MST."
            })
        }

    # Check availability
    response = table.get_item(Key={"date": appointment_date, "time": appointment_time_12hr})
    if "Item" in response:
        return {"statusCode": 409, "body": json.dumps({"status": "booked"})}

    # Book appointment
    table.put_item(Item={
        "date": appointment_date,
        "time": appointment_time_12hr,
        "phone": phone_number,
        "status": "booked",
        "created_at": datetime.now(MST).isoformat(),
        "updated_at": datetime.now(MST).isoformat()
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "available",
            "message": "Appointment booked successfully."
        })
    }

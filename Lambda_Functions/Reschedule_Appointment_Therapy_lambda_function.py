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

    old_date = slots.get("oldDate")  # YYYY-MM-DD
    old_time = slots.get("oldTime")  # HH:MM (24-hour format)
    new_date = slots.get("apptDate")  # YYYY-MM-DD
    new_time = slots.get("apptTime")  # HH:MM (24-hour format)
    phone_number = slots.get("phoneNumber")

    if not old_date or not old_time or not new_date or not new_time or not phone_number:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing parameters"})}

    # Convert old time to MST
    try:
        old_time_obj = datetime.strptime(old_time, "%H:%M").replace(tzinfo=MST)
        old_time_12hr = old_time_obj.strftime("%I:%M %p")  # Convert to 12-hour format
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid old time format"})}

    # Convert new time to MST
    try:
        new_time_obj = datetime.strptime(new_time, "%H:%M").replace(tzinfo=MST)
        new_time_12hr = new_time_obj.strftime("%I:%M %p")  # Convert to 12-hour format
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid new time format"})}

    # Check if new appointment time is within working hours (8 AM - 5 PM MST)
    if not (8 <= new_time_obj.hour < 17):  # 17 = 5 PM (exclusive)
        return {
            "statusCode": 410,
            "body": json.dumps({
                "status": "unavailable",
                "message": "Appointments can only be scheduled between 8 AM and 5 PM MST."
            })
        }

    # Check if the old appointment exists
    response = table.get_item(Key={"date": old_date, "time": old_time_12hr})
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Old appointment not found"})}

    # Check if the new appointment slot is available
    response = table.get_item(Key={"date": new_date, "time": new_time_12hr})
    if "Item" in response:
        return {"statusCode": 409, "body": json.dumps({"status": "new slot booked"})}

    # Delete old appointment
    table.delete_item(Key={"date": old_date, "time": old_time_12hr})

    # Book new appointment
    table.put_item(Item={
        "date": new_date,
        "time": new_time_12hr,
        "phone": phone_number,
        "status": "booked",
        "created_at": datetime.now(MST).isoformat(),
        "updated_at": datetime.now(MST).isoformat()
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "rescheduled",
            "message": "Appointment rescheduled successfully."
        })
    }

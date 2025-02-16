import boto3
import json
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

# AWS Resources
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Appointments")

MST = ZoneInfo("America/Denver")

def lambda_handler(event, context):
    slots = event.get("Details", {}).get("Parameters", {})
    
    old_date = slots.get("oldDate")  # YYYY-MM-DD
    old_time = slots.get("oldTime")  # HH:MM (24-hour format)

    if not old_date or not old_time:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing parameters: oldDate and oldTime are required"})}

    # Convert old time to MST
    try:
        old_time_obj = datetime.strptime(old_time, "%H:%M")
        old_time = old_time_obj.strftime("%I:%M %p")  # Convert to 12-hour format
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid old time format"})}

    # Check if the appointment exists
    response = table.get_item(Key={"date": old_date, "time": old_time})
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Appointment not found"})}

    # Delete the appointment
    table.delete_item(Key={"date": old_date, "time": old_time})

    return {"statusCode": 200, "body": json.dumps({"status": "cancelled", "message": "Appointment successfully cancelled."})}
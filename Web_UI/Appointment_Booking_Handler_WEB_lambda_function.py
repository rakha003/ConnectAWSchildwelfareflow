import json
import boto3
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChildWelfareAppointments")

# Initialize Amazon SES
ses = boto3.client('ses', region_name="us-west-2")

def lambda_handler(event, context):
    try:
        # Check if body exists in the event
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Request body is missing"})
            }

        # Extract request body and parse JSON
        body = json.loads(event['body'])

        # Extract parameters (Ensure keys match request)
        appointment_id = body.get('appointment_id')
        user_name = body.get('user_name')
        appointment_date = body.get('appointment_date')
        appointment_time = body.get('appointment_time')
        reason = body.get('reason')

        # Validate required fields
        if not appointment_id or not user_name or not appointment_date or not appointment_time or not reason:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"})
            }

        # Store in DynamoDB
        table.put_item(Item={
            "appointment_id": appointment_id,
            "user_name": user_name,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "reason": reason,
            "status": "Scheduled",
            "created_at": str(datetime.utcnow())
        })

        # Send confirmation email via Amazon SES
        ses.send_email(
            Source="99.rakhachandre@gmail.com",
            Destination={"ToAddresses": ["99.rakhachandre@gmail.com"]},
            Message={
                "Subject": {"Data": "Appointment Confirmation"},
                "Body": {"Text": {"Data": f"Hello {user_name}, your appointment is confirmed on {appointment_date} at {appointment_time}."}}
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Appointment Created Successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

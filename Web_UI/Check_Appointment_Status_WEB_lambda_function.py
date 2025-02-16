import json
import boto3

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ChildWelfareAppointments")

def lambda_handler(event, context):
    try:
        # Ensure pathParameters exist
        if "pathParameters" not in event or "appointment_id" not in event["pathParameters"]:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing appointment ID"})
            }

        # Extract appointment ID
        appointment_id = event["pathParameters"]["appointment_id"]

        # Fetch appointment from DynamoDB
        response = table.get_item(Key={"appointment_id": appointment_id})

        # Check if item exists
        if "Item" not in response:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Appointment not found"})
            }

        # Return appointment details
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(response["Item"])
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }

import datetime
import boto3

# Define MST timezone offset (-7:00 without daylight savings, -6:00 with DST)
MST_OFFSET = datetime.timedelta(hours=-7)  # Adjust as necessary timings

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Holidays')  

def lambda_handler(event, context):
    try:
        # Get current UTC time and convert to MST
        now_utc = datetime.datetime.utcnow()
        now_mst = now_utc + MST_OFFSET
        today_mst = now_mst.strftime('%Y-%m-%d')

        # Querying DynamoDB for today's date
        response = table.get_item(Key={'date': today_mst})

        if 'Item' in response:
            return {
                "isHoliday": "true",
                "holidayName": response['Item'].get('holidayName', 'Unknown Holiday')
            }
        else:
            return {
                "isHoliday": "false",
                "holidayName": "None"
            }

    except Exception as e:
        return {"isHoliday": "false", "holidayName": f"Error - {str(e)}"}

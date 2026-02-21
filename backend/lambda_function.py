import json
import boto3
from decimal import Decimal
import os

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLENAME', 'VisitorCounter')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    Lambda function to track and return visitor count
    
    This function:
    1. Increments the visitor count in DynamoDB
    2. Returns the updated count
    3. Handles CORS headers for web requests
    """
    
    try:
        # Update visitor count atomically
        response = table.update_item(
            Key={
                'id': 'visitor-count'
            },
            UpdateExpression='SET visit_count = if_not_exists(visit_count, :start) + :inc',
            ExpressionAttributeValues={
                ':inc': 1,
                ':start': 0
            },
            ReturnValues='UPDATED_NEW'
        )
        
        # Extract the updated count
        count = int(response['Attributes']['visit_count'])
        
        # Return successful response with CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'count': count,
                'message': 'Visitor count updated successfully'
            })
        }
        
    except Exception as e:
        print(f"Error updating visitor count: {str(e)}")
        
        # Return error response with CORS headers
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Failed to update visitor count',
                'message': str(e)
            })
        }

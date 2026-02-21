import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'prod-VisitorCounter')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    
    # Handle OPTIONS preflight request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': ''
        }
    
    try:
        # Get current count from DynamoDB
        response = table.get_item(Key={'id': 'visitor_count'})
        
        if 'Item' in response:
            current_count = int(response['Item']['count'])
            new_count = current_count + 1
        else:
            new_count = 1
        
        # Update DynamoDB with new count
        table.put_item(
            Item={
                'id': 'visitor_count',
                'count': new_count
            }
        )
        
        # Return response with CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'count': new_count,
                'message': 'Visitor count updated successfully'
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

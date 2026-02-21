import json
import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
import sys
import os

# Add the parent directory to the path so we can import lambda_function
sys.path.insert(0, os.path.dirname(__file__))

# Import the lambda function
from lambda_function import lambda_handler


class TestLambdaFunction:
    """Test suite for the visitor counter Lambda function"""
    
    @patch('lambda_function.table')
    def test_successful_increment(self, mock_table):
        """Test that the counter increments successfully"""
        # Arrange
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': Decimal('42')
            }
        }
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        body = json.loads(response['body'])
        assert body['count'] == 42
        assert 'message' in body
        
        # Verify DynamoDB was called correctly
        mock_table.update_item.assert_called_once()
        call_args = mock_table.update_item.call_args
        assert call_args[1]['Key'] == {'id': 'visitor-count'}
    
    @patch('lambda_function.table')
    def test_first_visitor(self, mock_table):
        """Test the first visitor scenario"""
        # Arrange
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': Decimal('1')
            }
        }
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['count'] == 1
    
    @patch('lambda_function.table')
    def test_large_visitor_count(self, mock_table):
        """Test handling of large visitor counts"""
        # Arrange
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': Decimal('999999')
            }
        }
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['count'] == 999999
    
    @patch('lambda_function.table')
    def test_dynamodb_error(self, mock_table):
        """Test error handling when DynamoDB fails"""
        # Arrange
        mock_table.update_item.side_effect = Exception('DynamoDB connection failed')
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 500
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        body = json.loads(response['body'])
        assert 'error' in body
        assert 'message' in body
    
    @patch('lambda_function.table')
    def test_cors_headers_present(self, mock_table):
        """Test that CORS headers are properly set"""
        # Arrange
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': Decimal('5')
            }
        }
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        headers = response['headers']
        assert headers['Access-Control-Allow-Origin'] == '*'
        assert 'Access-Control-Allow-Headers' in headers
        assert 'Access-Control-Allow-Methods' in headers
        assert headers['Content-Type'] == 'application/json'
    
    @patch('lambda_function.table')
    def test_response_format(self, mock_table):
        """Test that the response format is correct"""
        # Arrange
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': Decimal('10')
            }
        }
        
        event = {}
        context = {}
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert 'statusCode' in response
        assert 'headers' in response
        assert 'body' in response
        
        # Verify body is valid JSON
        body = json.loads(response['body'])
        assert isinstance(body, dict)
        assert 'count' in body
        assert isinstance(body['count'], int)
    
    @patch('lambda_function.table')
    def test_update_expression(self, mock_table):
        """Test that the DynamoDB update expression is correct"""
        # Arrange
        mock_table.update_item.return_value = {
            'Attributes': {
                'visit_count': Decimal('1')
            }
        }
        
        event = {}
        context = {}
        
        # Act
        lambda_handler(event, context)
        
        # Assert
        call_args = mock_table.update_item.call_args[1]
        assert 'UpdateExpression' in call_args
        assert 'if_not_exists' in call_args['UpdateExpression']
        assert call_args['ExpressionAttributeValues'][':inc'] == 1
        assert call_args['ExpressionAttributeValues'][':start'] == 0
        assert call_args['ReturnValues'] == 'UPDATED_NEW'


# Integration test fixture
@pytest.fixture
def lambda_context():
    """Mock Lambda context"""
    class LambdaContext:
        def __init__(self):
            self.function_name = 'visitor-counter'
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:visitor-counter'
            self.aws_request_id = 'test-request-id'
    
    return LambdaContext()


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])

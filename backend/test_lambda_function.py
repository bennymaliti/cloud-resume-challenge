import json
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from lambda_function import lambda_handler


class TestLambdaFunction:
    """Test suite for the visitor counter Lambda function"""
    
    @patch('lambda_function.table')
    def test_first_visitor(self, mock_table):
        """Test when visitor count starts at 0"""
        # Mock DynamoDB response - no existing item
        mock_table.get_item.return_value = {}
        mock_table.put_item.return_value = {}

        # Create test event
        event = {
            'httpMethod': 'POST',
            'path': '/visitor-count'
        }
        context = {}

        # Call Lambda
        response = lambda_handler(event, context)

        # Assertions
        assert response['statusCode'] == 200
        
        body = json.loads(response['body'])
        assert body['count'] == 1
        assert body['message'] == 'Visitor count updated successfully'

        # Verify DynamoDB was called
        mock_table.get_item.assert_called_once_with(Key={'id': 'visitor_count'})
        mock_table.put_item.assert_called_once_with(
            Item={'id': 'visitor_count', 'count': 1}
        )

    @patch('lambda_function.table')
    def test_successful_increment(self, mock_table):
        """Test that the counter increments successfully from 42 to 43"""
        # Mock DynamoDB response - existing count of 42
        mock_table.get_item.return_value = {
            'Item': {
                'id': 'visitor_count',
                'count': 42
            }
        }
        mock_table.put_item.return_value = {}

        event = {'httpMethod': 'POST'}
        context = {}

        response = lambda_handler(event, context)

        # Assertions
        assert response['statusCode'] == 200
        
        body = json.loads(response['body'])
        assert body['count'] == 43  # 42 + 1
        assert body['message'] == 'Visitor count updated successfully'

        # Verify put_item was called with count 43
        mock_table.put_item.assert_called_once_with(
            Item={'id': 'visitor_count', 'count': 43}
        )

    @patch('lambda_function.table')
    def test_large_visitor_count(self, mock_table):
        """Test handling of large visitor counts"""
        # Mock existing count of 999999
        mock_table.get_item.return_value = {
            'Item': {
                'id': 'visitor_count',
                'count': 999999
            }
        }
        mock_table.put_item.return_value = {}

        event = {'httpMethod': 'POST'}
        context = {}

        response = lambda_handler(event, context)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['count'] == 1000000  # 999999 + 1

    @patch('lambda_function.table')
    def test_dynamodb_error(self, mock_table):
        """Test error handling when DynamoDB fails"""
        # Mock DynamoDB to raise exception
        mock_table.get_item.side_effect = Exception('DynamoDB connection failed')

        event = {'httpMethod': 'POST'}
        context = {}

        response = lambda_handler(event, context)

        # Should return 500 error
        assert response['statusCode'] == 500
        assert 'Access-Control-Allow-Origin' in response['headers']
        
        body = json.loads(response['body'])
        assert 'error' in body
        assert body['error'] == 'Internal server error'
        assert 'message' in body

    @patch('lambda_function.table')
    def test_cors_headers_present(self, mock_table):
        """Test that CORS headers are properly set"""
        mock_table.get_item.return_value = {
            'Item': {'id': 'visitor_count', 'count': 5}
        }
        mock_table.put_item.return_value = {}

        event = {'httpMethod': 'POST'}
        context = {}

        response = lambda_handler(event, context)

        # Check all required CORS headers
        headers = response['headers']
        assert headers['Access-Control-Allow-Origin'] == '*'
        assert 'Access-Control-Allow-Headers' in headers
        assert 'Access-Control-Allow-Methods' in headers
        assert headers['Content-Type'] == 'application/json'

    def test_options_request(self):
        """Test OPTIONS preflight request for CORS"""
        event = {'httpMethod': 'OPTIONS'}
        context = {}

        response = lambda_handler(event, context)

        # Should return 200 with CORS headers and empty body
        assert response['statusCode'] == 200
        assert response['headers']['Access-Control-Allow-Origin'] == '*'
        assert 'Access-Control-Allow-Methods' in response['headers']
        assert response['body'] == ''

    @patch('lambda_function.table')
    def test_response_format(self, mock_table):
        """Test that the response format is correct"""
        mock_table.get_item.return_value = {
            'Item': {'id': 'visitor_count', 'count': 10}
        }
        mock_table.put_item.return_value = {}

        event = {'httpMethod': 'POST'}
        context = {}

        response = lambda_handler(event, context)

        # Check response structure
        assert 'statusCode' in response
        assert 'headers' in response
        assert 'body' in response
        
        # Verify body is valid JSON
        body = json.loads(response['body'])
        assert isinstance(body, dict)
        assert 'count' in body
        assert 'message' in body
        assert isinstance(body['count'], int)

    @patch('lambda_function.table')
    def test_get_item_called_correctly(self, mock_table):
        """Test that DynamoDB get_item is called with correct key"""
        mock_table.get_item.return_value = {
            'Item': {'id': 'visitor_count', 'count': 7}
        }
        mock_table.put_item.return_value = {}

        event = {'httpMethod': 'POST'}
        context = {}

        lambda_handler(event, context)

        # Verify get_item was called with correct key
        mock_table.get_item.assert_called_once_with(
            Key={'id': 'visitor_count'}
        )

    @patch('lambda_function.table')
    def test_put_item_called_correctly(self, mock_table):
        """Test that DynamoDB put_item is called with correct data"""
        mock_table.get_item.return_value = {
            'Item': {'id': 'visitor_count', 'count': 5}
        }
        mock_table.put_item.return_value = {}

        event = {'httpMethod': 'POST'}
        context = {}

        lambda_handler(event, context)

        # Verify put_item was called with incremented count
        mock_table.put_item.assert_called_once_with(
            Item={'id': 'visitor_count', 'count': 6}
        )


# Integration test fixture (for future use)
@pytest.fixture
def lambda_context():
    """Mock Lambda context"""
    class LambdaContext:
        def __init__(self):
            self.function_name = 'visitor-counter'
            self.memory_limit_in_mb = 128
            self.invoked_function_arn = 'arn:aws:lambda:eu-west-2:123456789012:function:visitor-counter'
            self.aws_request_id = 'test-request-id'
    
    return LambdaContext()


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--cov=lambda_function', '--cov-report=term-missing'])
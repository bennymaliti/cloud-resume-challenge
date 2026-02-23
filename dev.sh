#!/bin/bash

# Cloud Resume Challenge - Local Development Script
# This script helps with local testing and development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    commands=("python3" "pip" "aws")
    
    for cmd in "${commands[@]}"; do
        if command -v $cmd &> /dev/null; then
            print_success "$cmd is installed"
        else
            print_error "$cmd is not installed"
            exit 1
        fi
    done

    # Optional: SAM CLI (can use CloudShell instead)
    if command -v sam &> /dev/null; then
        print_success "SAM CLI is installed"
    else
        print_info "SAM is not installed (use CloudShell for SAM operations)"
    fi
}

# Setup Python virtual environment
setup_venv() {
    print_info "Setting up Python virtual environment..."
    
    if [ ! -d "backend/venv" ]; then
        python3 -m venv backend/venv
        print_success "Virtual environment created"
    else
        print_info "Virtual environment already exists"
    fi
    
    source backend/venv/bin/activate
    pip install -r backend/requirements.txt
    print_success "Dependencies installed"
}

# Run backend tests
run_tests() {
    print_info "Running backend tests..."
    
    cd backend
    source venv/bin/activate
    
    pytest test_lambda_function.py -v --cov=lambda_function --cov-report=term-missing
    
    if [ $? -eq 0 ]; then
        print_success "All tests passed!"
    else
        print_error "Tests failed!"
        exit 1
    fi
    
    cd ..
}

# Build SAM application
build_sam() {
    print_info "Building SAM application..."
    
    cd backend
    sam build
    
    if [ $? -eq 0 ]; then
        print_success "SAM build successful!"
    else
        print_error "SAM build failed!"
        exit 1
    fi
    
    cd ..
}

# Start local API
start_local_api() {
    print_info "Starting local API Gateway and Lambda..."
    print_info "API will be available at http://localhost:3000"
    
    cd backend
    sam local start-api --port 3000
    cd ..
}

# Test local API
test_local_api() {
    print_info "Testing local API..."
    
    response=$(curl -s -X POST http://localhost:3000/visitor-count)
    
    if [[ $response == *"count"* ]]; then
        print_success "Local API is working!"
        echo "Response: $response"
    else
        print_error "Local API test failed!"
        echo "Response: $response"
    fi
}

# Validate SAM template
validate_sam() {
    print_info "Validating SAM template..."
    
    cd backend
    sam validate --lint
    
    if [ $? -eq 0 ]; then
        print_success "SAM template is valid!"
    else
        print_error "SAM template validation failed!"
        exit 1
    fi
    
    cd ..
}

# Deploy to AWS
deploy() {
    print_info "Deploying to AWS..."
    
    cd backend
    sam build
    sam deploy
    
    if [ $? -eq 0 ]; then
        print_success "Deployment successful!"
    else
        print_error "Deployment failed!"
        exit 1
    fi
    
    cd ..
}

# Clean build artifacts
clean() {
    print_info "Cleaning build artifacts..."
    
    rm -rf backend/.aws-sam
    rm -rf backend/venv
    rm -rf backend/__pycache__
    rm -rf backend/.pytest_cache
    rm -rf backend/htmlcov
    rm -rf backend/.coverage
    
    print_success "Cleanup complete!"
}

# Display help
show_help() {
    cat << EOF
Cloud Resume Challenge - Local Development Script

Usage: ./dev.sh [command]

Commands:
    check           Check prerequisites (Python, AWS CLI, SAM)
    setup           Setup virtual environment and install dependencies
    test            Run backend tests with coverage
    build           Build SAM application
    validate        Validate SAM template
    local-api       Start local API Gateway (http://localhost:3000)
    test-api        Test local API endpoint
    deploy          Build and deploy to AWS
    clean           Clean build artifacts
    all             Run all validations and tests
    help            Show this help message

Examples:
    ./dev.sh check          # Check if all tools are installed
    ./dev.sh setup          # Set up development environment
    ./dev.sh test           # Run tests with coverage
    ./dev.sh local-api      # Start local development server
    ./dev.sh deploy         # Deploy to AWS
    ./dev.sh all            # Run full validation suite

Development Workflow:
    1. ./dev.sh setup       # First time setup
    2. ./dev.sh local-api   # Test locally
    3. ./dev.sh test        # Run tests
    4. ./dev.sh deploy      # Deploy to AWS

EOF
}

# Main script logic
case "${1}" in
    check)
        check_prerequisites
        ;;
    setup)
        check_prerequisites
        setup_venv
        ;;
    test)
        run_tests
        ;;
    build)
        build_sam
        ;;
    validate)
        validate_sam
        ;;
    local-api)
        start_local_api
        ;;
    test-api)
        test_local_api
        ;;
    deploy)
        deploy
        ;;
    clean)
        clean
        ;;
    all)
        check_prerequisites
        setup_venv
        validate_sam
        run_tests
        build_sam
        print_success "All validations and tests completed successfully!"
        ;;
    help|*)
        show_help
        ;;
esac
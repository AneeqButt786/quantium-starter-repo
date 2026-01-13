#!/bin/bash

# CI Test Runner Script for Dash App
# This script runs the pytest test suite and exits with appropriate status codes
# Compatible with GitHub Actions, GitLab CI, and other CI/CD platforms

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Return value of a pipeline is the status of the last command to exit with a non-zero status

# Colors for output (optional, for better readability)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_info "Starting test suite execution..."
print_info "Working directory: $SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python is not installed or not in PATH"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

print_info "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version

# Check if virtual environment exists
VENV_DIRS=(".venv" "venv" "env")
VENV_ACTIVATED=false

# Try to activate existing virtual environment
for venv_dir in "${VENV_DIRS[@]}"; do
    if [ -d "$venv_dir" ]; then
        print_info "Found virtual environment: $venv_dir"
        if [ -f "$venv_dir/bin/activate" ]; then
            # Unix/Linux/Mac
            source "$venv_dir/bin/activate"
            VENV_ACTIVATED=true
            print_info "Activated virtual environment: $venv_dir"
            break
        elif [ -f "$venv_dir/Scripts/activate" ]; then
            # Windows (Git Bash, WSL)
            source "$venv_dir/Scripts/activate"
            VENV_ACTIVATED=true
            print_info "Activated virtual environment: $venv_dir"
            break
        fi
    fi
done

# If no virtual environment found, check if we're already in one or use system Python
if [ "$VENV_ACTIVATED" = false ]; then
    if [ -n "$VIRTUAL_ENV" ]; then
        print_info "Already in a virtual environment: $VIRTUAL_ENV"
    else
        print_warning "No virtual environment found. Using system Python."
        print_warning "Consider creating a virtual environment for isolated testing."
    fi
fi

# Verify pytest is installed
if ! $PYTHON_CMD -m pytest --version &> /dev/null; then
    print_error "pytest is not installed. Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        $PYTHON_CMD -m pip install --quiet --upgrade pip
        $PYTHON_CMD -m pip install --quiet -r requirements.txt
    else
        print_error "requirements.txt not found. Cannot install dependencies."
        exit 1
    fi
fi

# Verify test file exists
if [ ! -f "test_app.py" ]; then
    print_error "test_app.py not found in current directory"
    exit 1
fi

# Run the test suite
print_info "Running pytest test suite..."
print_info "Test file: test_app.py"

# Run pytest with verbose output
# Temporarily disable set -e to capture exit code properly
set +e
$PYTHON_CMD -m pytest test_app.py -v --tb=short
TEST_EXIT_CODE=$?
set -e

# Check test results and exit with appropriate status code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    print_info "All tests passed successfully!"
    exit 0
else
    print_error "Tests failed with exit code: $TEST_EXIT_CODE"
    exit 1
fi

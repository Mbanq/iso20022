# ISO20022Gen Tests

This directory contains tests for the ISO20022Gen library.

## Running Tests

You can run the tests using pytest:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with code coverage report
pytest --cov=iso20022gen

# Run specific test file
pytest tests/test_code_generator.py
```

## Test Structure

The tests are organized by module:

- `test_code_generator.py`: Tests for the core ISO 20022 code generation functionality
- `test_fedwire.py`: Tests for the Fedwire envelope wrapping functionality
- `test_cli.py`: Tests for the command-line interface

## Adding Tests

When adding new features to the library, please also add corresponding tests. Each public function or method should have at least one test case.

### Example Test

```python
def test_new_feature():
    # Arrange
    test_input = {"test": "data"}
    
    # Act
    result = my_module.new_feature(test_input)
    
    # Assert
    assert result == expected_result
```

## Mocking

For tests that would normally require external resources (e.g., XSD schema files), use mock objects to simulate the expected behavior. This ensures that tests can run in any environment without requiring additional setup.

```python
from unittest.mock import patch, MagicMock

@patch('module.function_to_mock')
def test_with_mocking(mock_function):
    # Set up the mock
    mock_function.return_value = "mocked result"
    
    # Test code that uses the mocked function
    result = code_that_calls_mocked_function()
    
    # Assert
    assert result == expected_result
``` 
---
name: generate-pytest-suite
description: Standardized generation of unit and integration tests using Pytest, fixtures, mocking, and coverage conventions.
---

# Pytest Test Suite Guidance

When asked to generate unit, integration, or regression tests for Python code:

## 1. Test Organization & Framework Rules
- Use **Pytest** exclusively as the test framework. Do NOT use `unittest.TestCase` unless specifically asked.
- Save tests in the `tests/` directory mirroring the `src/` directory layout (e.g., `src/services/data_service.py` -> `tests/services/test_data_service.py`).
- Name test files starting with `test_` and test functions starting with `test_`.

## 2. Test structure
Structure tests so setup, action, and expected behavior are easy to distinguish. Use comments only when they improve readability; short tests do not need ceremonial section labels.

```python
def test_calculate_discount_valid_input():
    # Arrange
    original_price = 100.0
    discount = 0.20

    # Act
    result = calculate_discount(original_price, discount)

    # Assert
    assert result == 80.0
```

## 3. Fixtures & Mocking
- Use `@pytest.fixture` for reusable test setup/data instead of inline duplicates.
- Use `unittest.mock` (`MagicMock`, `patch`) or `pytest-mock` (`mocker` fixture) for all external network, database, or API calls. Never execute real API queries in unit tests.
- Wrap external cloud calls (e.g., GCP services, AWS, external endpoints) in mocks.

## 4. Behavior and edge cases
Cover the important supported behavior and relevant boundaries for the change. Test exceptions with `pytest.raises()` when raising is part of the contract. Do not invent exception cases for functions that have no meaningful exceptional behavior.

```python
import pytest

def test_process_data_raises_value_error_on_empty():
    # Arrange
    invalid_input = None

    # Act & Assert
    with pytest.raises(ValueError, match="Input data cannot be None"):
        process_data(invalid_input)
```

## 5. Parametrized testing
Use `@pytest.mark.parametrize` when several inputs exercise the same behavior and a parameter table is clearer than duplicated tests:

```python
@pytest.mark.parametrize("price, discount, expected", [
    (100.0, 0.1, 90.0),
    (50.0, 0.0, 50.0),
    (200.0, 0.5, 100.0),
])
def test_calculate_discount_parametrized(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

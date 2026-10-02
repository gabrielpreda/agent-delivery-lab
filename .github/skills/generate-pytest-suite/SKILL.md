---
name: generate-pytest-suite
description: Standardized generation of unit and integration tests using Pytest, fixtures, mocking, and coverage conventions.
---

# Pytest Test Suite Generation Standards

When asked to generate unit, integration, or regression tests for Python code:

## 1. Test Organization & Framework Rules
- Use **Pytest** exclusively as the test framework. Do NOT use `unittest.TestCase` unless specifically asked.
- Save tests in the `tests/` directory mirroring the `src/` directory layout (e.g., `src/services/data_service.py` -> `tests/services/test_data_service.py`).
- Name test files starting with `test_` and test functions starting with `test_`.

## 2. Test Structure (AAA Pattern)
Every generated test function must follow the **Arrange-Act-Assert** pattern, separated by comments:

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

## 4. Edge Cases & Exception Testing
For every function tested, include at least:
1. One **Happy Path** test.
2. One **Edge Case** test (empty list, `None` values, boundary numbers).
3. One **Exception Handling** test using `pytest.raises()`:

```python
import pytest

def test_process_data_raises_value_error_on_empty():
    # Arrange
    invalid_input = None

    # Act & Assert
    with pytest.raises(ValueError, match="Input data cannot be None"):
        process_data(invalid_input)
```

## 5. Parametrized Testing
Use `@pytest.mark.parametrize` when testing a function with multiple input-output variations:

```python
@pytest.mark.parametrize("price, discount, expected", [
    (100.0, 0.1, 90.0),
    (50.0, 0.0, 50.0),
    (200.0, 0.5, 100.0),
])
def test_calculate_discount_parametrized(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```
# Test Suite

This directory contains comprehensive tests for the Dr. Jart+ Campaign Generation Pipeline.

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_phase1_sourcing.py
```

### Run specific test class
```bash
pytest tests/test_phase1_sourcing.py::TestSearchSerper
```

### Run specific test
```bash
pytest tests/test_phase1_sourcing.py::TestSearchSerper::test_search_serper_success
```

### Run with coverage
```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
```

## Test Structure

### Unit Tests
- **test_phase1_sourcing.py** — Tests for trend sourcing (search, filtering, synthesis)
- **test_phase2_processing.py** — Tests for asset generation (chains, parallel execution)
- **test_phase3_scoring.py** — Tests for scoring and regeneration loop
- **test_phase4_packaging.py** — Tests for final bundling and output
- **test_models.py** — Tests for Pydantic model validation

### Integration Tests
- **test_graph.py** — Tests for pipeline orchestration and node execution

## Key Test Fixtures (conftest.py)

All fixtures are defined in `conftest.py` and available to all tests:

- `mock_trend_source` — Sample TrendSource
- `mock_sourcing_output` — Complete sourcing output
- `mock_asset_bundle` — Complete asset bundle with all 4 assets
- `mock_bundle_score_report` — Complete scoring report
- `mock_serper_api` — Mock Serper API response
- `mock_claude_response_*` — Various Claude API mock responses

## Mocking Strategy

### External APIs
- **Serper API** — Mocked to return predefined search results
- **Claude API** — Mocked to return valid JSON responses

### LangChain Components
- **ChatPromptTemplate** — Mocked to return mock chains
- **JsonOutputParser** — Mocked to validate JSON output
- **RunnableParallel** — Mocked for parallel execution

### File I/O
- **os.makedirs** — Mocked to prevent actual directory creation
- **open()** — Mocked for file writing

## Test Coverage Goals

| Module | Coverage Goal |
|--------|--------------|
| phase1_sourcing.py | 80% |
| phase2_processing.py | 75% |
| phase3_scoring.py | 80% |
| phase4_packaging.py | 85% |
| graph.py | 85% |
| models/schemas.py | 90% |

## Common Test Patterns

### Testing successful execution
```python
def test_function_success(self):
    result = function_under_test()
    assert result is not None
    assert result.field == expected_value
```

### Testing error handling
```python
def test_function_failure(self):
    with pytest.raises(SpecificException):
        function_that_raises()
```

### Mocking external APIs
```python
@patch('module.external_api')
def test_with_mock(self, mock_api):
    mock_api.return_value = expected_response
    result = function_under_test()
    assert result == expected
```


# Testing Plan

## Tools and Techniques

- Framework: pytest
- Coverage: pytest-cov
- Linting: Ruff
- Techniques: Equivalence Partitioning and Boundary Value Analysis

## Initial Test Cases

| ID | Requirement | Test Condition | Expected Result | Technique | Result |
|---|---|---|---|---|---|
| T01 | FR-00 | Open home page | HTTP 200 | Functional | Pass |
| T02 | FR-00 | Login with invalid credentials | Reject login | Equivalence Partitioning | Planned |
| T03 | FR-01 | View equipment catalogue | Display equipment | Functional | Planned |
| T04 | FR-02 | Submit a valid booking | Create Pending booking | Functional | Planned |
| T05 | FR-03 | End time equals start time | Reject | Boundary Value Analysis | Planned |
| T06 | FR-03 | Duration is 29 minutes | Reject | Boundary Value Analysis | Planned |
| T07 | FR-03 | Duration is 30 minutes | Accept | Boundary Value Analysis | Planned |
| T08 | FR-03 | Duration is 4 hours | Accept | Boundary Value Analysis | Planned |
| T09 | FR-03 | Duration is 4 hours 1 minute | Reject | Boundary Value Analysis | Planned |
| T10 | FR-03 | Booking starts in the past | Reject | Equivalence Partitioning | Planned |
| T11 | FR-03 | Equipment is out of service | Reject | Equivalence Partitioning | Planned |
| T12 | FR-03 | Booking overlaps a Pending booking | Reject | Boundary Value Analysis | Planned |
| T13 | FR-03 | Booking starts when existing booking ends | Accept | Boundary Value Analysis | Planned |
| T14 | FR-04 | Staff approves a Pending booking | Status becomes Approved | Functional | Planned |
| T15 | FR-04 | Student views own booking | Show current status | Functional | Planned |

## Test Execution Instructions

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run automated tests:

```powershell
python -m pytest -v
```

Run tests with coverage:

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

Run code quality checks:

```powershell
ruff check .
```

## Test Execution Results

Update this section after executing the tests.

| Item | Actual Result |
|---|---|
| Total tests | Record actual count |
| Passed | Record actual count |
| Failed | Record actual count |
| Code coverage | Record actual percentage |
| Ruff | Record actual result |

## Boundary Value and Negative Testing

The test suite should verify:
- Empty or missing required fields.
- Invalid booking start and end times.
- A duration of 29 minutes, 30 minutes, and 4 hours, according to the booking rules.
- Equipment that does not exist or is unavailable.
- Invalid login credentials, if login is implemented.

## Continuous Integration

GitHub Actions should execute the automated tests and Ruff checks whenever code is pushed or a pull request is opened. Review the Actions logs and record the actual results.

## Limitations

Only implemented features and executed tests should be reported as completed. Update the test results whenever the test suite changes.


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

## Initial Test Results

- T01 passed when executed with pytest.
- Coverage for app.py: 95%.
- Total statements: 20.
- Missed statements: 1.

## Notes

The remaining test cases are planned for implementation
as the related application features are developed.

Results must reflect actual test execution.

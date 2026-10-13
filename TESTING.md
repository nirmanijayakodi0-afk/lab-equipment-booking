# Testing Plan

## 1. Testing Tools

- pytest: Runs automated tests.
- pytest-cov: Measures test coverage.
- Ruff: Checks code quality and style.

## 2. Initial Test Cases

| Test ID | Test Description | Expected Result | Status |
|---|---|---|---|
| T01 | Open the home page | HTTP 200 response | Passed |
| T02 | Login with invalid details | Login is rejected | Planned |
| T03 | View equipment | Equipment list is displayed | Planned |
| T04 | Submit a valid booking | Booking request is created | Planned |
| T05 | Submit invalid booking times | Booking is rejected | Planned |
| T06 | Book unavailable equipment | Booking is rejected | Planned |
| T07 | Submit overlapping booking | Booking is rejected | Planned |
| T08 | Approve a booking | Booking status is updated | Planned |

## 3. Initial Testing Results

- The home page test passed using pytest.
- Initial code coverage for app.py was 95%.
- Additional test cases will be implemented as project features are developed.
- GitHub Actions initial run failed because the app module could not be imported. Fix and rerun required.

## 4. Future Testing

- Test equipment management.
- Test booking validation.
- Test login and role restrictions.
- Run all automated tests before merging pull requests.
- Run Ruff to check code quality.

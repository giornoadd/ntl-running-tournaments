# 🧪 Unit Test Results

This file captures the automated testing results for the `src/` modular pipeline. The test suite guarantees the integrity of our configuration mappings, image logic, files parsing, and CSV formulas.

### Latest Run (`pytest tests/ -v`)

```
=================== test session starts ====================
platform darwin -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/giornoadd/my-macos/running-comp
plugins: anyio-4.10.0, Faker-37.6.0, typeguard-4.4.4
collected 13 items                                         

tests/test_config.py::test_determine_team_mandalorian PASSED [  7%]
tests/test_config.py::test_determine_team_itsystem PASSED    [ 15%]
tests/test_config.py::test_determine_team_unknown PASSED     [ 23%]
tests/test_config.py::test_renamed_pattern_valid PASSED      [ 30%]
tests/test_config.py::test_renamed_pattern_invalid PASSED    [ 38%]
tests/test_files.py::test_get_nickname_with_parens_english PASSED [ 46%]
tests/test_files.py::test_get_nickname_no_parens_english PASSED   [ 53%]
tests/test_files.py::test_get_nickname_invalid PASSED        [ 61%]
tests/test_files.py::test_get_nickname_spacing PASSED        [ 69%]
tests/test_recalculate_csv.py::test_parse_runners_string_empty PASSED [ 76%]
tests/test_recalculate_csv.py::test_parse_runners_string_single PASSED [ 84%]
tests/test_recalculate_csv.py::test_parse_runners_string_multiple PASSED [ 92%]
tests/test_recalculate_csv.py::test_parse_runners_string_with_noise PASSED [100%]

==================== 13 passed in 0.03s ====================
```

**Status:** 🟩 **All Passing**

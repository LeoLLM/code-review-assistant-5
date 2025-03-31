# Code Review Assistant

An automated code review assistant system that provides templates and logic for code reviews.

## Features

- Pre-defined code review templates for different contexts (general, security, performance)
- Automated code review logic
- Example code with common issues for demonstration

## Installation

```bash
# Clone the repository
git clone https://github.com/LeoLLM/code-review-assistant-5.git
cd code-review-assistant-5

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Usage

```bash
# Basic usage
python review_logic.py example_code.py

# Specify a template
python review_logic.py example_code.py --template security

# Analyze multiple files
for file in *.py; do python review_logic.py "$file" --template performance; done
```

### API Usage

```python
from review_logic import CodeReviewAnalyzer

# Initialize the analyzer
analyzer = CodeReviewAnalyzer()

# Analyze a file
issues = analyzer.analyze_file("example_code.py")
for issue in issues:
    print(f"{issue['severity'].upper()} - Line {issue['line']}: {issue['message']}")

# Generate a review using a specific template
review = analyzer.generate_review("example_code.py", "security")
print(review)
```

### Example Output

Using the security template:

```
# Code Review for example_code.py

Using the security template.

## Issues Found

- **[HIGH]** Line 2: Hardcoded credentials detected. Use environment variables instead.
- **[HIGH]** Line 3: Hardcoded credentials detected. Use environment variables instead.
- **[HIGH]** Line 11: Potential SQL injection vulnerability. Use parameterized queries.
- **[MEDIUM]** Line 78: Bare except clause found. Specify exceptions to catch.
```

## Similar Projects

- [Danger](https://github.com/danger/danger) - Automates common code review chores
- [Review Dog](https://github.com/reviewdog/reviewdog) - Automated code review tool integrated with any linter

## Contributing

Please see the Issues section for planned enhancements and bugs that need fixing.

## License

MIT
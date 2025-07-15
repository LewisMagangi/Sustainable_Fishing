# Contributing to Sustainable Fishing Platform

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!
7. **Add yourself to the Contributors section below** (see format below).

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/LewisMagangi/Sustainable_Fishing/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/LewisMagangi/Sustainable_Fishing/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

- Use [Black](https://black.readthedocs.io/) for Python code formatting
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Write docstrings for functions and classes

## Setting Up Development Environment

1. **Clone the repository**
```bash
git clone https://github.com/LewisMagangi/Sustainable_Fishing.git
cd sustainable_fishing_project
```

2. **Create virtual environment**
```bash
python -m venv fishnet_env
source fishnet_env/bin/activate  # Linux/Mac
# fishnet_env\Scripts\activate   # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install black flake8  # Development tools
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Run tests**
```bash
python manage.py test
```

## Code Formatting

Before submitting a pull request, please run:

```bash
# Format code with Black
black .

# Check for style issues
flake8 .
```

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add user authentication system

- Implement Django's built-in authentication
- Add custom user profile model
- Create login/logout views
- Fixes #123
```

## Contributors

When you contribute to this project, please add your information to this list in alphabetical order by last name:

### Format:
```
- **[Your Name](https://github.com/yourusername)** - Brief description of contribution
```

### Current Contributors:

- **[Lewis Magangi](https://github.com/LewisMagangi)** - Project creator and maintainer
<!-- Add your name here when you contribute! -->

## Feature Requests

We track feature requests using GitHub issues. Before creating a new feature request:

1. **Check existing issues** to avoid duplicates
2. **Provide a clear title** that summarizes the feature
3. **Describe the problem** you're trying to solve
4. **Explain the solution** you'd like to see
5. **Consider alternatives** you've thought about
6. **Add mockups or examples** if helpful

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test both positive and negative scenarios

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions and classes
- Update API documentation if applicable
- Include examples in documentation

## Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Focus on what's best for the community
- Show empathy towards other community members

## Questions?

Don't hesitate to ask questions! You can:

- Open an issue for discussion
- Contact the maintainers directly
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to sustainable fishing practices! 🐟💚**

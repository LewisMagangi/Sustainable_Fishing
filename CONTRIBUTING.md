# Contributing to Sustainable Fishing Platform

Thank you for your interest in contributing to the Sustainable Fishing Platform. This guide outlines the process for contributing to our project and helps ensure a smooth collaboration experience.

## Ways to Contribute

We welcome contributions in the following areas:

* Bug reports and fixes
* Feature development and enhancements
* Documentation improvements
* Code reviews and testing
* Performance optimizations

## Development Setup

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
   pip install black flake8
   ```
4. **Run migrations**
   ```bash
   python manage.py migrate
   ```
5. **Run tests**
   ```bash
   python manage.py test
   ```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Run code formatting: `black .` and `flake8 .`
4. Ensure all tests pass
5. Submit pull request with clear description
6. Add yourself to the Contributors section

## Code Standards

Run before submitting PR:

```bash
black .
flake8 .
```

* Follow PEP 8 style guidelines
* Use descriptive variable and function names
* Add docstrings for functions and classes

## Contributors

* **[Lewis Magangi](https://github.com/LewisMagangi)** - Project creator and maintainer
* **[Fidel](https://github.com/phantom-kali)** - Developer
* **[Benard Karanja](https://github.com/N-cognto)** - Developer

*Add your name when you contribute!*

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to sustainable fishing practices! 🐟💚**

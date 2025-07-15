# 🐟 Sustainable Fishing Platform

A Django-based web platform promoting sustainable fishing practices and connecting fishing communities.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
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
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```
sustainable_fishing_project/
├── sustainable_fishing/    # Django project settings
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Development

### Adding new dependencies
```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Creating new Django apps
```bash
python manage.py startapp <app-name>
```

### Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🎯 Features (Planned)

- [ ] User registration and profiles
- [ ] Catch logging and tracking
- [ ] Educational content library
- [ ] Community timeline and posts
- [ ] Sustainable fishing guidelines
- [ ] Mobile-responsive design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Project Link: [https://github.com/yourusername/sustainable_fishing_project](https://github.com/yourusername/sustainable_fishing_project)

---

Made with ❤️ for sustainable fishing communities

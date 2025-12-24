# Syllabus Accessibility Checker

A web application that analyzes course syllabi for accessibility issues based on WCAG guidelines and educational best practices.

🌐 **Live Demo**: https://syllabus-checker.clarkenstein.com

## Features

### 42+ Automated Accessibility Checks

Issues are organized into 8 categories:

- **Font Usage** - font sizes, decorative fonts, consistency
- **Table Structure** - headers, captions, layout tables, merged cells
- **Color & Contrast** - WCAG compliance, color-only meaning
- **Links & Navigation** - descriptive text, table of contents, bookmarks
- **Lists** - proper formatting, hierarchy
- **Text Formatting** - alignment, spacing, caps, emphasis
- **Readability** - sentence length, date format clarity
- **Images** - alt text, decorative marking, text content detection
- **Document Properties** - metadata, language

### User-Friendly Interface

- Drag-and-drop file upload
- Real-time processing
- Categorized results with expandable details
- Download marked document with issues highlighted
- Mobile-responsive design

## Quick Start (Local Development)

```bash
# Clone the repository
git clone <your-repo-url>
cd syllabus_checker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

Visit http://localhost:5001 in your browser!

## Production Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment instructions for syllabus-check.clarkenstein.com.

Quick summary:
1. Set up server with Python 3.8+, nginx
2. Install dependencies in virtual environment
3. Configure gunicorn systemd service
4. Set up nginx reverse proxy
5. Add SSL with Let's Encrypt

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Document Processing**: python-docx
- **Production Server**: Gunicorn
- **Web Server**: Nginx

## How It Works

1. **Upload** a `.docx` syllabus file via web interface
2. **Analysis** runs 42+ checks across 8 categories
3. **View Results** organized by category with expandable details
4. **Download** marked document with issues highlighted in yellow

## Key Files

- `app.py` - Flask web application
- `syllabus_checker.py` - Core checking logic
- `wsgi.py` - WSGI entry point for production
- `templates/` - HTML templates (index, results, about)
- `requirements.txt` - Python dependencies
- `Uniform-Syllabus-Template-1.docx` - Required sections template

## Configuration

Environment variables (set in `.env` for production):

```bash
SECRET_KEY=<generate-with-secrets.token_hex()>
UPLOAD_FOLDER=/var/www/syllabus-checker/uploads
```

## API / Command Line

The underlying checker can also be used as a Python library:

```python
from syllabus_checker import SyllabusChecker

checker = SyllabusChecker('template.docx', 'my_syllabus.docx')
missing = checker.check_missing_sections()
checker.run_all_checks()
report = checker.generate_report()
checker.create_marked_document('output_marked.docx')
```

## Development

```bash
# Install in development mode
pip install -e .

# Run with debug mode
python app.py

# Access at http://localhost:5001
```

Debug output can be enabled by uncommenting the debug print statements in `app.py`.

## Security Considerations

- Files are stored temporarily and auto-deleted
- Upload size limited to 16MB
- Only `.docx` files accepted
- Secret key configured via environment variable
- HTTPS required in production

## Contributing

Issues and feature requests welcome! This tool is actively maintained.

## License

Copyright © 2025

---

**Live at**: https://syllabus-check.clarkenstein.com

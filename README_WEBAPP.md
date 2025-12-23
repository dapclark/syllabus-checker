# Syllabus Accessibility Checker - Web Application

A user-friendly web interface for checking Word document syllabi for accessibility issues.

## Features

- **Drag & Drop Upload**: Simply drag and drop your .docx file or click to browse
- **40+ Accessibility Checks**: Comprehensive testing for tables, headings, fonts, colors, images, and more
- **Instant Results**: Get detailed feedback in seconds
- **Downloadable Report**: Download a marked document with all issues highlighted
- **Beautiful Interface**: Clean, modern design with visual feedback

## Installation

1. Create and activate virtual environment (if not already done):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Web App

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

**Note for macOS users:** We use port 5001 instead of 5000 to avoid conflicts with AirPlay Receiver.

3. Upload your syllabus (.docx file) using drag-and-drop or file browser

4. View the detailed accessibility report

5. Download the marked document with issues highlighted

## How It Works

1. **Upload**: Users drag and drop or select a Word document (.docx)
2. **Analysis**: The system runs 40+ accessibility checks on the document
3. **Results**: A comprehensive report is displayed showing:
   - Total number of issues
   - Missing required sections
   - Issues grouped by category
   - Detailed accessibility report
4. **Download**: Users can download the marked document with comments and highlights

## Accessibility Checks Include

- **Tables**: Headers, layout detection, captions, merged cells, scope declarations
- **Typography**: Font sizes, decorative fonts, consistency, ALL CAPS blocks
- **Color & Contrast**: WCAG compliance, color-only meaning
- **Links**: Descriptive text, styling, long URLs, PDF links
- **Images**: Alt text, decorative marking
- **Lists**: Manual formatting, hierarchy, layout misuse
- **Document Properties**: Metadata, language settings
- **Readability**: Long sentences
- **And more...**

## Configuration

- **Max Upload Size**: 16MB (configurable in `app.py`)
- **Allowed File Types**: .docx only
- **Port**: 5001 (configurable in `app.py` - using 5001 to avoid macOS AirPlay conflict)

## Production Deployment

For production use:

1. Change the secret key in `app.py`:
```python
app.secret_key = 'your-secure-random-secret-key'
```

2. Set `debug=False`

3. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. Consider using a reverse proxy (nginx, Apache)

5. Set up proper file storage and cleanup

## Troubleshooting

- **Port already in use**: Change the port number in `app.py`
- **File upload fails**: Check file size (max 16MB) and format (.docx only)
- **Module not found**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## Command Line Version

For command-line usage, see the main README and use:
```bash
python syllabus_checker.py your_document.docx
```

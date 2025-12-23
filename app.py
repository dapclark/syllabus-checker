"""
Syllabus Accessibility Checker Web Application
Flask app for uploading and checking Word documents for accessibility issues
"""

from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from werkzeug.utils import secure_filename
from syllabus_checker import SyllabusChecker
import tempfile
import shutil
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'syllabus-checker-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', tempfile.mkdtemp())

ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main upload page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and run accessibility checks"""
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a .docx file', 'error')
        return redirect(url_for('index'))

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Run accessibility checker
        # Note: SyllabusChecker expects (template_path, target_path)
        checker = SyllabusChecker('Uniform-Syllabus-Template-1.docx', upload_path)

        # Get missing sections
        missing_sections = checker.check_missing_sections()

        # Run all checks
        checker.run_all_checks()

        # Generate report (generate_report already returns a joined string)
        report_text = checker.generate_report()

        # Create marked document
        marked_filename = f"{os.path.splitext(filename)[0]}_marked.docx"
        marked_path = os.path.join(app.config['UPLOAD_FOLDER'], marked_filename)
        checker.create_marked_document(marked_path)

        # Define categories that group related issue types
        category_mapping = {
            'Font Usage': ['SMALL_FONT', 'DECORATIVE_FONT', 'INCONSISTENT_FONTS'],
            'Table Structure': ['EMPTY_TABLE_ROW', 'EMPTY_TABLE_COLUMN', 'LAYOUT_TABLE', 'TABLE_NO_HEADER',
                               'TABLE_MISSING_SCOPE', 'TABLE_MISSING_CAPTION', 'MERGED_CELLS', 'NUMERIC_ALIGNMENT',
                               'TABLE_READING_ORDER', 'EMBEDDED_TABLE_IMAGE'],
            'Color & Contrast': ['LOW_CONTRAST', 'COLOR_ONLY_MEANING', 'TEXT_OVER_BACKGROUND', 'COLOR_CODED_TABLE'],
            'Links & Navigation': ['NON_DESCRIPTIVE_LINK', 'UNSTYLED_LINK', 'LONG_URL', 'PDF_LINK',
                                   'MISSING_TOC', 'MISSING_BOOKMARKS'],
            'Lists': ['INCONSISTENT_LIST_HIERARCHY', 'LAYOUT_LIST'],
            'Text Formatting': ['PSEUDO_TABLE', 'UNDERLINE_NON_LINK', 'INSUFFICIENT_LINE_SPACING',
                               'FULL_JUSTIFICATION', 'ALL_CAPS_BLOCK', 'EXCESSIVE_BOLD',
                               'EXCESSIVE_ITALIC', 'EXCESSIVE_UNDERLINE', 'INCONSISTENT_FORMATTING'],
            'Readability': ['LONG_SENTENCE'],
            'Images': ['MISSING_ALT_TEXT', 'QUESTIONABLE_DECORATIVE'],
            'Document Properties': ['MISSING_TITLE', 'MISSING_LANGUAGE', 'MULTILINGUAL_CONTENT'],
        }

        # Map each issue type to its report section header
        issue_section_map = {
            'SMALL_FONT': 'ACCESSIBILITY: FONT SIZES',
            'DECORATIVE_FONT': 'ACCESSIBILITY: DECORATIVE/INACCESSIBLE FONTS',
            'INCONSISTENT_FONTS': 'ACCESSIBILITY: FONT CONSISTENCY',
            'EMPTY_TABLE_ROW': 'ACCESSIBILITY: EMPTY TABLE ROWS/COLUMNS',
            'EMPTY_TABLE_COLUMN': 'ACCESSIBILITY: EMPTY TABLE ROWS/COLUMNS',
            'LAYOUT_TABLE': 'ACCESSIBILITY: LAYOUT vs. DATA TABLES',
            'TABLE_NO_HEADER': 'ACCESSIBILITY: TABLE HEADERS',
            'TABLE_MISSING_SCOPE': 'ACCESSIBILITY: TABLE SCOPE DECLARATIONS',
            'TABLE_MISSING_CAPTION': 'ACCESSIBILITY: TABLE CAPTIONS',
            'MERGED_CELLS': 'ACCESSIBILITY: MERGED/SPLIT CELLS',
            'NUMERIC_ALIGNMENT': 'ACCESSIBILITY: TABLE NUMERIC ALIGNMENT',
            'TABLE_READING_ORDER': 'ACCESSIBILITY: TABLE READING ORDER',
            'EMBEDDED_TABLE_IMAGE': 'ACCESSIBILITY: EMBEDDED IMAGES IN TABLES',
            'LOW_CONTRAST': 'ACCESSIBILITY: COLOR CONTRAST',
            'COLOR_ONLY_MEANING': 'ACCESSIBILITY: COLOR AS SOLE INDICATOR',
            'TEXT_OVER_BACKGROUND': 'ACCESSIBILITY: TEXT OVER COLORED BACKGROUNDS',
            'COLOR_CODED_TABLE': 'ACCESSIBILITY: COLOR AS SOLE INDICATOR',
            'NON_DESCRIPTIVE_LINK': 'ACCESSIBILITY: NON-DESCRIPTIVE LINKS',
            'UNSTYLED_LINK': 'ACCESSIBILITY: UNSTYLED LINKS',
            'LONG_URL': 'ACCESSIBILITY: LONG URLs',
            'PDF_LINK': 'ACCESSIBILITY: LINKS TO PDFs',
            'MISSING_TOC': 'ACCESSIBILITY: TABLE OF CONTENTS',
            'MISSING_BOOKMARKS': 'ACCESSIBILITY: BOOKMARKS/NAVIGATION',
            'INCONSISTENT_LIST_HIERARCHY': 'ACCESSIBILITY: NESTED LIST HIERARCHY',
            'LAYOUT_LIST': 'ACCESSIBILITY: LISTS USED FOR LAYOUT',
            'PSEUDO_TABLE': 'ACCESSIBILITY: MANUAL ALIGNMENT (PSEUDO-TABLES)',
            'UNDERLINE_NON_LINK': 'ACCESSIBILITY: UNDERLINED NON-LINK TEXT',
            'INSUFFICIENT_LINE_SPACING': 'ACCESSIBILITY: LINE SPACING',
            'FULL_JUSTIFICATION': 'ACCESSIBILITY: TEXT JUSTIFICATION',
            'ALL_CAPS_BLOCK': 'ACCESSIBILITY: ALL CAPS TEXT BLOCKS',
            'EXCESSIVE_BOLD': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'EXCESSIVE_ITALIC': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'EXCESSIVE_UNDERLINE': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'INCONSISTENT_FORMATTING': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'LONG_SENTENCE': 'ACCESSIBILITY: LONG SENTENCES',
            'MISSING_ALT_TEXT': 'ACCESSIBILITY: IMAGE ALT TEXT',
            'QUESTIONABLE_DECORATIVE': 'ACCESSIBILITY: DECORATIVE IMAGE MARKING',
            'MISSING_TITLE': 'ACCESSIBILITY: DOCUMENT METADATA',
            'MISSING_LANGUAGE': 'ACCESSIBILITY: DOCUMENT LANGUAGE',
            'MULTILINGUAL_CONTENT': 'ACCESSIBILITY: MULTILINGUAL CONTENT',
        }

        # Count issues by category
        category_counts = {}
        issues_by_category = {}

        # Debug: track all issue types found
        all_issue_types = set()

        for issue in checker.issues:
            all_issue_types.add(issue.issue_type)

            # Find which category this issue belongs to
            issue_category = None
            for category, issue_types in category_mapping.items():
                if issue.issue_type in issue_types:
                    issue_category = category
                    break

            if issue_category:
                if issue_category not in category_counts:
                    category_counts[issue_category] = 0
                    issues_by_category[issue_category] = set()
                category_counts[issue_category] += 1
                issues_by_category[issue_category].add(issue.issue_type)
            # else:
                # Issue type not mapped to any category (uncomment for debugging)
                # print(f"WARNING: Issue type '{issue.issue_type}' not mapped to any category")

        # Extract content for each category by combining relevant sections
        category_details = {}
        report_lines = report_text.split('\n')

        for category, issue_types in category_mapping.items():
            if category not in issues_by_category:
                continue  # Skip categories with no issues

            # Get all unique section headers for this category
            section_headers = set()
            for issue_type in issues_by_category[category]:
                if issue_type in issue_section_map:
                    section_headers.add(issue_section_map[issue_type])

            # Extract content from all relevant sections
            combined_content = []
            for section_header in sorted(section_headers):
                section_content = []
                in_section = False

                for line in report_lines:
                    if section_header in line:
                        in_section = True
                        # Add the section header (without "ACCESSIBILITY: " prefix)
                        section_title = section_header.replace('ACCESSIBILITY: ', '')
                        section_content.append(f"── {section_title} ──")
                        continue
                    elif in_section:
                        # Stop at next section
                        if line.startswith('ACCESSIBILITY:') and section_header not in line:
                            break
                        # Skip the dashes line
                        if line.startswith('-' * 20):
                            continue
                        # Collect content lines
                        if line.strip():
                            section_content.append(line)
                        # Stop after a blank line following content
                        elif section_content:
                            break

                if section_content:
                    combined_content.extend(section_content)
                    combined_content.append('')  # Add spacing between sections

            if combined_content:
                category_details[category] = '\n'.join(combined_content)

        # Debug output (comment out for production)
        # print(f"\n=== DEBUG: Issue Types Found ===")
        # print(f"All issue types: {sorted(all_issue_types)}")
        # print(f"Categories with issues: {sorted(category_counts.keys())}")
        # print(f"Category counts: {category_counts}")
        # print("================================\n")

        # Prepare results
        results = {
            'filename': filename,
            'total_issues': len(checker.issues),
            'missing_sections': missing_sections,
            'category_counts': category_counts,
            'category_details': category_details,
            'report_text': report_text,
            'marked_file': marked_filename,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return render_template('results.html', results=results)

    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download marked document"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    # Clean up temp folder on exit
    import atexit
    atexit.register(lambda: shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True))

    # Run the app (using port 5001 to avoid macOS AirPlay conflict)
    app.run(debug=True, host='0.0.0.0', port=5001)

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
from dotenv import load_dotenv
import markdown
import analytics_db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'syllabus-checker-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', '/tmp/syllabus_checker_uploads')

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Run accessibility checker
        # Note: SyllabusChecker expects (template_path, target_path)
        checker = SyllabusChecker('Uniform-Syllabus-Template-1.docx', upload_path)

        # Get section analysis using LLM (semantic matching)
        section_analysis = checker.analyze_sections_with_llm()

        # Extract just the missing sections list for backward compatibility
        missing_sections = section_analysis.get('missing', [])

        # Run all checks
        checker.run_all_checks()

        # Get additional checks that return dictionaries (not added to self.issues)
        heading_check = checker.check_heading_structure()
        table_check = checker.check_table_usage()
        list_check = checker.check_list_usage()

        # Run growth mindset and belonging analysis
        growth_mindset_analysis = checker.analyze_growth_mindset_and_belonging()

        # Run syllabus quality analysis
        quality_analysis = checker.analyze_syllabus_quality()

        # Extract course metadata using LLM
        course_metadata = checker.extract_course_metadata()

        # Run image alt text analysis
        image_alt_analysis = checker.analyze_image_alt_text()

        # Generate report (generate_report already returns a joined string)
        report_text = checker.generate_report()

        # Create marked document with missing sections and growth mindset recommendations
        marked_filename = f"{os.path.splitext(filename)[0]}_marked.docx"
        marked_path = os.path.join(app.config['UPLOAD_FOLDER'], marked_filename)
        checker.create_marked_document(marked_path, missing_sections, growth_mindset_analysis)

        # Define categories that group related issue types
        category_mapping = {
            'Font Usage': ['SMALL_FONT', 'DECORATIVE_FONT', 'INCONSISTENT_FONTS'],
            'Table Structure': ['EMPTY_TABLE_ROW', 'EMPTY_TABLE_COLUMN', 'LAYOUT_TABLE', 'TABLE_NO_HEADER',
                               'TABLE_MISSING_SCOPE', 'TABLE_MISSING_CAPTION', 'MERGED_CELLS', 'NUMERIC_ALIGNMENT',
                               'TABLE_READING_ORDER', 'EMBEDDED_TABLE_IMAGE'],
            'Color & Contrast': ['LOW_CONTRAST', 'COLOR_ONLY_MEANING', 'TEXT_OVER_BACKGROUND', 'COLOR_CODED_TABLE'],
            'Links & Navigation': ['NON_DESCRIPTIVE_LINK', 'UNSTYLED_LINK', 'LONG_URL',
                                   'MISSING_TOC', 'MISSING_BOOKMARKS'],
            'Lists': ['INCONSISTENT_LIST_HIERARCHY', 'LAYOUT_LIST'],
            'Text Formatting': ['PSEUDO_TABLE', 'UNDERLINE_NON_LINK', 'INSUFFICIENT_LINE_SPACING',
                               'FULL_JUSTIFICATION', 'ALL_CAPS_BLOCK', 'EXCESSIVE_BOLD',
                               'EXCESSIVE_ITALIC', 'EXCESSIVE_UNDERLINE', 'INCONSISTENT_FORMATTING'],
            'Readability': ['LONG_SENTENCE', 'NUMERIC_DATE_FORMAT'],
            'Images': ['IMAGE_MISSING_ALT', 'DECORATIVE_IMAGE_QUESTIONABLE', 'IMAGE_TEXT_CONTENT'],
            'Document Properties': ['MISSING_TITLE', 'MISSING_LANGUAGE', 'MULTIPLE_LANGUAGES'],
            'Heading Structure': ['ALL_CAPS_HEADING', 'LONG_HEADING', 'H1_NOT_AT_TOP', 'MULTIPLE_H1',
                                 'SHOULD BE HEADING 2', 'SHOULD BE HEADING 3', 'SHOULD BE HEADING 4'],
            'Content Quality': ['BROKEN_STYLE_COPIED_CONTENT', 'FOOTNOTE_USAGE', 'VISUAL_INDICATOR_NO_TEXT', 'MATH_NO_ACCESSIBLE_MARKUP'],
        }

        # Faculty-friendly help information for each category
        category_help = {
            'Font Usage': {
                'summary': 'Some text may be hard to read due to small or decorative fonts.',
                'why_matters': 'Students with visual impairments or reading difficulties need adequate font sizes (11pt+) and clear, standard fonts to read your syllabus.',
                'how_to_fix': 'Select the text → Home tab → Change font size to 11pt or larger. Use Arial, Calibri, or Times New Roman.',
                'help_link': 'https://support.microsoft.com/en-us/office/change-the-font-size-dc5b3f47-9e78-4af6-9734-ffc69175811c',
                'help_text': 'How to change fonts'
            },
            'Table Structure': {
                'summary': 'Tables need proper structure so screen readers can navigate them.',
                'why_matters': 'Screen readers announce table contents cell-by-cell. Without proper headers, students using assistive technology can\'t understand what each cell means.',
                'what_is_it': '<strong>Table header</strong> = the top row that labels each column (e.g., "Week", "Topic", "Reading"). This tells screen readers what each column contains.',
                'how_to_fix': 'Click anywhere in your table → Table Design tab → Check "Header Row" box. This marks the first row as the header.',
                'help_link': 'https://support.microsoft.com/en-us/office/video-create-accessible-tables-in-word-cb464015-59dc-46a0-ac01-6217c62210e5',
                'help_text': 'Video: Fix table headers'
            },
            'Color & Contrast': {
                'summary': 'Some colors may be hard to see or distinguish.',
                'why_matters': 'About 8% of men have some form of color blindness. Low contrast text is also difficult for students reading on phones or in bright environments.',
                'how_to_fix': 'Use dark text (black or dark blue) on light backgrounds. If you use color to convey meaning (like red for "late"), also add a text label.',
                'help_link': 'https://webaim.org/resources/contrastchecker/',
                'help_text': 'Check your colors'
            },
            'Links & Navigation': {
                'summary': 'Some links use vague text like "click here" that doesn\'t describe the destination.',
                'why_matters': 'Screen reader users often navigate by jumping between links. If all links say "click here," they can\'t tell where each one goes.',
                'how_to_fix': 'Right-click the link → Edit Hyperlink → Change "Text to display" to something descriptive like "view the grading rubric" instead of "click here".',
                'help_link': 'https://support.microsoft.com/en-us/office/create-accessible-links-in-word-28305cc8-3be2-417f-a789-67c5a8d14393',
                'help_text': 'How to fix link text'
            },
            'Text Formatting': {
                'summary': 'Some formatting choices can make text harder to read.',
                'why_matters': 'ALL CAPS text is harder to read (we recognize words by their shape). Justified text creates uneven spacing. Underlined text looks like links.',
                'how_to_fix': 'For emphasis, use <strong>bold</strong> instead of ALL CAPS or underline. Use left alignment instead of justified. Use Word\'s built-in Heading styles.',
                'help_link': 'https://support.microsoft.com/en-us/office/use-headings-and-styles-in-word-c0d409b5-5c0a-4a5c-8c5e-001e76072e51',
                'help_text': 'Using Word styles'
            },
            'Images': {
                'summary': 'Some images are missing descriptions (alt text).',
                'why_matters': 'Students who are blind or have low vision use screen readers that read alt text aloud. Without it, they miss the image content entirely.',
                'what_is_it': '<strong>Alt text</strong> = a brief description of what\'s in the image. It should convey the same information a sighted person would get.',
                'how_to_fix': 'Right-click the image → "View Alt Text" (or "Edit Alt Text") → Type a brief description like "UWM logo" or "Chart showing enrollment trends 2020-2024".',
                'help_link': 'https://support.microsoft.com/en-us/office/add-alternative-text-to-a-shape-picture-chart-smartart-graphic-or-other-object-44989b2a-903c-4d9a-b742-6a75b451c669',
                'help_text': 'Video: Add alt text'
            },
            'Document Properties': {
                'summary': 'The document is missing a title or language setting.',
                'why_matters': 'Screen readers announce the document title when opening a file. The language setting ensures text-to-speech uses correct pronunciation.',
                'how_to_fix': 'File → Info → Properties (on the right) → Add a Title. For language: Review tab → Language → Set Proofing Language.',
                'help_link': 'https://support.microsoft.com/en-us/office/make-your-word-documents-accessible-d9bf3683-87ac-47ea-b91a-78dcacb3c66d',
                'help_text': 'Full accessibility guide'
            },
            'Heading Structure': {
                'summary': 'The document structure could be improved with proper headings.',
                'why_matters': 'Screen reader users navigate long documents by jumping between headings. Proper heading levels (Heading 1, 2, 3) create a logical outline.',
                'what_is_it': '<strong>Headings</strong> = structural markers that create an outline. Use Heading 1 for the title, Heading 2 for main sections, Heading 3 for subsections.',
                'how_to_fix': 'Select your heading text → Home tab → Styles group → Click "Heading 1", "Heading 2", etc. Don\'t just make text big and bold—use actual heading styles.',
                'help_link': 'https://support.microsoft.com/en-us/office/use-headings-and-styles-in-word-c0d409b5-5c0a-4a5c-8c5e-001e76072e51',
                'help_text': 'Using heading styles'
            },
            'Content Quality': {
                'summary': 'Some content may have formatting issues or accessibility concerns.',
                'why_matters': 'Pasted content often brings hidden formatting problems. Footnotes can be hard to navigate. Visual symbols need text alternatives.',
                'how_to_fix': 'When pasting, use Ctrl+Shift+V (or Paste Special → Keep Text Only) to avoid formatting issues. Replace footnotes with inline explanations when possible.',
                'help_link': 'https://support.microsoft.com/en-us/office/make-your-word-documents-accessible-d9bf3683-87ac-47ea-b91a-78dcacb3c66d',
                'help_text': 'Accessibility best practices'
            },
            'Lists': {
                'summary': 'List formatting could be improved.',
                'why_matters': 'Properly formatted lists help screen readers announce "list of 5 items" and navigate item-by-item.',
                'how_to_fix': 'Use Word\'s built-in bullet or numbered list buttons instead of manually typing dashes or numbers.',
                'help_link': 'https://support.microsoft.com/en-us/office/create-a-bulleted-or-numbered-list-9ff81241-58a8-4d88-8d8c-acab3006a23e',
                'help_text': 'Creating proper lists'
            },
            'Readability': {
                'summary': 'Some content may be difficult to read or understand.',
                'why_matters': 'Long sentences and ambiguous dates can confuse all students, especially non-native English speakers and those with cognitive disabilities.',
                'how_to_fix': 'Break long sentences into shorter ones. Use clear date formats like "January 15, 2024" instead of "1/15/24".',
                'help_link': 'https://support.microsoft.com/en-us/office/get-your-document-s-readability-and-level-statistics-85b4969e-e80a-4777-8dd3-f7fc3c8b3fd2',
                'help_text': 'Check readability'
            },
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
            'TABLE_MISSING_CAPTION': 'ACCESSIBILITY: TABLE CAPTIONS/DESCRIPTIONS',
            'MERGED_CELLS': 'ACCESSIBILITY: TABLE MERGED CELLS',
            'NUMERIC_ALIGNMENT': 'ACCESSIBILITY: TABLE NUMERIC ALIGNMENT',
            'TABLE_READING_ORDER': 'ACCESSIBILITY: TABLE READING ORDER',
            'EMBEDDED_TABLE_IMAGE': 'ACCESSIBILITY: TABLE EMBEDDED IMAGES',
            'LOW_CONTRAST': 'ACCESSIBILITY: COLOR CONTRAST',
            'COLOR_ONLY_MEANING': 'ACCESSIBILITY: COLOR AS SOLE INDICATOR',
            'TEXT_OVER_BACKGROUND': 'ACCESSIBILITY: TEXT OVER COLORED BACKGROUNDS',
            'COLOR_CODED_TABLE': 'ACCESSIBILITY: COLOR AS SOLE INDICATOR',
            'NON_DESCRIPTIVE_LINK': 'ACCESSIBILITY: NON-DESCRIPTIVE LINKS',
            'UNSTYLED_LINK': 'ACCESSIBILITY: UNSTYLED LINKS',
            'LONG_URL': 'ACCESSIBILITY: LONG URLs',
            'MISSING_TOC': 'ACCESSIBILITY: TABLE OF CONTENTS',
            'MISSING_BOOKMARKS': 'ACCESSIBILITY: INTERNAL NAVIGATION/BOOKMARKS',
            'INCONSISTENT_LIST_HIERARCHY': 'ACCESSIBILITY: NESTED LIST HIERARCHY',
            'LAYOUT_LIST': 'ACCESSIBILITY: LISTS USED FOR LAYOUT',
            'PSEUDO_TABLE': 'ACCESSIBILITY: MANUAL ALIGNMENT (PSEUDO-TABLES)',
            'UNDERLINE_NON_LINK': 'ACCESSIBILITY: UNDERLINED TEXT',
            'INSUFFICIENT_LINE_SPACING': 'ACCESSIBILITY: LINE SPACING',
            'FULL_JUSTIFICATION': 'ACCESSIBILITY: TEXT JUSTIFICATION',
            'ALL_CAPS_BLOCK': 'ACCESSIBILITY: ALL CAPS TEXT BLOCKS',
            'EXCESSIVE_BOLD': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'EXCESSIVE_ITALIC': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'EXCESSIVE_UNDERLINE': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'INCONSISTENT_FORMATTING': 'ACCESSIBILITY: EXCESSIVE/INCONSISTENT FORMATTING',
            'LONG_SENTENCE': 'ACCESSIBILITY: SENTENCE LENGTH',
            'IMAGE_MISSING_ALT': 'ACCESSIBILITY: IMAGE ALT TEXT',
            'DECORATIVE_IMAGE_QUESTIONABLE': 'ACCESSIBILITY: DECORATIVE IMAGE MARKING',
            'IMAGE_TEXT_CONTENT': 'ACCESSIBILITY: IMAGES CONTAINING TEXT/SCHEDULES',
            'NUMERIC_DATE_FORMAT': 'ACCESSIBILITY: DATE FORMATS',
            'MISSING_TITLE': 'ACCESSIBILITY: DOCUMENT METADATA',
            'MISSING_LANGUAGE': 'ACCESSIBILITY: DOCUMENT LANGUAGE SETTING',
            'MULTIPLE_LANGUAGES': 'ACCESSIBILITY: MULTILINGUAL CONTENT',
            'BROKEN_STYLE_COPIED_CONTENT': 'ACCESSIBILITY: COPIED CONTENT WITH INCONSISTENT STYLES',
            'FOOTNOTE_USAGE': 'ACCESSIBILITY: FOOTNOTE USAGE',
            'VISUAL_INDICATOR_NO_TEXT': 'ACCESSIBILITY: VISUAL INDICATORS WITHOUT TEXT',
            'MATH_NO_ACCESSIBLE_MARKUP': 'ACCESSIBILITY: MATHEMATICAL EXPRESSIONS',
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

        # Extract the SUMMARY section from the report
        summary_section = ""
        report_lines = report_text.split('\n')
        in_summary = False
        summary_lines = []

        for i, line in enumerate(report_lines):
            # Look for the SUMMARY header (it's between two lines of equals signs)
            if line.strip() == "SUMMARY":
                # Skip the next line (which should be another line of equals signs)
                in_summary = True
                continue
            elif in_summary:
                # Skip the line of equals signs right after SUMMARY
                if line.strip().startswith("=" * 40) and len(summary_lines) == 0:
                    continue
                # Stop at the next major section (another line of equals signs after we've started collecting)
                if line.strip().startswith("=" * 40) and len(summary_lines) > 0:
                    break
                summary_lines.append(line)

        summary_section = '\n'.join(summary_lines).strip()

        # Calculate total issues (must match text report calculation)
        # Total includes: missing sections + heading/table/list check issues + all other issues from run_all_checks()
        total_web_issues = (
            len(missing_sections) +
            len(heading_check.get('issues', [])) +
            len(table_check.get('issues', [])) +
            len(list_check.get('issues', [])) +
            len(checker.issues)
        )

        # Debug output (comment out for production)
        # print(f"\n=== ISSUE COUNT DEBUG ===")
        # print(f"Missing sections: {len(missing_sections)}")
        # print(f"Heading check issues: {len(heading_check.get('issues', []))}")
        # print(f"Table check issues: {len(table_check.get('issues', []))}")
        # print(f"List check issues: {len(list_check.get('issues', []))}")
        # print(f"Checker.issues (algorithmic): {len(checker.issues)}")
        # print(f"Total for web: {total_web_issues}")
        # print(f"\nCategory counts sum: {sum(category_counts.values())}")
        # print(f"Categories: {category_counts}")
        # print(f"All issue types found: {sorted(all_issue_types)}")
        # print("========================\n")

        # Prepare summary
        summary_message = ""
        if total_web_issues == 0:
            summary_message = "Excellent! This syllabus meets all standards."
            summary_status = "success"
        elif total_web_issues < 5:
            summary_message = f"This syllabus has {total_web_issues} issue(s) that should be addressed."
            summary_status = "warning"
        else:
            summary_message = f"This syllabus has {total_web_issues} issue(s) that need attention."
            summary_status = "danger"

        # Add structural issues to appropriate categories
        # These come from heading_check, table_check, and list_check which return plain strings
        if table_check.get('issues'):
            # Add table structure issues to the Table Structure category
            if 'Table Structure' not in category_counts:
                category_counts['Table Structure'] = 0
            category_counts['Table Structure'] += len(table_check.get('issues', []))

            # Extract table usage section from report for category details
            if 'Table Structure' not in category_details:
                category_details['Table Structure'] = ''

            # Add table usage issues to the details
            table_usage_section = []
            report_lines = report_text.split('\n')
            in_table_usage = False
            for line in report_lines:
                if 'ACCESSIBILITY: TABLE USAGE' in line:
                    in_table_usage = True
                    table_usage_section.append('── TABLE USAGE ──')
                    continue
                elif in_table_usage:
                    if line.startswith('ACCESSIBILITY:') or line.startswith('=' * 40):
                        break
                    if line.startswith('-' * 40):
                        continue
                    if line.strip():
                        table_usage_section.append(line)

            if table_usage_section:
                # Prepend to existing Table Structure details
                existing = category_details.get('Table Structure', '')
                category_details['Table Structure'] = '\n'.join(table_usage_section) + '\n\n' + existing

        if heading_check.get('issues'):
            # Add heading structure issues - create a new category for document structure
            if 'Document Structure' not in category_counts:
                category_counts['Document Structure'] = 0
            category_counts['Document Structure'] += len(heading_check.get('issues', []))

            # Extract heading sections from report
            heading_sections = []
            report_lines = report_text.split('\n')
            for section_name in ['ACCESSIBILITY: HEADING STRUCTURE', 'ACCESSIBILITY: HEADING LEVEL RECOMMENDATIONS']:
                in_section = False
                for line in report_lines:
                    if section_name in line:
                        in_section = True
                        heading_sections.append(f"── {section_name.replace('ACCESSIBILITY: ', '')} ──")
                        continue
                    elif in_section:
                        if line.startswith('ACCESSIBILITY:') or line.startswith('=' * 40):
                            break
                        if line.startswith('-' * 40):
                            continue
                        if line.strip():
                            heading_sections.append(line)
                if in_section:
                    heading_sections.append('')  # Add spacing

            if heading_sections:
                category_details['Document Structure'] = '\n'.join(heading_sections)

        if list_check.get('issues'):
            # Add list issues to the Lists category
            if 'Lists' not in category_counts:
                category_counts['Lists'] = 0
            category_counts['Lists'] += len(list_check.get('issues', []))

        # Convert growth mindset analysis markdown to HTML
        if growth_mindset_analysis.get('status') == 'success' and 'analysis' in growth_mindset_analysis:
            # Convert markdown to HTML with extra extensions for better formatting
            growth_mindset_analysis['analysis_html'] = markdown.markdown(
                growth_mindset_analysis['analysis'],
                extensions=['extra', 'nl2br', 'sane_lists']
            )

        # Convert quality analysis markdown to HTML
        if quality_analysis.get('status') == 'success' and 'analysis' in quality_analysis:
            quality_analysis['analysis_html'] = markdown.markdown(
                quality_analysis['analysis'],
                extensions=['extra', 'nl2br', 'sane_lists']
            )

        # Convert image alt text analysis markdown to HTML
        if image_alt_analysis.get('status') == 'success' and 'analysis' in image_alt_analysis:
            image_alt_analysis['analysis_html'] = markdown.markdown(
                image_alt_analysis['analysis'],
                extensions=['extra', 'nl2br', 'sane_lists']
            )

        results = {
            'filename': filename,
            'total_issues': total_web_issues,  # Match the text report calculation
            'missing_sections': missing_sections,
            'section_analysis': section_analysis,  # Detailed analysis with found/suggest_rename/missing
            'category_counts': category_counts,
            'category_details': category_details,
            'category_help': category_help,  # Faculty-friendly explanations
            'report_text': report_text,
            'summary_section': summary_section,
            'marked_file': marked_filename,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary_message': summary_message,
            'summary_status': summary_status,
            'growth_mindset_analysis': growth_mindset_analysis,
            'quality_analysis': quality_analysis,
            'image_alt_analysis': image_alt_analysis
        }

        # Store scan results in analytics database
        try:
            # Use LLM-extracted metadata (not form inputs)
            instructor_name = None
            department = None
            course_subject = None
            course_number = None
            course_title = None
            semester = None
            metadata_extraction_status = course_metadata.get('status', 'error')

            if course_metadata.get('status') == 'success':
                instructor_name = course_metadata.get('instructor_name')
                department = course_metadata.get('department')
                course_subject = course_metadata.get('course_subject')
                course_number = course_metadata.get('course_number')
                course_title = course_metadata.get('course_title')
                semester = course_metadata.get('semester')

            # Generate summaries for the four key areas
            import re

            # ===== LANGUAGE & TONE (Growth Mindset) - 6 subcategories =====
            language_tone_summary = None
            growth_mindset_score = None
            language_tone_subcategories = {}

            if growth_mindset_analysis.get('status') == 'success':
                analysis_text = growth_mindset_analysis.get('analysis', '')

                # Extract assessments for each of the 6 subcategories
                # Format in LLM output: "## QUESTION N: Title\n**Assessment:** Strong/Moderate/Weak/Not Addressed"
                subcategory_patterns = [
                    (r'(?:QUESTION\s*1|Growth\s*Mindset)[^\n]*\n\**Assessment:?\**\s*(Strong|Moderate|Weak|Not\s*Addressed)', 'Growth Mindset'),
                    (r'(?:QUESTION\s*2|Normalizing\s*Challenge)[^\n]*\n\**Assessment:?\**\s*(Strong|Moderate|Weak|Not\s*Addressed)', 'Normalizing Challenge'),
                    (r'(?:QUESTION\s*3|Instructor\s*Care)[^\n]*\n\**Assessment:?\**\s*(Strong|Moderate|Weak|Not\s*Addressed)', 'Instructor Care'),
                    (r'(?:QUESTION\s*4|Valuing\s*Diversity)[^\n]*\n\**Assessment:?\**\s*(Strong|Moderate|Weak|Not\s*Addressed)', 'Valuing Diversity'),
                    (r'(?:QUESTION\s*5|Normalizing\s*Student\s*Challenges)[^\n]*\n\**Assessment:?\**\s*(Strong|Moderate|Weak|Not\s*Addressed)', 'Normalizing Student Challenges'),
                    (r'(?:QUESTION\s*6|Normalizing\s*Academic\s*Support)[^\n]*\n\**Assessment:?\**\s*(Strong|Moderate|Weak|Not\s*Addressed)', 'Normalizing Academic Support'),
                ]

                for pattern, category in subcategory_patterns:
                    match = re.search(pattern, analysis_text, re.IGNORECASE)
                    if match:
                        assessment = match.group(1).strip().title()
                        # Normalize "Not Addressed" capitalization
                        if 'not' in assessment.lower():
                            assessment = 'Not Addressed'
                        language_tone_subcategories[category] = assessment

                # Count strong/weak for summary
                strong_count = sum(1 for v in language_tone_subcategories.values() if v == 'Strong')
                weak_count = sum(1 for v in language_tone_subcategories.values() if v in ['Weak', 'Not Addressed'])

                if strong_count >= 4:
                    language_tone_summary = f'Strong ({strong_count}/6 areas)'
                elif weak_count >= 3:
                    language_tone_summary = f'Needs work ({weak_count}/6 areas weak)'
                else:
                    language_tone_summary = 'Mixed results'

                # Try to extract overall score if present
                score_match = re.search(r'(?:score|rating|overall)[:\s]*(\d+)(?:/10|\s*out of\s*10)?', analysis_text, re.IGNORECASE)
                if score_match:
                    growth_mindset_score = int(score_match.group(1))

            elif growth_mindset_analysis.get('error'):
                language_tone_summary = 'Analysis unavailable'

            # ===== CLARITY & QUALITY - 4 subcategories =====
            # (Note: LLM may output a 5th "Heading Structure" section, but we ignore it
            # since headings are already covered in accessibility checks)
            clarity_quality_summary = None
            quality_issues_count = 0
            clarity_quality_subcategories = {}

            if quality_analysis.get('status') == 'success':
                analysis_text = quality_analysis.get('analysis', '')

                # Extract issue counts for each of the 4 subcategories
                # Format varies - LLM may output "Term:" or "**Term**:" (bold markdown)
                # Handle both straight quotes ("') and curly/smart quotes (""'')
                sections = [
                    # Section 1: Undefined Terminology - count "Term:" or "**Term**:" entries
                    (r'1\.?\s*UNDEFINED\s*(?:COURSE\s*)?TERMINOLOGY(.*?)(?=\n\s*(?:##\s*)?2\.|$)', 'Undefined Terminology', r'\*?\*?Term\*?\*?\s*:\s*[""\'\']'),
                    # Section 2: Tone Issues - count "Issue:" or "**Issue**:" entries
                    (r'2\.?\s*TONE\s*(?:AND\s*INCLUSIVITY|ISSUES)(.*?)(?=\n\s*(?:##\s*)?3\.|$)', 'Tone Issues', r'\*?\*?Issue\*?\*?\s*:\s*[""\'\']'),
                    # Section 3: Confusing Policies - count "Policy:" or "**Policy**:" entries
                    (r'3\.?\s*(?:POLICIES\s*THAT\s*MAY\s*)?CONFUS(?:ING|E)(.*?)(?=\n\s*(?:##\s*)?4\.|$)', 'Confusing Policies', r'\*?\*?Policy\*?\*?\s*:\s*[""\'\']'),
                    # Section 4: Formatting Inconsistencies - count "Element type:" entries
                    (r'4\.?\s*(?:INCONSISTENT\s*)?FORMAT(?:TING)?(?:\s*INCONSISTENC(?:IES|Y))?(.*?)(?=\n\s*(?:##\s*)?5\.|$)', 'Formatting Inconsistencies', r'\*?\*?Element\s*type\*?\*?\s*:\s*'),
                ]

                for section_pattern, category, issue_pattern in sections:
                    match = re.search(section_pattern, analysis_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        section_text = match.group(1)
                        issues = len(re.findall(issue_pattern, section_text, re.IGNORECASE))
                        clarity_quality_subcategories[category] = issues
                    else:
                        # Section not found, mark as 0
                        clarity_quality_subcategories[category] = 0

                # Calculate total and summary
                quality_issues_count = sum(clarity_quality_subcategories.values())
                categories_with_issues = sum(1 for v in clarity_quality_subcategories.values() if v > 0)

                if quality_issues_count == 0:
                    clarity_quality_summary = 'Excellent clarity'
                elif categories_with_issues == 1:
                    problem_cat = [k for k, v in clarity_quality_subcategories.items() if v > 0][0]
                    clarity_quality_summary = f'{problem_cat}: {quality_issues_count} issue(s)'
                else:
                    clarity_quality_summary = f'{quality_issues_count} issues in {categories_with_issues} areas'

            elif quality_analysis.get('error'):
                clarity_quality_summary = 'Analysis unavailable'

            # Generate accessibility summary from top issues
            accessibility_summary = None
            if category_counts:
                top_issues = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                if top_issues:
                    accessibility_summary = '; '.join([f"{cat}: {count}" for cat, count in top_issues])

            analytics_db.store_scan_result(
                filename=filename,
                instructor_name=instructor_name,
                department=department,
                course_subject=course_subject,
                course_number=course_number,
                course_title=course_title,
                semester=semester,
                total_issues=total_web_issues,
                missing_sections=missing_sections,
                category_counts=category_counts,
                growth_mindset_status=growth_mindset_analysis.get('status'),
                growth_mindset_score=growth_mindset_score,
                quality_analysis_status=quality_analysis.get('status'),
                quality_issues_count=quality_issues_count,
                language_tone_summary=language_tone_summary,
                clarity_quality_summary=clarity_quality_summary,
                accessibility_summary=accessibility_summary,
                metadata_extraction_status=metadata_extraction_status,
                language_tone_subcategories=language_tone_subcategories,
                clarity_quality_subcategories=clarity_quality_subcategories
            )
        except Exception as db_error:
            # Don't fail the request if analytics storage fails
            print(f"Analytics storage error: {db_error}")

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

# ============================================================
# ADMIN ANALYTICS ROUTES
# ============================================================

@app.route('/admin/analytics')
def admin_analytics():
    """Admin analytics dashboard"""
    # Get filter parameters
    department_filter = request.args.get('department', '')
    dept_param = department_filter if department_filter else None

    # Get overview statistics
    stats = analytics_db.get_overview_stats(dept_param)

    # Get four areas summary
    four_areas = analytics_db.get_four_areas_summary(dept_param)

    # Get common issues (accessibility)
    common_issues = analytics_db.get_common_issues(limit=10, department=dept_param)

    # Get trends by month
    trends = analytics_db.get_trends_by_month(months=6, department=dept_param)

    # Get growth mindset trends
    growth_mindset_trends = analytics_db.get_growth_mindset_trends(months=6, department=dept_param)

    # Get quality analysis trends
    quality_trends = analytics_db.get_quality_analysis_trends(months=6, department=dept_param)

    # Get language & tone breakdown
    language_tone_breakdown = analytics_db.get_language_tone_breakdown(dept_param)

    # Get clarity & quality breakdown
    clarity_quality_breakdown = analytics_db.get_clarity_quality_breakdown(dept_param)

    # Get subcategory statistics for detailed breakdowns
    language_tone_subcategories = analytics_db.get_language_tone_subcategory_stats(dept_param)
    clarity_quality_subcategories = analytics_db.get_clarity_quality_subcategory_stats(dept_param)

    # Get department summary
    department_summary = analytics_db.get_department_summary()

    # Get missing sections frequency
    missing_sections_freq = analytics_db.get_missing_sections_frequency()

    # Get list of departments for filter dropdown
    departments = analytics_db.get_departments_list()

    # Get recent scans
    recent_scans = analytics_db.get_all_scans(limit=25, department=dept_param)

    return render_template('admin_analytics.html',
                           stats=stats,
                           four_areas=four_areas,
                           common_issues=common_issues,
                           trends=trends,
                           growth_mindset_trends=growth_mindset_trends,
                           quality_trends=quality_trends,
                           language_tone_breakdown=language_tone_breakdown,
                           clarity_quality_breakdown=clarity_quality_breakdown,
                           language_tone_subcategories=language_tone_subcategories,
                           clarity_quality_subcategories=clarity_quality_subcategories,
                           department_summary=department_summary,
                           missing_sections_freq=missing_sections_freq,
                           departments=departments,
                           department_filter=department_filter,
                           recent_scans=recent_scans)

@app.route('/admin/analytics/delete', methods=['POST'])
def admin_analytics_delete():
    """Delete selected scan entries"""
    try:
        # Get scan IDs from form
        scan_ids = request.form.getlist('scan_ids')

        if not scan_ids:
            flash('No scans selected for deletion', 'warning')
            return redirect(url_for('admin_analytics'))

        # Convert to integers
        scan_ids = [int(id) for id in scan_ids]

        # Delete the scans
        deleted_count = analytics_db.delete_scans(scan_ids)

        flash(f'Successfully deleted {deleted_count} scan(s)', 'success')

    except Exception as e:
        flash(f'Error deleting scans: {str(e)}', 'error')

    # Preserve department filter if present
    department = request.form.get('department_filter', '')
    if department:
        return redirect(url_for('admin_analytics', department=department))
    return redirect(url_for('admin_analytics'))

if __name__ == '__main__':
    # Clean up temp folder on exit
    import atexit
    atexit.register(lambda: shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True))

    # Run the app (using port 5001 to avoid macOS AirPlay conflict)
    app.run(debug=True, host='0.0.0.0', port=5001)

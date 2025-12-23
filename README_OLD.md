# Syllabus Accessibility Checker

A web application that checks course syllabi for accessibility issues based on WCAG guidelines and best practices. Upload a syllabus and receive a detailed report with issues organized by category, plus a marked-up document showing where issues occur.

## Features

### Section Completeness
- Identifies missing required sections from the UWM template
- Searches for sections both in document body and within table cells

### Algorithmic Accessibility Checks

The tool performs the following automated accessibility checks:

**Table-Related Issues:**
- **Layout Tables**: Detects tables used for layout instead of tabular data using heuristics:
  - Single column/row tables
  - High percentage of empty cells
  - Inconsistent cell content lengths
  - Label-value patterns (two-column with short labels and long descriptions)
- **Table Headers**: Identifies data tables missing proper header rows
- **Empty Table Rows/Columns**: Detects empty rows or columns used for spacing (bad practice)
- **Table Complexity**: Flags tables with excessive text or size

**Text and Formatting Issues:**
- **Pseudo-Tables**: Detects use of tabs or multiple spaces to create columnar alignment (inaccessible for screen readers)
- **Font Sizes**: Identifies text below 11pt (minimum accessible size)
- **Manual Formatting**: Detects excessive manual bold formatting used as section headers
- **Underlined Non-Links**: Flags underlined text that is not a hyperlink (confusing for users)
- **Manual List Formatting**: Checks for manual bullets/numbers instead of built-in list styles

**Links and Media:**
- **Hyperlink Accessibility**: Verifies descriptive link text vs. raw URLs
- **Image Alt Text**: Alerts to verify alt text for images

**Document Metadata:**
- **Missing Title**: Checks for document title in metadata properties

### What This Tool Does NOT Check

**Semantic/Content Checks** (better suited for LLM analysis):
- Whether text should semantically be a heading
- Heading hierarchy appropriateness
- Quality of headings or alt text
- Readability or jargon
- Content quality or completeness

These require understanding document meaning and context, which is beyond algorithmic pattern matching.

## Key Features

- **Analyzes content everywhere** - Finds issues in both document body and table cells
- **Labels issues in place** - Creates a marked Word document with `[← ISSUE_TYPE]` labels and yellow highlighting
- **Auto-generates standardized output files** - Consistent naming based on input file
- **Single command operation** - No need to specify the template every time

## Requirements

- Python 3.7+
- python-docx library (installed in the virtual environment)

## Installation

The project includes a virtual environment with all dependencies installed. To activate it:

```bash
source venv/bin/activate
```

If you need to install dependencies manually:

```bash
pip install python-docx
```

## Usage

### Quick Start

Simply run the checker on any syllabus file:

```bash
source venv/bin/activate
python3 syllabus_checker.py YOUR_SYLLABUS.docx
```

The script automatically:
- Uses `Uniform-Syllabus-Template-1.docx` as the template
- Creates `YOUR_SYLLABUS_report.txt` - Comprehensive text report
- Creates `YOUR_SYLLABUS_marked.docx` - Word document with issues labeled and highlighted

**Example:**
```bash
python3 syllabus_checker.py spilka/spilka_205.docx
```

**Output:**
- `spilka/spilka_205_report.txt` - Text report with all issues and locations
- `spilka/spilka_205_marked.docx` - Word doc with issues labeled (e.g., `[← PSEUDO_TABLE]`)

### Advanced Options

**Use a different template:**
```bash
python3 syllabus_checker.py my_syllabus.docx -t path/to/custom_template.docx
```

**Get help:**
```bash
python3 syllabus_checker.py --help
```

## Understanding the Report

The tool generates a comprehensive report with the following sections:

### Document Statistics
Shows total paragraphs analyzed, including those in tables vs. top-level.

### Section Completeness
Lists all required sections that are missing from the syllabus:
- Course Title & Basic Information
- Instructor Information
- Welcome Statement
- Course Overview & Objectives
- Student Learning Outcomes
- Assessment Information
- Prerequisites
- Course Modality & Format
- Course Materials
- Grading Scheme & Scale
- Course Policies
- University Policies
- Resources & Academic Supports
- Important Dates & Calendar

### Accessibility Checks

**Heading Structure**: Reports on actual heading usage (Heading 1, Heading 2, etc.) found in the document. Note: The tool does NOT attempt to determine if text should be a heading - this requires semantic understanding better suited for LLM analysis.

**Table Headers**: Identifies data tables that lack proper header rows. Screen readers rely on table headers to understand table structure.

**Layout vs. Data Tables**: Distinguishes between tables used for layout (bad for accessibility) and tables containing actual tabular data. Uses heuristics including:
- Single column/row detection
- Cell content length analysis
- Empty cell percentage
- Label-value pattern recognition
- Content variance analysis

**Table Usage**: Identifies excessive or improper table usage that can harm accessibility.

**Empty Table Rows/Columns**: Detects completely empty rows or columns used for spacing (should use proper table formatting instead).

**Manual Alignment (Pseudo-Tables)**: Flags use of tabs or multiple spaces to create columnar layouts. This creates "pseudo-tables" that screen readers cannot parse correctly. Proper tables should be used instead.

**Font Sizes**: Identifies text with font size below 11pt (minimum accessible size for body text).

**Text Formatting**: Detects manual bold formatting that may be used as section headers.

**List Formatting**: Checks for proper use of built-in list styles vs. manual bullet points.

**Underlined Text**: Flags underlined text that is not a hyperlink (users expect underlined text to be clickable).

**Document Metadata**: Checks for missing document title in properties (important for accessibility and document management).

**Hyperlinks**: Verifies that hyperlinks use descriptive text rather than displaying raw URLs.

**Images**: Alerts you to verify alt text for any images in the document.

### Report Symbols

- `[X]` - Issue found that needs attention
- `[!]` - Warning (minor issues)
- `[OK]` - Check passed
- `[i]` - Informational note

## Example Output

```
================================================================================
SYLLABUS ASSESSMENT REPORT
================================================================================

DOCUMENT STATISTICS
--------------------------------------------------------------------------------
Total paragraphs analyzed: 131
  - Top-level paragraphs: 131
  - Paragraphs in tables: 0
Total tables: 0

SECTION COMPLETENESS
--------------------------------------------------------------------------------
[X] MISSING 15 REQUIRED SECTIONS:
  - Course Title
  - Welcome Statement
  - Course Overview
  ...

ACCESSIBILITY: HEADING STRUCTURE
--------------------------------------------------------------------------------
Heading usage:
  - Heading 1: 4
  - Heading 2: 7
[OK] Heading structure looks good

ACCESSIBILITY: TABLE HEADERS
--------------------------------------------------------------------------------
[OK] No tables to check

ACCESSIBILITY: LAYOUT vs. DATA TABLES
--------------------------------------------------------------------------------
[OK] No tables to check

ACCESSIBILITY: MANUAL ALIGNMENT (PSEUDO-TABLES)
--------------------------------------------------------------------------------
[X] Found 5 paragraph(s) using tabs or spaces for alignment:
    (This creates pseudo-tables that are difficult for screen readers to parse)
  - Paragraph 85: Uses tabs for columnar alignment: "January 6	Business..."
  - Paragraph 90: Uses tabs for columnar alignment: "January 7	Proposal..."
  ...

ACCESSIBILITY: FONT SIZES
--------------------------------------------------------------------------------
[OK] All text meets minimum font size requirements

ACCESSIBILITY: EMPTY TABLE ROWS/COLUMNS
--------------------------------------------------------------------------------
[OK] No tables to check

ACCESSIBILITY: DOCUMENT METADATA
--------------------------------------------------------------------------------
[OK] Document has title metadata

ACCESSIBILITY: UNDERLINED TEXT
--------------------------------------------------------------------------------
[X] Found 6 underlined text(s) that are not hyperlinks:
    (Underlined text is often confused with links by users)
  - Paragraph 25: Underlined text that is not a hyperlink: "Because all..."
  ...

SUMMARY
--------------------------------------------------------------------------------
[X] This syllabus has 11 issues that need attention.
```

## Understanding the Marked Document

The `_marked.docx` file contains:
- **Yellow highlighting** on problematic text
- **Red labels** at the end of problematic paragraphs, like:
  - `[← PSEUDO_TABLE]` - Uses tabs/spaces for alignment
  - `[← SMALL_FONT]` - Font size below 11pt
  - `[← UNDERLINE_NON_LINK]` - Underlined but not a link
  - `[← LAYOUT_TABLE]` - Table used for layout
  - `[← TABLE_NO_HEADER]` - Table missing headers
  - `[← EMPTY_TABLE_ROW]` - Empty table row
  - `[← EMPTY_TABLE_COLUMN]` - Empty table column

Issues are **labeled, not fixed** - you review and fix them manually.

## Recommendations

Based on the assessment, the tool provides actionable recommendations:

1. Add all missing required sections from the template
2. Avoid using tables for layout; use headings and paragraphs instead
3. Ensure all data tables have proper header rows
4. Remove empty table rows/columns; use proper spacing/padding instead
5. Replace pseudo-tables (tabs/spaces) with proper tables or formatting
6. Ensure all text is at least 11pt
7. Remove underlines from non-link text (use bold or italics for emphasis)
8. Use descriptive hyperlink text instead of displaying URLs
9. Ensure all images have descriptive alt text
10. Use built-in list formatting instead of manual bullets
11. Add document title in metadata (File > Info > Properties)

## Files in This Project

- **`syllabus_checker.py`** - The main script
- `Uniform-Syllabus-Template-1.docx` - The UWM template (used as default)
- `spilka/` - Example syllabi directory
- `english215/` - Example syllabi directory
- `venv/` - Virtual environment with dependencies
- `README.md` - Full documentation
- `QUICK_START.md` - Quick reference guide
- `MARKED_DOCUMENT_GUIDE.md` - Guide to understanding marked documents
- `todo.md` - Comprehensive list of potential future checks

## Technical Details

The tool uses the `python-docx` library to parse Word documents and extract:
- Document structure (headings, paragraphs, tables)
- Style information
- Text formatting details (font size, bold, underline, etc.)
- Table structure (rows, columns, cells)
- Hyperlinks and images
- Document metadata

It performs algorithmic checks based on WCAG guidelines and accessibility best practices, focusing on issues that can be reliably detected through pattern matching rather than semantic understanding.

## Customization

To modify the required sections, edit the `REQUIRED_SECTIONS` dictionary in `syllabus_checker.py`:

```python
REQUIRED_SECTIONS = {
    "Section Name": ["search", "terms", "to", "match"],
    ...
}
```

## Future Enhancements

See `todo.md` for a comprehensive list of potential checks. Many semantic checks (e.g., determining if text should be a heading, evaluating heading quality, assessing readability) are better suited for LLM-based analysis rather than algorithmic detection.

## Support

For questions or issues with the script, contact Dave Clark (dclark@uwm.edu)

## License

This tool is provided for use by UWM faculty and staff to ensure syllabus compliance with university standards.

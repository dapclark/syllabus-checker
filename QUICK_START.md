# Syllabus Checker - Quick Start Guide

## TL;DR - Just Want to Check a Syllabus?

```bash
cd /Users/dclark/Documents/syllabus_checker
source venv/bin/activate
python3 syllabus_checker.py YOUR_SYLLABUS.docx
```

That's it! The script automatically:
- Uses `Uniform-Syllabus-Template-1.docx` as the template
- Creates `YOUR_SYLLABUS_report.txt` - Detailed text report with all issues
- Creates `YOUR_SYLLABUS_marked.docx` - Word doc with table issues highlighted

Example:
```bash
python3 syllabus_checker.py english215.docx
```
Creates: `english215_report.txt` and `english215_marked.docx`

---

## What Gets Checked?

### Missing Sections (20 Required Sections)
- Course Title, Instructor Info, Welcome Statement
- Course Overview, Objectives, Learning Outcomes
- Assessment, Prerequisites, Modality, Materials
- Time Investment, Assignments & Grading, Policies
- Resources, Important Dates, Calendar

### Accessibility Issues

**Headings**
- ✓ Detects bold/caps text that should be Heading styles
- ✓ Checks heading hierarchy (H1, H2, H3, etc.)

**Tables**
- ✓ Identifies missing table headers
- ✓ Detects tables used for layout (accessibility violation)
- ✓ Flags tables with excessive text

**Other**
- ✓ Manual formatting vs. proper styles
- ✓ List formatting
- ✓ Hyperlink text
- ✓ Image alt text reminders

---

## Command Options

### Standard usage (RECOMMENDED)
```bash
python3 syllabus_checker.py your_syllabus.docx
```
Automatically creates both text report and marked document.

### Use a different template
```bash
python3 syllabus_checker.py your_syllabus.docx -t path/to/custom_template.docx
```

### See all options
```bash
python3 syllabus_checker.py --help
```

---

## Understanding the Marked Document

When you open the marked document in Word, you'll see:

- **Yellow highlighting** on problematic text
- **Red text markers** like:
  - `[ISSUE: UNSTYLED_HEADING]` - This text should use a Heading style
  - `[TABLE ISSUE: ...]` - Problems with table structure/usage

---

## Common Issues Found

| Issue | What It Means | How to Fix |
|-------|---------------|------------|
| UNSTYLED_HEADING | Bold/caps text acting as heading | Select text → Apply Heading 1 or Heading 2 style |
| TABLE_NO_HEADER | Table missing header row | Make first row bold or use Table Design → Header Row |
| LAYOUT_TABLE | Table used for layout | Replace table with Heading + paragraphs |
| Manual bold formatting | Using bold instead of styles | Use Heading styles instead |

---

## Tips

1. **Always activate the virtual environment first**: `source venv/bin/activate`
2. **Use the marked document** to quickly find and fix issues in Word
3. **Use the text report** for a comprehensive overview
4. **Fix headings first** - they're the foundation of accessibility
5. **Replace layout tables** with proper headings and paragraphs

---

## Need Help?

See `README.md` for full documentation or contact Dave Clark (dclark@uwm.edu)

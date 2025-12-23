# Understanding the Marked Document

## What to Look For

When you open the marked Word document, you'll see issues highlighted in two ways:

### 1. Cell/Paragraph Issues
**Appearance:**
- Red text: `>>> UNSTYLED_HEADING <<<` (or other issue type)
- Yellow highlighting on the problematic content
- Appears at the very beginning of the affected cell or paragraph

**Example:**
```
┌─────────────────────────────────────┐
│ >>> UNSTYLED_HEADING <<<            │ ← Red marker
│ Instructor                          │ ← Yellow highlighted
│                                     │
└─────────────────────────────────────┘
```

### 2. Table-Level Issues
**Appearance:**
- Red text: `*** TABLE ISSUE: [description] ***`
- Bright green highlighting
- Appears at the top of the table (in first cell)

**Example:**
```
┌─────────────────────────────────────────────────────┐
│ *** TABLE ISSUE: Table 1 appears to be used for  │ ← Red on green
│ layout (25/38 empty cells)... ***                │
│                                                   │
│ [rest of table content]                           │
└─────────────────────────────────────────────────────┘
```

## Issue Types You'll See

### >>> UNSTYLED_HEADING <<<
- **Problem:** Text is bold/caps/large but doesn't use proper Heading styles
- **Fix:** Select the text, then apply Heading 1 or Heading 2 style from the Styles menu

### *** TABLE ISSUE: Layout table ***
- **Problem:** Table is being used for page layout instead of tabular data
- **Fix:** Remove the table and use Heading styles + regular paragraphs instead

### *** TABLE ISSUE: No header row ***
- **Problem:** Data table doesn't have a clear header row
- **Fix:** Make the first row bold or use Table Design > Header Row option

## Statistics for Your Example

Your `english215.docx` has:
- **37 total issues** detected
- **25 marked locations** in the document
  - 1 top-level paragraph with issues
  - 23 table cells with issues
  - 1 table with table-level issues

Note: Some cells contain multiple issues of the same type (e.g., 6 unstyled headings in one cell). These show as a single marker per cell to avoid clutter.

## How to Use the Marked Document

1. **Open in Word:** `english215_marked.docx`
2. **Scroll through and look for:**
   - Yellow highlighting (individual issues)
   - Green highlighting (table-level issues)
   - Red text markers showing issue types
3. **Fix each issue:**
   - Read the text report for detailed explanations
   - Use the marked document to quickly locate problems
   - Apply the appropriate fixes
4. **Re-run the checker** to verify all issues are resolved

## Color Legend

| Color | Meaning |
|-------|---------|
| 🟨 Yellow highlight | Content with accessibility issues |
| 🟩 Bright green highlight | Table-level structural issues |
| 🔴 Red text | Issue type markers |

## Common Questions

**Q: Why do I see fewer markers than issues in the report?**
A: When a single cell/paragraph has multiple issues of the same type, we show one marker per location (not one per issue) to keep it readable.

**Q: What's the difference between yellow and green highlighting?**
A: Yellow = specific content issues (like unstyled headings). Green = structural table problems (like using tables for layout).

**Q: Can I ignore some issues?**
A: The text report explains why each issue matters for accessibility. Focus on the critical ones first (unstyled headings, layout tables).

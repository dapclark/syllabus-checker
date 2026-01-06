# Syllabus Checker - Comprehensive TODO & Implementation Guide

## 📊 Progress Summary

### Implemented Features
- ✅ **44+ Algorithmic Accessibility Checks** - Font sizes, spacing, tables, links, lists, etc.
- ✅ **Enhanced Heading Analysis** - Hierarchy, ALL CAPS, length, position, multiple H1 detection
- ✅ **AI-Powered Growth Mindset Analysis** - 6-question framework with ready-to-use text
- ✅ **AI-Powered Quality Analysis** - 5 key areas: terminology, tone, policies, formatting, heading structure
- ✅ **Smart Placement System** - Inserts AI recommendations into appropriate syllabus sections

### Key Achievements
- Combined programmatic + LLM approach for comprehensive analysis
- Reduced false positives through smart detection algorithms
- Added actionable, ready-to-use recommendations
- Implemented full markdown-to-HTML rendering for LLM output

---

## Legend
- ✅ = Currently Implemented (algorithmic or LLM-based check)
- ⏳ = Not Yet Implemented (but feasible)
- N/A = Out of scope for this tool

---

## 1. Document Structure, Semantics, and Reading Order

**Why this matters:**
Assistive technologies (screen readers, braille displays, keyboard navigation) rely on semantic structure, not visual appearance. Improper heading hierarchy, pseudo-lists, and layout tables disrupt navigation and comprehension.

**Key references:**
- WCAG 2.1 / 2.2 - https://www.w3.org/WAI/standards-guidelines/wcag/
  (SC 1.3.1 Info and Relationships, 1.3.2 Meaningful Sequence, 2.4.6 Headings and Labels)
- W3C – Document Semantics - https://www.w3.org/TR/html52/semantics.html
- Deque University – Headings, Lists, and Tables - https://dequeuniversity.com/

### Headings and Hierarchy
- ✅ Detect heading level inconsistencies (e.g., skipping levels) - **Programmatic check**
- ✅ Identify headings created using styling but not semantic heading tags - **LLM Quality Analysis**
- ✅ Flag headings written in ALL CAPS - **Programmatic check**
- ✅ Flag headings styled manually (bold/size changes) instead of heading styles - **LLM Quality Analysis**
- ✅ Flag overly long or non-descriptive headings - **Programmatic (length) + LLM (descriptiveness)**
- ✅ Ensure a single Heading 1 exists and appears at the top - **Programmatic check**

### Lists
- ✅ Detect lists created manually using tabs, hyphens, or numbers instead of proper list structures
- ✅ Flag incorrect or inconsistent nested list hierarchy
- ✅ Identify lists used for layout or indentation rather than semantic grouping

### Tables
- ✅ Detect tables used for formatting/layout rather than data
- ✅ Identify missing header rows
- ✅ Flag tables missing proper scope declarations on header cells
- ✅ Detect missing captions or table descriptions
- ✅ Identify empty rows/columns used for spacing
- ✅ Detect merged or split cells impacting reading order
- ✅ Flag inconsistent or illogical table reading order
- ✅ Identify non-left-aligned numeric data inconsistently applied
- ✅ Detect color-coded meaning in cells without textual explanation
- ✅ Identify images embedded inside table cells when text should be used

---

## 2. Typography, Emphasis, and Visual Formatting

**Why this matters:**
Poor typography disproportionately affects users with dyslexia, low vision, cognitive disabilities, and those using screen magnification.

**Key references:**
- WCAG 1.4.8 – Visual Presentation - https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html
- British Dyslexia Association – Dyslexia-Friendly Style Guide - https://www.bdadyslexia.org.uk/
- National Center on Accessible Educational Materials (AEM) - https://aem.cast.org/

### Capitalization and Emphasis
- ✅ Flag ALL CAPS used for large blocks of text (50+ characters)
- ✅ Detect excessive or inconsistent use of bold, italics, or underline
- ✅ Identify underlining applied to non-hyperlink text
- ✅ Manual bold formatting (excessive use)

### Fonts and Spacing
- ✅ Detect inaccessible or decorative fonts
- ✅ Flag font sizes below 11 pt for body text
- ✅ Identify inconsistent font families
- ✅ Detect insufficient line spacing (below 1.15)
- ✅ Detect spacing or line breaks used for layout/positioning (pseudo-tables)
- ✅ Flag full justification of text

---

## 3. Color, Contrast, and Non-Text Meaning

**Why this matters:**
Color-only meaning excludes users with color-vision deficiencies and those using high-contrast or monochrome modes.

**Key references:**
- WCAG 1.4.1 – Use of Color - https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html
- WCAG 1.4.3 / 1.4.11 – Contrast - https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- WebAIM – Color & Contrast - https://webaim.org/articles/contrast/

### Checks
- ✅ Detect insufficient color contrast based on WCAG thresholds
- ✅ Flag color used as the sole means of conveying meaning
- ✅ Identify text placed over backgrounds/images without readable contrast

---

## 4. Images, Alt Text, and Non-Text Content

**Why this matters:**
Images without meaningful alt text cause information loss. Screenshots of text are inaccessible to assistive technology.

**Key references:**
- WCAG 1.1.1 – Non-text Content - https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html
- DIAGRAM Center – Image Description Guidelines - https://diagramcenter.org/
- Penn State Accessibility – Alt Text Decision Tree - https://accessibility.psu.edu/images/

### Checks
- ✅ Detect images missing alt text
- ✅ Identify alt text that is too short, irrelevant, or redundant (e.g., "Image of…") - **LLM-powered Image Alt Text Analysis**
- ✅ Identify decorative images missing decorative marking
- ✅ Detect screenshots replacing text content (e.g., schedules, tables)
- ✅ Flag institutional logos without meaningful alt text - **LLM-powered Image Alt Text Analysis**
- ✅ Image presence check (alerts to verify alt text)

---

## 5. Links, Navigation, and Wayfinding

**Why this matters:**
Screen-reader users often navigate by links alone. Non-descriptive link text and missing navigation increase cognitive load.

**Key references:**
- WCAG 2.4.4 – Link Purpose - https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context.html
- WCAG 2.4.5 – Multiple Ways - https://www.w3.org/WAI/WCAG21/Understanding/multiple-ways.html
- Usability.gov – Navigation and Links - https://www.usability.gov/

### Checks
- ✅ Flag hyperlinks with non-descriptive text (e.g., "click here")
- ✅ Identify links styled as normal text (missing underline/color)
- ✅ Identify underlined non-link text
- ✅ Detect excessively long URLs
- ✅ Detect missing table of contents in longer documents
- ✅ Detect missing internal navigation/bookmarks

---

## 6. Language, Readability, and Policy Clarity

**Why this matters:**
Complex language, inconsistent terminology, and unclear policies disproportionately affect first-generation, international, and neurodivergent students.

**Key references:**
- Plain Language Association International - https://plainlanguagenetwork.org/
- CAST – Universal Design for Learning (UDL) - https://www.cast.org/impact/universal-design-for-learning-udl
- Council for Exceptional Children - https://exceptionalchildren.org/

### Readability
- ✅ Detect overly long sentences (>35 words)
- ✅ Flag complex language or jargon without definitions - **LLM Quality Analysis**
- ✅ Detect inconsistent terminology - **LLM Quality Analysis**

### Accessibility & Inclusion Statements
- ⏳ Detect missing legally-required disability accommodation statements - **Future LLM enhancement**
- ⏳ Identify outdated or institutionally incorrect policy language - **Future LLM enhancement**
- ✅ Flag ambiguous, discouraging, or inaccessible policy instructions - **LLM Quality Analysis**

### Course Calendar and Schedule
- ✅ Identify schedules provided as images instead of text
- ✅ Detect unclear date formats (e.g., numeric-only dates)
- ✅ Identify merged table cells used to create visual layouts

---

## 7. File-Level Accessibility, Metadata, and PDFs

**Why this matters:**
Documents without proper metadata or tagged PDFs are often unreadable to assistive technologies.

**Key references:**
- PDF Accessibility (WCAG & Techniques) - https://www.w3.org/WAI/standards-guidelines/pdf/
- PDF/UA (ISO 14289) - https://www.pdfa.org/resource/pdfua/
- Adobe – Create Accessible PDFs - https://www.adobe.com/accessibility/products/acrobat/pdf.html

### Checks
- ✅ Detect missing document title/metadata tags
- ✅ Detect missing or incorrect document language setting
- ✅ Identify multiple languages without proper tagging
- ✅ Identify untagged mathematical expressions

---

## 8. Pedagogical Integrity and Syllabus-Specific Requirements

**Why this matters:**
A syllabus functions as a contract, roadmap, and accessibility gateway. Missing or unclear elements directly affect student success and equity.

**Key references:**
- AAC&U – Essential Learning Outcomes - https://www.aacu.org/
- Quality Matters – Course Design Standards - https://www.qualitymatters.org/
- Student Experience Project - https://studentexperienceproject.org/

### Required Content
- ✅ Identifying missing required syllabus elements (instructor info, outcomes, assessment breakdown)

### Quality and Clarity (LLM-Powered)
- ✅ Detecting undefined course terminology - **LLM Quality Analysis**
- ✅ Flagging tone and inclusivity issues in policy language - **LLM Quality Analysis**
- ✅ Highlighting policies that may violate accessibility guidance or confuse students - **LLM Quality Analysis**
- ✅ Detect inconsistent formatting across repeated syllabus elements - **LLM Quality Analysis**

### Growth Mindset and Belonging (LLM-Powered)
- ✅ Evaluate growth mindset communication - **LLM Growth Mindset Analysis**
- ✅ Check instructor approachability messaging - **LLM Growth Mindset Analysis**
- ✅ Evaluate diversity and belonging cues - **LLM Growth Mindset Analysis**
- ✅ Analyze resource connection language - **LLM Growth Mindset Analysis**
- ✅ Check normalization of challenges and academic support - **LLM Growth Mindset Analysis**
- ✅ Provide ready-to-use text with placement guidance - **Smart Placement System**

### Other Quality Checks
- ✅ Identify copied content with broken or inconsistent style application
- ✅ Flag footnotes used instead of inline explanations
- ✅ Detect visual indicators of due dates or significance without text equivalents
- ✅ Identify math expressions not using accessible markup (MathML or equivalent)

---

## Summary of Current Implementation

### Algorithmic Checks: 50+
1. Section Completeness (1)
2. Headings (6)
3. Tables (10)
4. Lists (2)
5. Typography & Text (8)
6. Color & Contrast (3)
7. Links & Navigation (6)
8. Document Properties (3)
9. Readability (2)
10. Images (4)
11. Content Quality (4)

### LLM-Powered Features: 3 Major Systems

#### Growth Mindset and Belonging Analysis
- Evaluates 6 core questions from Student Experience Project research
- Provides ready-to-use text for improvements
- Smart placement into appropriate syllabus sections

#### Syllabus Quality Analysis
- Undefined Course Terminology
- Tone and Inclusivity Issues
- Potentially Confusing Policies
- Inconsistent Formatting
- Heading Structure Issues

#### Image Alt Text Analysis
- Flags institutional logos without meaningful alt text
- Identifies poor quality alt text (too short, redundant, irrelevant, non-descriptive)
- Provides specific recommendations for improved alt text

---

## Future Enhancements (Priority Order)

### High Priority
1. **Content Quality & Completeness**
   - Check if section content is substantive or just placeholders
   - Detect boilerplate text needing customization
   - Verify required sections have meaningful content

2. **Date & Schedule Validation**
   - Validate dates are reasonable
   - Check calendar completeness
   - Detect placeholder dates

3. **Policy & Template Compliance**
   - Verify specific institutional policy statements
   - Check for contradictions in policies
   - Verify consistency across sections

### Medium Priority
4. **Section Organization & Flow**
   - Verify logical section ordering
   - Detect redundancy across sections
   - Suggest section consolidation or splitting

5. **Contact Information Completeness**
   - Verify instructor contact info is complete
   - Check if contact methods are accessible

6. **Learning Outcomes Alignment**
   - Check if assessments align with learning outcomes
   - Verify outcomes are measurable

### Advanced Features
7. **Cross-Reference Validation**
   - Verify all assignments in grading appear in schedule
   - Check percentage totals add to 100%

8. **Screen Reader Simulation**
   - Simulate screen reader experience
   - Detect "here" references needing context

9. **Workload Estimation**
   - Estimate time investment based on assignments
   - Flag potential overload situations

---

## Implementation Notes
- Algorithmic checks enforce explicit, testable accessibility rules
- LLM-based checks address meaning, tone, clarity, and consistency
- Combined approach provides comprehensive analysis with minimal false positives
- Each rule is implemented as a discrete, versioned check
- All LLM recommendations include actionable guidance

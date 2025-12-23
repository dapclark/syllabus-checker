# Syllabus Checker - Function Analysis & Enhancement Roadmap

## Current Algorithmic Functions (Implemented)

### Section Analysis
- ✅ **check_missing_sections()** - Detects missing required syllabus sections
  - Uses keyword matching against template
  - Checks both top-level and table paragraphs

### Heading Analysis
- ✅ **check_heading_structure()** - Analyzes heading usage and counts
  - Counts headings by level (H1, H2, etc.)
  - Smart H1 count warning (only if >10 H1s with <3 H2s, or >15 H1s total)
  - Detects missing H1s
  - ~~Disabled: check_unstyled_headings()~~ (too many false positives, better for LLM)
  - ~~Disabled: check_heading_hierarchy()~~ (too many false positives, better for LLM)

### Table Analysis
- ✅ **check_table_usage()** - General table usage analysis
  - Counts tables
  - Detects cells with excessive text (>500 chars)
  - Smart warnings (only flags >5 tables, not >2)
  - Smart large table detection (only warns if lacks headers)

- ✅ **check_table_headers()** - Detects tables without header rows
  - Enhanced detection: checks bold, shading, large font

- ✅ **check_layout_tables()** - Identifies tables used for layout vs. data
  - Single column/row detection
  - Empty cell percentage (but skips if has headers)
  - Long text cells (but skips if has headers)
  - Inconsistent cell lengths (but skips if has headers)
  - Label-value pattern detection (but skips if has headers)

- ✅ **check_empty_table_rows_columns()** - Detects empty rows/columns used for spacing

### Text Formatting
- ✅ **check_text_formatting()** - Detects manual bold formatting instead of heading styles
  - Smart detection: only flags if >80% bold, <100 chars, no punctuation, starts with capital

- ✅ **check_font_sizes()** - Detects font sizes below 11pt

- ✅ **check_line_spacing()** - Checks for line spacing below 1.15

- ✅ **check_full_justification()** - Detects full text justification

- ✅ **check_all_caps_blocks()** - Detects large blocks (>50 chars) of ALL CAPS text

### List Formatting
- ✅ **check_list_usage()** - Detects manual list items vs. proper list styles

### Manual Alignment
- ✅ **check_manual_alignment()** - Detects pseudo-tables using tabs/spaces

### Hyperlinks
- ✅ **check_hyperlinks()** - Checks for accessible hyperlink practices
  - Detects URL text displayed directly

- ✅ **check_non_descriptive_links()** - Detects "click here", "here", etc.

- ✅ **check_underline_non_links()** - Detects underlined text that isn't a link

### Images & Media
- ✅ **check_images()** - Detects images (prompts user to verify alt text)

### Document Metadata
- ✅ **check_document_metadata()** - Checks for missing document title

---

## Potential LLM-Based Enhancements

### 🤖 HIGH PRIORITY - Natural Language Understanding

#### 1. **LLM-Based Heading Analysis** ⭐⭐⭐
**Why LLM:** Requires semantic understanding of content
- Detect text that should be headings (better than current bold detection)
- Validate heading hierarchy in context
- Suggest appropriate heading levels based on content
- Example: "Course Materials" in a table should be H2, not H1

#### 2. **Content Quality & Completeness** ⭐⭐⭐
**Why LLM:** Requires understanding of educational content
- Check if section content is substantive or just placeholders
  - "TBD", "Coming soon", "See Canvas" without details
  - Empty sections with just a heading
- Verify required sections have meaningful content
  - Does "Assessment" section actually describe assessments?
  - Does "Grading" section include actual grading criteria?
- Detect boilerplate text that needs customization
  - "[Insert course name here]", "XX credits"

#### 3. **Accessibility - Descriptive Text** ⭐⭐⭐
**Why LLM:** Requires understanding of context and clarity
- Evaluate link text descriptiveness
  - Beyond "click here" - is "document" descriptive enough?
  - Suggest better link text: "Course syllabus" vs. "this"
- Check if table captions/headers are descriptive
  - "Table 1" vs. "Grading Scale"
- Verify instructional text is clear and accessible
  - Reading level analysis
  - Jargon detection without explanation

#### 4. **Policy & Template Compliance** ⭐⭐
**Why LLM:** Requires understanding of policy requirements
- Verify specific UWM policy statements are included
  - Exact wording requirements
  - Required disclaimers
- Check for contradictions in policies
  - Late policy says "no late work" but assignment says "submit by..."
- Verify consistency across sections
  - Prerequisites mentioned in overview match prerequisites section

#### 5. **Date & Schedule Validation** ⭐⭐
**Why LLM:** Requires understanding of dates and schedules
- Validate dates are reasonable
  - Due dates fall on class meeting days
  - No assignments due during breaks
  - Dates are in chronological order
- Check calendar completeness
  - All assignments mentioned in grading section appear in calendar
  - All exams have dates
- Detect placeholder dates
  - "TBD", "Week 1", without actual dates

---

### 🤖 MEDIUM PRIORITY - Enhanced Analysis

#### 6. **Tone & Clarity Analysis** ⭐⭐
**Why LLM:** Requires understanding of communication style
- Check tone is welcoming and inclusive
  - Does welcome statement feel welcoming?
  - Is language student-centered?
- Detect overly complex or unclear instructions
- Suggest simpler phrasing for accessibility

#### 7. **Section Organization & Flow** ⭐
**Why LLM:** Requires understanding of document structure
- Verify logical section ordering
  - Prerequisites before course materials?
  - Grading scale before assignments?
- Detect redundancy across sections
  - Same policy stated in multiple places
- Suggest section consolidation or splitting

#### 8. **Contact Information & Office Hours** ⭐
**Why LLM:** Requires understanding of contact formats
- Verify instructor contact info is complete
  - Email, office location, phone
  - Office hours with times and location/mode
- Check if contact methods are accessible
  - Not just phone (accessibility issue)

#### 9. **Learning Outcomes Alignment** ⭐⭐
**Why LLM:** Requires understanding of educational alignment
- Check if assessments align with learning outcomes
  - Do assignments measure stated outcomes?
- Verify outcomes are measurable
  - "Understand" vs. "Demonstrate understanding by..."
- Check outcomes use appropriate Bloom's taxonomy verbs

---

### 🤖 ADVANCED - Sophisticated Analysis

#### 10. **Cross-Reference Validation** ⭐⭐
**Why LLM:** Requires tracking references across document
- Verify all assignments mentioned in grading appear in schedule
- Check percentage totals add to 100%
- Validate cross-references
  - "See section X" actually points to valid section

#### 11. **Accessibility - Screen Reader Simulation** ⭐⭐⭐
**Why LLM:** Requires understanding how screen readers interpret content
- Simulate screen reader experience
  - Would table make sense when read linearly?
  - Are visual cues (colors, formatting) explained in text?
- Detect "here" references that need context
  - "Click here" - here where?

#### 12. **Comparative Analysis with Template** ⭐
**Why LLM:** Requires understanding of structure and style
- Compare section ordering with template
- Detect sections that exist in template but not in syllabus
- Suggest improvements based on template best practices

#### 13. **Equity & Inclusion Check** ⭐⭐
**Why LLM:** Requires understanding of inclusive language
- Detect non-inclusive language
  - Gendered language when neutral is better
  - Culturally-specific references without explanation
- Check for assumptions about student circumstances
  - "Just ask your parents", assumes family support
- Verify accommodation statements are welcoming, not legalistic

#### 14. **Workload Estimation** ⭐
**Why LLM:** Requires understanding of assignment complexity
- Estimate actual time investment based on assignments
- Compare stated time investment with actual requirements
- Flag potential overload situations

---

## Implementation Strategy

### Phase 1: Core LLM Functions (Start Here)
1. **LLM-Based Heading Analysis** - Replace disabled algorithmic version
2. **Content Quality & Completeness** - High value, addresses major gaps
3. **Accessibility - Descriptive Text** - Improves existing accessibility checks

### Phase 2: Policy & Validation
4. **Policy & Template Compliance** - Ensures institutional requirements
5. **Date & Schedule Validation** - Common error source

### Phase 3: Advanced Analysis
6. **Tone & Clarity Analysis** - Improves student experience
7. **Learning Outcomes Alignment** - Pedagogical value
8. **Cross-Reference Validation** - Catches inconsistencies

### Phase 4: Specialized Checks
9. **Equity & Inclusion Check** - Important but requires careful implementation
10. **Screen Reader Simulation** - Advanced accessibility
11. **Workload Estimation** - Nice-to-have

---

## LLM Integration Architecture Considerations

### Option 1: Local LLM (Ollama, LLaMA)
**Pros:**
- Privacy (no data sent externally)
- No API costs
- Fast for multiple documents

**Cons:**
- Requires setup
- May need good hardware
- Model quality varies

### Option 2: Cloud LLM (OpenAI, Anthropic Claude)
**Pros:**
- Best quality analysis
- Easy to use
- No local setup

**Cons:**
- API costs
- Privacy concerns
- Requires internet

### Option 3: Hybrid Approach
- Algorithmic checks for clear-cut issues (current system)
- LLM for ambiguous/semantic analysis
- User configurable (local vs. cloud)

---

## Success Metrics

### For Algorithmic Functions:
- ✅ False positive rate < 5%
- ✅ Processing time < 5 seconds per document
- ✅ No external dependencies

### For LLM Functions:
- 🎯 Useful suggestions > 80%
- 🎯 Processing time < 30 seconds per document
- 🎯 Clear explanation for each suggestion
- 🎯 Actionable recommendations

---

## Notes
- Algorithmic functions should handle clear-cut, rule-based checks
- LLM functions should handle semantic, contextual, ambiguous analysis
- Always prefer algorithmic when possible (faster, cheaper, more reliable)
- LLM should augment, not replace, algorithmic checks

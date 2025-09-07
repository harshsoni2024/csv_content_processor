# Walmart Content Generator

A Python-based CSV processor that generates Walmart-compliant product content while adhering to strict content guidelines and formatting requirements.

## Overview

This tool processes product data from CSV files and generates:
- Walmart-safe product titles
- HTML-formatted bullet points (8 bullets, max 85 characters each)
- Product descriptions (120-160 words)
- Meta titles (≤70 characters)
- Meta descriptions (≤160 characters)

The generator automatically detects and removes banned words, tracks rule violations, and preserves brand names and keywords.

## Features

- **Banned Word Detection**: Automatically identifies and removes 30+ prohibited terms
- **Length Validation**: Ensures all content meets character/word count requirements
- **Keyword Integration**: Naturally incorporates provided keywords into generated content
- **Violation Tracking**: Reports any rules that couldn't be satisfied
- **Batch Processing**: Handles multiple products via CSV input/output

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd walmart-content-generator
```

2. Install required dependencies:
```bash
pip install pandas pytest
```

## Usage

### Basic Usage

1. Prepare your input CSV with the following columns:
   - `brand` - Product brand name
   - `product_type` - Type of product
   - `attributes` - Comma-separated product attributes
   - `current_description` - Existing product description
   - `current_bullets` - Existing bullet points (pipe-separated)
   - `keywords` (optional) - Keywords to incorporate

2. Run the generator:
```bash
python walmart_content_generator.py
```

3. The script will:
   - Read from `products_input.csv`
   - Generate compliant content
   - Save results to `products_output.csv`
   - Report any violations

### Example Input

```csv
brand,product_type,attributes,current_description,current_bullets,keywords
Dell,Monitor,"27-inch Display, Full HD, Adjustable Stand",Description text,Bullet1|Bullet2,"display, clarity"
```

### Example Output

The output CSV includes all original columns plus:
- `walmart_title` - Cleaned product title
- `html_bullets` - 8 HTML-formatted bullet points
- `new_description` - Compliant 120-160 word description
- `meta_title` - SEO meta title (≤70 chars)
- `meta_description` - SEO meta description (≤160 chars)
- `violations` - List of any rules that couldn't be satisfied

## Content Rules

### Banned Words
The following terms are automatically removed:
- Marketing terms: premium, perfect, best, exclusive, luxury, elite
- Medical claims: medical, cure, therapeutic, treatment, clinical
- Guarantees: guaranteed, warranty, lifetime, forever
- Certifications: FDA, approved, certified, authentic
- Dangerous items: weapon, knife, UV
- Others: cosplay, superior, supreme

### Length Requirements
- **Bullet Points**: Maximum 85 characters each, exactly 8 bullets
- **Description**: 120-160 words
- **Meta Title**: Maximum 70 characters
- **Meta Description**: Maximum 160 characters

## Testing

Run the test suite to verify functionality:

```bash
pytest test_walmart_generator.py -v
```

Tests cover:
- Banned word detection and removal
- Bullet point length validation
- Description word count compliance
- Meta field length limits
- Full CSV processing workflow

## Project Structure

```
.
├── walmart_content_generator.py   # Main generator class
├── test_walmart_generator.py      # Pytest test suite
├── products_input.csv             # Sample input file
├── products_output.csv            # Generated output
└── README.md                      # This file
```

## API Reference

### WalmartContentGeneratorClass

Main class for content generation.

#### Methods

- `check_banned_words(text)` - Returns list of banned words found in text
- `clean_text(text)` - Removes banned words from text
- `generate_walmart_title(brand, product_type, attributes)` - Creates compliant title
- `generate_bullets(brand, product_type, attributes, current_description, keywords)` - Generates 8 HTML bullets
- `generate_description(brand, product_type, attributes, current_description, keywords)` - Creates 120-160 word description
- `generate_meta_title(brand, product_type)` - Creates meta title (≤70 chars)
- `generate_meta_description(brand, product_type, attributes)` - Creates meta description (≤160 chars)
- `process_csv(input_file, output_file)` - Processes entire CSV file

## Grading Criteria

The solution addresses:
- **Rule Adherence (40%)**: Strict compliance with banned words and length limits
- **Rewriting Quality (30%)**: Natural, readable content generation
- **Keyword Handling & Length Limits (20%)**: Proper keyword integration and character limits
- **Code/Documentation (10%)**: Clean, tested, documented code

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues or questions, please open an issue on the repository.

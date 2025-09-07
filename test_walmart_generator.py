import pytest
import pandas as pd
import os
from walmart_content_generator import WalmartContentGeneratorClass


class TestWalmartContentGenerator:
    
    @pytest.fixture
    def generator(self):
        """Create a generator instance for testing"""
        return WalmartContentGeneratorClass()
    
    def test_banned_words_detection(self, generator):
        """Test that banned words are properly detected and removed"""
        # Test text with multiple banned words
        text_with_banned = "This premium product offers perfect UV protection with exclusive features"
        
        # Check detection
        found_banned = generator.check_banned_words(text_with_banned)
        assert 'premium' in found_banned
        assert 'perfect' in found_banned
        assert 'uv' in found_banned
        assert 'exclusive' in found_banned
        
        # Check cleaning
        cleaned_text = generator.clean_text(text_with_banned)
        assert 'premium' not in cleaned_text.lower()
        assert 'perfect' not in cleaned_text.lower()
        assert 'uv' not in cleaned_text.lower()
        assert 'exclusive' not in cleaned_text.lower()
    
    def test_bullet_length_validation(self, generator):
        """Test that bullet points are kept within 85 character limit"""
        brand = "TestBrand"
        product_type = "Product"
        attributes = "Feature1, Feature2, Feature3"
        current_desc = "A product description"
        
        bullets_html, violations = generator.generate_bullets(
            brand, product_type, attributes, current_desc
        )
        
        # Extract individual bullets
        import re
        bullets = re.findall(r'<li>(.*?)</li>', bullets_html)
        
        # Check we have exactly 8 bullets
        assert len(bullets) == 8
        
        # Check each bullet length
        for bullet in bullets:
            assert len(bullet) <= 85, f"Bullet exceeds 85 chars: {bullet}"
    
    def test_description_word_count_range(self, generator):
        """Test that descriptions stay within 120-160 word range"""
        brand = "TestBrand"
        product_type = "TestProduct"
        attributes = "Durable, Lightweight, Portable, Efficient, Modern"
        current_desc = "A test product description"
        keywords = "quality, performance, value"
        
        description, violations = generator.generate_description(
            brand, product_type, attributes, current_desc, keywords
        )
        
        word_count = len(description.split())
        
        # Check word count is in valid range
        assert 120 <= word_count <= 160, f"Word count {word_count} outside 120-160 range"
        
        # Verify no word count violations if within range
        word_count_violations = [v for v in violations if "word count" in v.lower()]
        assert len(word_count_violations) == 0
    
    def test_meta_fields_length_limits(self, generator):
        """Test meta title and description length constraints"""
        # Test meta title
        brand = "VeryLongBrandNameThatMightExceedLimit"
        product_type = "ExtremelylongProductTypeName"
        
        meta_title, title_violations = generator.generate_meta_title(brand, product_type)
        assert len(meta_title) <= 70, f"Meta title exceeds 70 chars: {len(meta_title)}"
        
        # Test meta description
        attributes = "Feature1, Feature2, Feature3, Feature4, Feature5, Feature6"
        meta_desc, desc_violations = generator.generate_meta_description(
            brand, product_type, attributes
        )
        assert len(meta_desc) <= 160, f"Meta description exceeds 160 chars: {len(meta_desc)}"
    
    def test_csv_processing_integration(self, generator, tmp_path):
        """Test full CSV processing workflow"""
        # Create test input CSV
        input_file = tmp_path / "test_input.csv"
        test_data = pd.DataFrame({
            'brand': ['CleanBrand', 'SafeBrand'],
            'product_type': ['Widget', 'Gadget'],
            'attributes': ['Sturdy, Reliable, Efficient', 'Compact, Modern, Durable'],
            'current_description': ['A clean description', 'Another safe description'],
            'current_bullets': ['Simple bullet 1|Simple bullet 2', 'Clean bullet 1|Clean bullet 2'],
            'keywords': ['quality, value', 'efficiency, design']
        })
        test_data.to_csv(input_file, index=False)
        
        # Process CSV
        output_file = tmp_path / "test_output.csv"
        result_df = generator.process_csv(str(input_file), str(output_file))
        
        # Verify output file exists
        assert output_file.exists()
        
        # Check all required columns exist
        required_columns = [
            'walmart_title', 'html_bullets', 'new_description',
            'meta_title', 'meta_description', 'violations'
        ]
        for col in required_columns:
            assert col in result_df.columns
        
        # Verify content was generated for all rows
        assert len(result_df) == 2
        assert result_df['walmart_title'].notna().all()
        assert result_df['new_description'].notna().all()
        
        # Check for products without violations
        clean_products = result_df[result_df['violations'] == 'None']
        assert len(clean_products) == 2, "Clean test data should have no violations"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
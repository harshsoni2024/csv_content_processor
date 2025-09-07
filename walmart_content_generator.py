import csv
import re
import warnings
from typing import Dict, List, Tuple
import pandas as pd

class WalmartContentGeneratorClass:
    def __init__(self):
        self.banned_words = [
            'cosplay', 'weapon', 'knife', 'knives', 'uv', 'premium', 'perfect',
            'medical', 'cure', 'heal', 'therapeutic', 'treatment', 'clinical',
            'prescription', 'surgical', 'hospital', 'doctor', 'physician',
            'guaranteed', 'warranty', 'lifetime', 'forever', 'permanent',
            'fda', 'approved', 'certified', 'authentic', 'genuine', 'original',
            'best', 'top', 'leading', 'number one', '#1', 'exclusive',
            'luxury', 'deluxe', 'elite', 'superior', 'supreme'
        ]
        
        self.max_bullet_length = 85
        self.num_bullets = 8
        self.max_meta_title_length = 70
        self.max_meta_desc_length = 160
        self.min_description_words = 120
        self.max_description_words = 160
        
    def check_banned_words(self, text: str) -> List[str]:
        """Check for banned words in text"""
        found_banned = []
        text_lower = text.lower()
        for word in self.banned_words:
            if word in text_lower:
                found_banned.append(word)
        return found_banned
    
    def clean_text(self, text: str) -> str:
        """Remove banned words from text"""
        clean = text
        for word in self.banned_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            clean = pattern.sub('', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    def generate_walmart_title(self, brand: str, product_type: str, attributes: str) -> Tuple[str, List[str]]:
        """Generate Walmart-safe title"""
        violations = []
        
        # Parse attributes
        attr_list = [a.strip() for a in attributes.split(',') if a.strip()]
        
        # Build title components
        title_parts = [brand]
        
        # Add product type
        if product_type:
            title_parts.append(product_type)
        
        # Add key attributes (first 2-3)
        for attr in attr_list[:3]:
            if len(' '.join(title_parts + [attr])) <= 150:
                title_parts.append(attr)
        
        title = ' '.join(title_parts)
        
        # Check for banned words
        banned_found = self.check_banned_words(title)
        if banned_found:
            title = self.clean_text(title)
            violations.append(f"Title had banned words: {', '.join(banned_found)}")
        
        return title, violations
    
    def generate_bullets(self, brand: str, product_type: str, attributes: str, 
                        current_description: str, keywords: str = "") -> Tuple[str, List[str]]:
        """Generate 8 HTML bullet points"""
        violations = []
        bullets = []
        
        # Parse attributes and keywords
        attr_list = [a.strip() for a in attributes.split(',') if a.strip()]
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []
        
        # Generate bullet templates
        bullet_templates = [
            f"{brand} {product_type} designed for quality and reliability",
            f"Features {attr_list[0] if attr_list else 'durable construction'}",
            f"{attr_list[1] if len(attr_list) > 1 else 'Easy to use'} design",
            f"Suitable for {attr_list[2] if len(attr_list) > 2 else 'everyday use'}",
            f"{attr_list[3] if len(attr_list) > 3 else 'Versatile'} functionality",
            f"Includes {attr_list[4] if len(attr_list) > 4 else 'essential features'}",
            f"{attr_list[5] if len(attr_list) > 5 else 'Built to last'}",
            f"Ideal for {attr_list[6] if len(attr_list) > 6 else 'home or office'}"
        ]
        
        # Process each bullet
        for i, template in enumerate(bullet_templates[:self.num_bullets]):
            bullet = template
            
            # Try to incorporate keywords naturally
            if i < len(keyword_list):
                keyword = keyword_list[i]
                if len(bullet) + len(keyword) + 5 <= self.max_bullet_length:
                    bullet = f"{bullet} with {keyword}"
            
            # Check length
            if len(bullet) > self.max_bullet_length:
                bullet = bullet[:self.max_bullet_length-3] + "..."
                violations.append(f"Bullet {i+1} truncated to meet length limit")
            
            # Check for banned words
            banned_found = self.check_banned_words(bullet)
            if banned_found:
                bullet = self.clean_text(bullet)
                violations.append(f"Bullet {i+1} had banned words: {', '.join(banned_found)}")
            
            bullets.append(f"<li>{bullet}</li>")
        
        html_bullets = "<ul>\n" + "\n".join(bullets) + "\n</ul>"
        return html_bullets, violations
    
    def generate_description(self, brand: str, product_type: str, attributes: str, 
                           current_description: str, keywords: str = "") -> Tuple[str, List[str]]:
        """Generate 120-160 word description"""
        violations = []
        
        # Parse inputs
        attr_list = [a.strip() for a in attributes.split(',') if a.strip()]
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []
        
        # Build description with more content
        sentences = []
        
        # Opening sentences
        sentences.append(f"The {brand} {product_type} delivers outstanding performance and value for everyday use.")
        sentences.append(f"This carefully designed product brings together functionality and reliability in one comprehensive solution.")
        
        # Features sentences
        if attr_list:
            sentences.append(f"Key features include {', '.join(attr_list[:2])}, making it an ideal choice for various applications.")
            if len(attr_list) > 2:
                sentences.append(f"Additional capabilities encompass {', '.join(attr_list[2:4])}, enhancing overall versatility and user satisfaction.")
            if len(attr_list) > 4:
                sentences.append(f"The product also incorporates {attr_list[4]}, adding extra value to your investment.")
        
        # Quality and usage
        sentences.append(f"Built with meticulous attention to detail, this {product_type} ensures dependable operation across different scenarios.")
        sentences.append("Its thoughtful design accommodates both personal and professional requirements with equal effectiveness.")
        
        # Keywords integration
        if keyword_list:
            sentences.append(f"Essential aspects like {', '.join(keyword_list[:2])} have been prioritized in the development process.")
            if len(keyword_list) > 2:
                sentences.append(f"The focus on {keyword_list[2]} further enhances the overall user experience.")
        
        # Brand commitment
        sentences.append(f"{brand} maintains high standards throughout the manufacturing process, ensuring consistent quality.")
        sentences.append("This dedication to excellence translates into a product that meets and exceeds expectations.")
        
        # Usage scenarios
        sentences.append("Suitable for home, office, or on-the-go use, it adapts seamlessly to your lifestyle.")
        sentences.append("The combination of practical features and durable construction provides lasting value.")
        
        # Closing
        sentences.append("Every element has been optimized to deliver maximum benefit to users.")
        sentences.append("This product represents a smart investment for those seeking quality and reliability.")
        
        # Join sentences and check word count
        description = " ".join(sentences)
        word_count = len(description.split())
        
        # Adjust to fit word count requirement
        if word_count > self.max_description_words:
            # Trim to fit
            words = description.split()[:self.max_description_words]
            description = " ".join(words)
            # Ensure last word ends properly
            if not description.endswith('.'):
                description = description.rsplit(' ', 1)[0] + '.'
        elif word_count < self.min_description_words:
            # This shouldn't happen with our expanded content, but handle it
            violations.append(f"Description word count ({word_count}) below minimum 120 words")
        
        # Check for banned words
        banned_found = self.check_banned_words(description)
        if banned_found:
            description = self.clean_text(description)
            violations.append(f"Description had banned words: {', '.join(banned_found)}")
        
        # Final word count check
        final_word_count = len(description.split())
        if final_word_count < self.min_description_words or final_word_count > self.max_description_words:
            violations.append(f"Description word count ({final_word_count}) outside 120-160 range")
        
        return description, violations
    
    def generate_meta_title(self, brand: str, product_type: str) -> Tuple[str, List[str]]:
        """Generate meta title (≤70 chars)"""
        violations = []
        
        meta_title = f"{brand} {product_type} | Shop Now"
        
        if len(meta_title) > self.max_meta_title_length:
            meta_title = f"{brand} {product_type}"[:self.max_meta_title_length-3] + "..."
            violations.append(f"Meta title truncated to {self.max_meta_title_length} chars")
        
        # Check for banned words
        banned_found = self.check_banned_words(meta_title)
        if banned_found:
            meta_title = self.clean_text(meta_title)
            violations.append(f"Meta title had banned words: {', '.join(banned_found)}")
        
        return meta_title, violations
    
    def generate_meta_description(self, brand: str, product_type: str, attributes: str) -> Tuple[str, List[str]]:
        """Generate meta description (≤160 chars)"""
        violations = []
        
        attr_list = [a.strip() for a in attributes.split(',') if a.strip()]
        key_attrs = ', '.join(attr_list[:2]) if attr_list else "quality features"
        
        meta_desc = f"Shop {brand} {product_type} with {key_attrs}. Great value and reliable performance for your needs."
        
        if len(meta_desc) > self.max_meta_desc_length:
            meta_desc = meta_desc[:self.max_meta_desc_length-3] + "..."
            violations.append(f"Meta description truncated to {self.max_meta_desc_length} chars")
        
        # Check for banned words
        banned_found = self.check_banned_words(meta_desc)
        if banned_found:
            meta_desc = self.clean_text(meta_desc)
            violations.append(f"Meta description had banned words: {', '.join(banned_found)}")
        
        return meta_desc, violations
    
    def process_csv(self, input_file: str, output_file: str):
        """Process input CSV and generate output with new content"""
        
        # Read input CSV
        df = pd.read_csv(input_file)
        
        # Initialize new columns
        df['walmart_title'] = ''
        df['html_bullets'] = ''
        df['new_description'] = ''
        df['meta_title'] = ''
        df['meta_description'] = ''
        df['violations'] = ''
        
        # Process each row
        for idx, row in df.iterrows():
            all_violations = []
            
            # Extract keywords if present
            keywords = row.get('keywords', '')
            
            # Generate title
            title, title_violations = self.generate_walmart_title(
                row['brand'], row['product_type'], row['attributes']
            )
            df.at[idx, 'walmart_title'] = title
            all_violations.extend(title_violations)
            
            # Generate bullets
            bullets, bullet_violations = self.generate_bullets(
                row['brand'], row['product_type'], row['attributes'],
                row['current_description'], keywords
            )
            df.at[idx, 'html_bullets'] = bullets
            all_violations.extend(bullet_violations)
            
            # Generate description
            description, desc_violations = self.generate_description(
                row['brand'], row['product_type'], row['attributes'],
                row['current_description'], keywords
            )
            df.at[idx, 'new_description'] = description
            all_violations.extend(desc_violations)
            
            # Generate meta title
            meta_title, mt_violations = self.generate_meta_title(
                row['brand'], row['product_type']
            )
            df.at[idx, 'meta_title'] = meta_title
            all_violations.extend(mt_violations)
            
            # Generate meta description
            meta_desc, md_violations = self.generate_meta_description(
                row['brand'], row['product_type'], row['attributes']
            )
            df.at[idx, 'meta_description'] = meta_desc
            all_violations.extend(md_violations)
            
            # Combine violations
            df.at[idx, 'violations'] = '; '.join(all_violations) if all_violations else 'None'
        
        # Save output CSV
        df.to_csv(output_file, index=False)
        print(f"✓ Generated content saved to {output_file}")
        
        # Display summary
        print(f"\nProcessed {len(df)} products")
        products_with_violations = df[df['violations'] != 'None']
        if len(products_with_violations) > 0:
            print(f"⚠ {len(products_with_violations)} products have violations")
        else:
            print("✓ All products meet requirements")
        
        return df

def main():
    # Create instance
    process_class = WalmartContentGeneratorClass()
    
    # Process CSV
    input_file = 'products_input.csv'
    output_file = 'products_output.csv'
    
    try:
        result_df = process_class.process_csv(input_file, output_file)
        print("\n✓ Content generation complete!")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        print("Please create an input CSV with columns: brand, product_type, attributes, current_description, current_bullets")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
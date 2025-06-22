from pdf2image import convert_from_path
import pytesseract
import glob

pdf_files = glob.glob(r"attachments\*.pdf")

for pdf_path in pdf_files:
    try:
        print(f"\nProcessing: {pdf_path}")
        pages = convert_from_path(pdf_path, dpi=300)
        
        for page_num, img in enumerate(pages, start=1):
            img = img.convert('L')  
            text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
            
            # Only save if text contains more than just whitespace
            if text.strip():
                output_path = f"{pdf_path[:-4]}_page{page_num}.txt"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"✓ Saved: {output_path} (Chars: {len(text)})")
            else:
                print(f"× Skipped empty page {page_num}")
                
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")

print("\nProcessing complete!")
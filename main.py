import fitz  # PyMuPDF

# Load the PDF
doc = fitz.open("roc.pdf")  # change to your PDF filename

with open("output.txt", "w", encoding="utf-8") as output:

    for page_num, page in enumerate(doc, start=1):
        output.write(f"\n--- Page {page_num} ---\n\n")
        
        # Extract plain text
        text = page.get_text("text")
        output.write("📄 Text:\n")
        output.write(text + "\n")

        # Extract detailed font info
        output.write("🔠 Font Info:\n")
        details = page.get_text("dict")
        for block in details["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    info = f"Text: {span['text']}\nFont: {span['font']}, Size: {span['size']}, Color: {span['color']}\n"
                    output.write(info)

        # Extract links
        links = page.get_links()
        if links:
            output.write("🔗 Links:\n")
            for link in links:
                if "uri" in link:
                    output.write(f"Link: {link['uri']}\n")
        
        # Extract image info (positions only, no image saving here)
        images = page.get_images(full=True)
        if images:
            output.write("🖼️ Images Found:\n")
            for img in images:
                xref = img[0]
                output.write(f"Image xref: {xref}, Width: {img[2]}, Height: {img[3]}\n")

print("✅ Extraction complete! Data saved to 'output.txt'")

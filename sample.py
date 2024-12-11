import fitz  # PyMuPDF

def generate_pdf_with_pymupdf(text, output_filename):
    # Create a new PDF document
    doc = fitz.open()
    
    # Add a page to the document
    page = doc.new_page()

    # Set font and size for the text
    font = "helv"  # Helvetica font
    font_size = 12

    # Define page dimensions and margins
    page_width = page.rect.width
    left_margin = 50
    right_margin = 50
    usable_width = page_width - left_margin - right_margin
    x, y = left_margin, 50  # Start near the top-left corner

    # Wrap text to fit within the usable width
    current_y = y
    for line in text.splitlines():
        # Break the line into chunks that fit the usable width
        while line:
            # Measure the text width and break if necessary
            max_chars = len(line)
            while max_chars > 0:
                if page.get_text_length(line[:max_chars], fontsize=font_size) <= usable_width:
                    break
                max_chars -= 1

            # Extract the part of the line that fits
            text_chunk = line[:max_chars]
            line = line[max_chars:].lstrip()  # Remove the part already added
            
            # Add the text chunk to the page
            page.insert_text((x, current_y), text_chunk, fontsize=font_size, fontname=font)
            current_y += font_size + 5  # Move to the next line (line spacing)

    # Save the PDF to the specified output file
    doc.save(output_filename)
    print(f"PDF saved as {output_filename}")

# Example usage
text = """Subject: Duplicate Claim Notification.

Dear John Doe,

We have received your claim submission for the incident that occurred on 28-Nov-2024 involving your Toyota Camry. After reviewing our records, we have determined that this submission is a duplicate claim.

If you believe this is an error or if you have any questions, please contact our customer service team at 1-555-234-5678 or reply to this email.

Thank you for your understanding.

Best regards,
Ageas Insurance"""
output_filename = "example_output.pdf"
generate_pdf_with_pymupdf(text, output_filename)

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
    page_height = page.rect.height
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50
    usable_width = page_width - left_margin - right_margin
    usable_height = page_height - top_margin - bottom_margin

    # Define a rectangle for text placement
    text_rect = fitz.Rect(left_margin, top_margin, page_width - right_margin, page_height - bottom_margin)

    # Insert the text into the page
    page.insert_textbox(
        text_rect,
        text,
        fontsize=font_size,
        fontname=font,
        align=0,  # Align left
    )

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

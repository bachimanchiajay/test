import fitz  # PyMuPDF
import io
import os
import boto3

def extract_images_to_pdf(filename, bucket_name, s3_folder):
    try:
        # Open the PDF file
        with open(filename, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        # Initialize variables
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")

        # Generate the output PDF filename
        input_file_name = os.path.splitext(os.path.basename(filename))[0]
        output_pdf_path = f"{input_file_name}_sub.pdf"

        # Create a new PDF document to store extracted images
        new_pdf = fitz.open()

        # Iterate through each page to extract images
        for page_number in range(len(pdf_document)):
            for img_index, img in enumerate(pdf_document.get_page_images(page_number)):
                xref = img[0]  # Reference number for the image
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]

                # Convert the image bytes to a Pixmap object
                image_stream = io.BytesIO(image_bytes)
                pixmap = fitz.Pixmap(image_stream)

                # Add a new page to the new PDF with the dimensions of the image
                pdf_page = new_pdf.new_page(width=pixmap.width, height=pixmap.height)

                # Insert the image into the new PDF page
                pdf_page.insert_image(pdf_page.rect, pixmap=pixmap)

        # Save the new PDF
        new_pdf.save(output_pdf_path)
        new_pdf.close()
        pdf_document.close()

        print(f"Extracted images saved to PDF: {output_pdf_path}")

        # Upload to S3
        s3_client = boto3.client('s3')
        s3_key = f"{s3_folder}/{os.path.basename(output_pdf_path)}"
        s3_client.upload_file(output_pdf_path, bucket_name, s3_key)

        print(f"Uploaded to S3: s3://{bucket_name}/{s3_key}")
        return f"s3://{bucket_name}/{s3_key}"

    except Exception as e:
        raise e


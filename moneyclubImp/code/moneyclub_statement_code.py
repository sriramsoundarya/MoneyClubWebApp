from PyPDF2 import PdfReader
import re
import pandas as pd
import os 


def get_pdf_files(folder_path):
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(folder_path, file))
    return pdf_files[0]

# Load the PDF file
def moneyClubStatement():
        folder_path2=r'static\uploads'
        directory = get_pdf_files(folder_path2)
        # pdf_path = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]
        reader = PdfReader(directory)

        # Initialize lists to store extracted data
        dates = []
        times = []
        amounts = []
        utrs = []

        # Regular expressions to extract the required details
        date_time_pattern = r"(\w+\s\d{2},\s\d{4}\s\d{2}:\d{2}\s(?:am|pm))"
        amount_pattern = r"₹([\d,]+\.?\d*)"
        utr_pattern = r"UTR No\. (\d+)"

        # Read the PDF page by page and extract information
        for page in reader.pages:
            text = page.extract_text()
            # Find all matches in the text
            date_time_matches = re.findall(date_time_pattern, text)
            amount_matches = re.findall(amount_pattern, text)

            utr_matches = re.findall(utr_pattern, text)
            
            amount_matches_new = [(item.replace(',', '')) for item in amount_matches]

            # Append to lists (ensuring consistent data length)
            dates.extend([dt.split(' ')[0] for dt in date_time_matches])
            times.extend([dt.split(' ')[1] + ' ' + dt.split(' ')[2] for dt in date_time_matches])
            amounts.extend(amount_matches_new)
            utrs.extend(utr_matches)

        # Create a DataFrame for extracted data
        data = {
            'Date': dates,
            'Time': times,
            'Amount (₹)': amounts,
            'UTR No.': utrs
        }
        df = pd.DataFrame(data)

        # Save to Excel
        # output_path = r'output\Staement_data.csv'
        # df.to_csv(output_path, index=False)

        # print(f"Data extracted and saved to {output_path}")
        return df


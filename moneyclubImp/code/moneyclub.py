import pytesseract
from PIL import Image
import re
import pandas as pd
from moneyclub_statement_code import moneyClubStatement
import os 

def get_jpg_files(folder_path):
    jpg_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            jpg_files.append(os.path.join(folder_path, file))
    return jpg_files[0]



# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

folder_path=r'static\uploads'
print(get_jpg_files(folder_path))
# Load the image
image_path = get_jpg_files(folder_path)  # Replace with your JPG screenshot file path

image = Image.open(image_path)

# Perform OCR on the image
text = pytesseract.image_to_string(image)

# Extract Transaction ID and Rupee amount using regular expressions
transaction_ids = re.findall(r'Transaction ID[:\s]+([A-Za-z0-9]+)', text)
rupee_amounts = re.findall(r'(\d+)\. Have you', text)

# Check lengths of both lists
len_tids = len(transaction_ids)
len_amounts = len(rupee_amounts)

# Ensure both lists are of the same length
if len_tids != len_amounts:
    # Print out a warning if lengths don't match and pad the shorter list with None or handle accordingly
    print(f'Warning: Different lengths detected! Transaction IDs: {len_tids}, Amounts: {len_amounts}')
    if len_tids < len_amounts:
        transaction_ids.extend([None] * (len_amounts - len_tids))
    else:
        rupee_amounts.extend([None] * (len_tids - len_amounts))

# Prepare data for the table
data = {
    'Transaction ID': transaction_ids,
    'Amount': rupee_amounts
}

# Create a DataFrame and display the table
df = pd.DataFrame(data)
print(df)

# Save the table to a CSV file
# df.to_csv(r'output\screenshot.csv', index=False)

df1=moneyClubStatement()
print(df1)

# Perform the left join
merged_df = pd.merge(df, df1, left_on=['Transaction ID'], right_on=['UTR No.'], how='left')

# Save the merged DataFrame to a CSV file
merged_df.to_csv(r'output\result.csv', index=False)
print(merged_df)

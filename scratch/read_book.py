import openpyxl
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

file_path = "the-book-of-GEMINIAEUS.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=True)

# Read Sheet 1 (index 0)
sheet1 = wb.worksheets[0]
print(f"\n--- Content of {sheet1.title} ---")
for row in sheet1.iter_rows(values_only=True):
    if any(row):
        print(row)

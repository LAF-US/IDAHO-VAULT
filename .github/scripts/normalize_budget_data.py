import csv

def normalize_data():
    """
    Reads the minidata.csv file, normalizes the data, and writes it to a new CSV file.
    """
    try:
        with open('minidata.csv', 'r', newline='', encoding='utf-8') as infile, 
             open('normalized_budget_data.csv', 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)
            fieldnames = [
                'budget_type', 'sector', 'agency', 'program', 'bill_id', 'bill_url',
                'status', 'event_date', 'event_summary', 'description'
            ]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                writer.writerow({
                    'budget_type': '',
                    'sector': '',
                    'agency': '',
                    'program': '',
                    'bill_id': row.get('bill_id', ''),
                    'bill_url': row.get('url', ''),
                    'status': '',
                    'event_date': '',
                    'event_summary': row.get('last_action', ''),
                    'description': row.get('title', '')
                })
        print("Successfully created normalized_budget_data.csv")

    except FileNotFoundError:
        print("Error: minidata.csv not found. Please run the scraper first.")

if __name__ == "__main__":
    normalize_data()

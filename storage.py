import csv
import os

def save_invoice(data):

    file_exists = os.path.isfile("invoice_database.csv")

    with open("invoice_database.csv","a",newline="") as file:

        writer = csv.DictWriter(file,fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)
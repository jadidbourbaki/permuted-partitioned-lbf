import csv
import random
import feature_extraction as fe
import os

def remove_data():
    os.remove("/tmp/malicious_urls.csv")
    os.remove("/tmp/malicious_urls_tiny.csv")

def generate_data():
    write_to = open("/tmp/malicious_urls.csv", "w")
    write_to_tiny = open("/tmp/malicious_urls_tiny.csv", "w") # For faster testing
    read_from = open("dataset/malicious_phish.csv", "r")

    reader = csv.DictReader(read_from)
    writer = csv.DictWriter(write_to, fieldnames=fe.feature_names())
    writer_tiny = csv.DictWriter(write_to_tiny, fieldnames=fe.feature_names())

    writer.writeheader()
    writer_tiny.writeheader()
        
    for row in reader:
        url = row['url']
        # remove the 'www'
        url = url.replace('www.', '')
        features = fe.generate_fields(url, row['type'])
        names = fe.feature_names()

        for name, feature in zip(names, features):
            row[name] = feature

        writer.writerow(row)

        if random.randint(1, 5) == 1:
            writer_tiny.writerow(row)

    read_from.close()
    write_to.close()
    write_to_tiny.close()
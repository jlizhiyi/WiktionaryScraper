import csv

# Input CSV filename
input_csv_filename = 'chinese_characters_with_pinyin.csv'

# Output CSV filename
output_csv_filename = 'chinese_characters_with_pinyin2.csv'

# Open the input CSV file for reading
with open(input_csv_filename, 'r', newline='', encoding='utf-8') as input_csv_file:
    # Open the output CSV file for writing
    with open(output_csv_filename, 'w', newline='', encoding='utf-8') as output_csv_file:
        csv_reader = csv.reader(input_csv_file)
        csv_writer = csv.writer(output_csv_file)
        
        for row in csv_reader:
            if len(row) == 2:
                character, pinyin = row
                # Extract the tone (last character) from the pinyin
                tone = pinyin[-1]
                # Remove the tone from the pinyin
                pinyin_without_tone = pinyin[:-1]
                # Write the transformed row with 3 columns
                csv_writer.writerow([character, pinyin_without_tone, tone])
            else:
                # Write the row as is (3-column format)
                csv_writer.writerow(row)

print(f"Transformation complete. Output saved to {output_csv_filename}")

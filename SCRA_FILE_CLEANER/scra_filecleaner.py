import argparse
import re


parser = argparse.ArgumentParser(description="Get SCRA file")
parser.add_argument('--file_path', type=str, required=True, help='Specify SCRA file path')
args=parser.parse_args()

file_path = args.file_path
# file_path= r"\\wf.local\dmfiles\ETL\internal\GA_Projects\RH-Test\TestUpload\SCRA_Input_20250110.txt"
output_path= file_path




# Define fixed-width column structure (Start Position is 0-based)
COLUMNS = [
    (0, 43),    # Column 1: Starts at position 1, length 43
    (43, 20),   # Column 2: Starts at position 44, length 20
    (63, 28),   # Column 3: Starts at position 64, length 28
    (91, 28)    # Column 4: Starts at position 92, length 28 (ensuring total width = 120)
]

MAX_RECORDS = 250000  # Maximum records allowed
VALID_CHARS_REGEX = re.compile(r"^[A-Za-z0-9 ]*$")  # Only letters, numbers, and spaces

def validate_and_fix_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if len(lines) > MAX_RECORDS:
        print(f"Error: File contains {len(lines)} records, exceeding the maximum allowed ({MAX_RECORDS}).")
        return

    fixed_lines = []
    errors = []

    for i, line in enumerate(lines):
        line = line.rstrip("\n")  # Remove newline for accurate indexing
        line = line.ljust(120)  # Ensure it meets min length requirement
        line = line[:42] + " " + line[43:62] + " " + line[63:90] + " " + line[91:]
        fixed_line = []
        for start, length in COLUMNS:
            if start + length > len(line):
                errors.append(f"Row {i+1} is too short.")
                continue

            segment = line[start:start + length]

            # Ensure only allowed characters (letters, numbers, spaces)
            if not VALID_CHARS_REGEX.match(segment):
                errors.append(f"Row {i+1}, column {start+1} contains invalid characters.")
                segment = re.sub(r"[^A-Za-z0-9 ]", " ", segment)  # Replace invalid characters with spaces

            # Trim field from the end if it's too long, pad if too short
            segment = segment[:length].ljust(length)  
            fixed_line.append(segment)

        # Join fixed fields and ensure line is exactly 120 characters
        final_line = "".join(fixed_line)[:120]  
        fixed_lines.append(final_line + "\n")

    # Save the corrected file
    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(fixed_lines)
    
    print(f"File has been validated and saved as: {output_path}")


validate_and_fix_file(file_path, output_path)

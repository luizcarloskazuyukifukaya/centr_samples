def sum_values_in_file(file_path):
    total_sum = 0
    total_files = 0
    total_directories = 0
    with open(file_path, 'r') as file:
        for line in file:
            if not line.rstrip().endswith('0'):
                print(line, end='')  # Print the line without adding extra newline
                total_files += int(1)
            else:
                total_directories += int(1)

            # Split the line into the filename and value
            parts = line.rsplit(',', 1)  # Split from the right, max 1 split
            if len(parts) == 2:
                filename, value = parts
                # Remove any whitespace from value and attempt conversion to int
                try:
                    total_sum += int(value.strip())
                except ValueError:
                    print(f"#Warning: Value '{value.strip()}' in line '{line.strip()}' is not a valid integer.")
    return total_sum, total_files, total_directories

# convert byte value
def convert_bytes(size_in_bytes):
    # Define conversion factors
    KB = 1024
    MB = KB * 1024
    GB = MB * 1024
    TB = GB * 1024

    # Perform conversions
    if size_in_bytes < KB:
        return f"{size_in_bytes} B"
    elif size_in_bytes < MB:
        return f"{size_in_bytes / KB:.2f} KB"
    elif size_in_bytes < GB:
        return f"{size_in_bytes / MB:.2f} MB"
    elif size_in_bytes < TB:
        return f"{size_in_bytes / GB:.2f} GB"
    else:
        return f"{size_in_bytes / TB:.2f} TB"


# Define the file name
file_name = 'missing.txt'  # Change this to the name of your file

if __name__ == "__main__":
    # Call the function
    size_in_bytes, total_file_found, total_dir_found = sum_values_in_file(file_name)
    converted_size_str = convert_bytes(size_in_bytes)

    print(f"# --- Missing objects information ---")
    print(f"#Total size: {converted_size_str}")
    print(f"#Total file number: {total_file_found}")
    print(f"#Total directories number: {total_dir_found}")
    print(f"#Total objects number: {total_dir_found+total_file_found}")

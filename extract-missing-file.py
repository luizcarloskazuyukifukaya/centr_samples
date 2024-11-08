# Define the file name
file_name = 'missing.txt'  # Change this to the name of your file

def extract_files(file):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                # Strip whitespace characters (like \n) from the end of the line
                # directory always end with "/, 0"
                if not line.rstrip().endswith('/, 0'):
                    print(line, end='')  # Print the line without adding extra newline
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")

if __name__ == "__main__":
    # Call the function
    extract_files(file_name)

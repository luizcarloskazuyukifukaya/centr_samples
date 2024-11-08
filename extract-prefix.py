# Define the file name
file_name = 'missing.txt'  # Change this to the name of 
file_name = 'delta.log'  # Change this to the name of 
# file_name = 'centr-source.txt'  # Change this to the name of your file
# file_name = 'centr-target.txt'  # Change this to the name of your file

def extract_prefix(file):
    prefix_num = 0
    try:
        with open(file_name, 'r') as file:
            for line in file:
                # Strip whitespace characters (like \n) from the end of the line
                if line.rstrip().endswith('/, 0'):
                    print(line, end='')  # Print the line without adding extra newline
                    prefix_num = prefix_num + int(1)
    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        
    print(f"# Total number of prefix: {prefix_num}")

if __name__ == "__main__":
    # Call the function
    extract_prefix(file_name)

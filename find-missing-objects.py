file_b = 'centr-source.txt'
file_a = 'centr-target.txt'

def compare_files(file_a, file_b):
    delta_num = 0  # number of objects missing

    # Read lines from A.txt and store in a set for faster lookup
    with open(file_a, 'r') as f_a:
        lines_a = {line.strip() for line in f_a}

    # Read lines from B.txt and check against A.txt
    with open(file_b, 'r') as f_b:
        for line in f_b:
            stripped_line = line.strip()
            items = [item.strip() for item in stripped_line.split(',')]
            object_key = items[0]

            print(f"#[debug]::[object_key]:[{object_key}]")

            # Check if object_key exists in lines_a
            if any(object_key in obj for obj in lines_a):
                # If found, remove the matched object from lines_a to prevent future matches
                lines_a = {obj for obj in lines_a if object_key not in obj}

                print(f"#[debug]::[FOUND]:[{len(lines_a)}]")

            else:
                delta_num += 1

                print(f"#[debug]::[NOT FOUND]:[{delta_num}]: {object_key}")

                print(f"{stripped_line}")

    return delta_num

if __name__ == "__main__":
    # Call the function
    missing_objects_num = compare_files(file_a, file_b)
    print(f"#Delta objects: {missing_objects_num}")
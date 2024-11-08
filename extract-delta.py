# Define file names
# file_b = 'Centr-SourceBucketLog.txt'
# file_a = 'Centr-TargetBucketLog.txt'
# file_b = 'source-inventory-all-2.log'
# file_a = 'target-inventory-all.log'
file_b = 'centr-source.txt'
file_a = 'centr-target.txt'

def compare_files(file_a, file_b):
    delta_num = 0 # number of object missing

    # Read lines from A.txt and store in a set for faster lookup
    with open(file_a, 'r') as f_a:
        lines_a = set(line.strip() for line in f_a)
        # print(lines_a)
        key_list = [line.split(',')[0] for line in lines_a]
        # print(key_list)
        print(f"#[debug]:: ****************************")
        print(f"#[debug]::key_list size:[{len(key_list)}]")
        print(f"#[debug]:: ****************************")

    # Read lines from B.txt and check against A.txt
    with open(file_b, 'r') as f_b:
        for line in f_b:
            stripped_line = line.strip()
            # Check if line from B.txt does not match any line in A.txt
# The comparison should be made against the file name level, as there is a case where the file size is not the same due to the copy not successfully completed
            # if stripped_line not in lines_a:
            #     print(stripped_line)
            #     delta_num += int(1)
# comparison of filename
            items = [item.strip() for item in stripped_line.split(',')]
            object_key = items[0]
            # # now we have the target object key, and need to check if it exist in A
            # if object_key not in lines_a:
            # for f in lines_a[:]:
            # print(f"#[debug]::object_key:[{object_key}]")
            found_flag = False

            # check if the object_key is present on the key_list
            is_present = any(item == object_key for item in key_list)

            if not is_present:
                delta_num += int(1)
                # print(f"#[debug]::{object_key} NOT FOUND")
                # print(f"#[debug]::[{delta_num}]:")
                print(f"{stripped_line}")
            else:
                # is present, so remove the key from the key_list
                # print(f"#{object_key} found")
                # print(f"#[debug]::key_list size:[{len(key_list)}]")
                key_list.remove(object_key)
                # print(f"#[debug]::remove object from key_list")
                # print(f"#[debug]::key_list size:[{len(key_list)}]")                
                        
    return delta_num

if __name__ == "__main__":
    # Call the function
    missing_objects_num = compare_files(file_a, file_b)
    print(f"#Delta objects: {missing_objects_num}")
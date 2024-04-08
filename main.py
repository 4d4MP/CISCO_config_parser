import os
import concurrent.futures as f
import re

def list_txt_files():
    return [f for f in os.listdir() if f.endswith('.txt')]

def process_file(filename):
    print(f"Processing {filename}\n")
    try:
        with open(filename, 'r') as file:
            data = file.read()
            i = 0
            for line in data.split('\n'):
                i += 1
                match = re.search(r'(rb\-.*\#)|(sb\-.*\#)')
                if "sh version" in line and "sh version | i Processor" not in line:
                    try:
                        for j in range(i, len(data.split('\n'))-1):
                            if "System image file is" in data.split('\n')[j]:
                                print(data.split('\n')[j])
                            if "Device#" in data.split('\n')[j]:
                                print("PID: " + data.split('\n')[j+2].split()[1])
                                print("VID: " + data.split('\n')[j+2].split()[2])
                            if data.split('\n')[j].match(match):
                                print(data.split('\n')[j])
                                i += j
                                break
                    except IndexError:
                        print("This is the last line of the file.\n")
                
        pass
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e} \n")

def process_txt_files_in_parallel():
    txt_files = list_txt_files()
    with f.ThreadPoolExecutor() as executor:
        executor.map(process_file, txt_files)
        
def __main__():
    process_txt_files_in_parallel()
    
if __name__ == '__main__':
    __main__()
    
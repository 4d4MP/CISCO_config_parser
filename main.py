import os
import concurrent.futures as f
import re
import csv

def list_txt_files():
    return [f for f in os.listdir() if f.endswith('.txt')]

def process_file(filename):
    print(f"Processing {filename}\n")
    output_filename = filename.split(".")[0] + "_out.csv"
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Hostname", "Serial Number", "Version", "Model", "Image"])
    
        try:
            with open(filename, 'r') as file:
                data = file.read().splitlines()
                for line in data:
                    if "(config)#end" in line or "#write mem" in line or "#configure terminal" in line:
                        data.remove(line)
                for i in range(len(data)):
                    j = i + 1
                    if data[i].startswith('Cisco IOS Software') and data[i-1].endswith('sh version'):
                        
                        
                        while j < len(data):
                            general_pattern = re.compile(r".*b-.+#$")
                            if "Cisco IOS Software" in data[j]:
                                print("3======D")
                                break

                            j += 1
                    
                        switch_pattern_1 = re.compile(r"sb-.+#$")
                        router_pattern_1 = re.compile(r"rb-.+#$")
                    
                        hostname = data[j]
                        if switch_pattern_1.match(data[j]) or router_pattern_1.match(data[j]):
                    
                            print(f"i = {i}, j = {j}")
                            
                            version = ""
                            serial = ""
                            model = ""
                            image = ""
                            print("-----------------------------------")
                            for k in range(i, j):
                                #print(data[k])
                                if "Cisco IOS Software" in data[k]:
                                    version = data[k].split(",")[2].strip("Version ")
                                if "Motherboard serial number" in data[k] and not router_pattern_1.match(data[j]):
                                    serial = {data[k].split(":")[-1].strip(" ").strip("{").strip("}").strip("'")}
                                elif "License UDI:" in data[k] and router_pattern_1.match(data[j]):
                                    serial = data[k + 5][29:].strip(" ")
                                if "K bytes of memory" in data[k]:
                                    model = data[k].split(" ")[1]
                                if "System image file is" in data[k]:
                                    image = data[k].split("is ")[-1].strip('"')
                            
                            print(f"Hostname: {hostname}, Serial: {serial}, Version: {version}, Model: {model}, Image: {image}\n")
                            writer.writerow([hostname, serial, version, model, image])
                             
                    i += j                         
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
    
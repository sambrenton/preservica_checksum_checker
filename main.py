from pyPreservica import *
import csv

client = EntityAPI()

# Takes preservica collection reference as argument - keep this as low level as you can to save proccessing time
def get_preservica_checksums(collection):
    with open('preservica_checksums.csv', mode='w', newline='\n') as file:
        for asset in filter(only_assets, client.all_descendants(collection)):
            for r in client.representations(asset):
                for co in client.content_objects(r):
                    for generation in client.generations(co):
                            for bs in generation.bitstreams:
                                    for algorithm,value in bs.fixity.items():
                                        if algorithm == 'MD5':
                                            print(bs.filename)
                                            print(value)
                                            writer = csv.writer(file, delimiter=',')
                                            try:
                                                writer.writerow([bs.filename, value])
                                            except UnicodeEncodeError:
                                                pass


# Reads .md5 file as text file, returns string
def checksum_reader(path):
    with open(path) as file:
        hash = file.read()
        return hash


# Reads local md5 where each folder *ONLY* contains file and checksum 
def get_local_checksums(directory):
    with open('local_checksums.csv', mode='w', newline='\n') as list:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_ext = file[-3:]
                if file_ext.lower() == 'md5':
                    if len(files) == 2:
                        hashes = [checksum_reader(os.path.join(root, file)) for file in files if file[-3:] == 'md5']
                        av_files = [file for file in files if file[-3:] != 'md5']
                        for a, b in zip(av_files, hashes):
                            writer = csv.writer(list, delimiter=',')
                            writer.writerow([a, b])


# Takes CSV files and returns dicts
def csv_to_dict(csv_path):
    dict = {}
    with open(csv_path, 'r') as hash_csv:
        for row in csv.reader(hash_csv):
            if row[0] not in dict.keys():
                dict[row[0]] = row[1]
        return dict

# Checks list of preservica generated checksums, against checksums created locally
def compare_checksums():
    local_md5_dict = csv_to_dict(r'local_checksums.csv')
    preservica_md5_dict = csv_to_dict(r'preservica_checksums.csv')
    for key, value in local_md5_dict.items():
        if key in preservica_md5_dict:
            if value != preservica_md5_dict[key]:
                print('==============================')
                print(key)
                print(value)
                print(preservica_md5_dict[key])


if __name__ == "__main__":
    get_preservica_checksums(collection='')
    get_local_checksums(directory='')
    compare_checksums()

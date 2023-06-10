import requests
import asyncio
import getting_phages_for_bacteria
from getting_phages_for_bacteria import *
import time

dbbact_api = 'https://api.dbbact.org'
human_associated_bacteria = []


def request_with_retry(url, json_data, timeout_duration, max_retries=3, retry_delay=2):
    for i in range(max_retries):
        try:
            res = requests.get(url, json=json_data, timeout=timeout_duration)
            return res
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise


def find_human_associated_bacteria():
    human_associated_bacteria_file = 'human_associated_bacteria.txt'
    if file_exists(human_associated_bacteria_file):
        return

    dbbact_api = 'https://api.dbbact.org'
    timeout_duration = 10

    for name in scientific_names_list:
        count = 0
        url = dbbact_api + '/sequences/get_species_seqs'
        json_data = {'species': name}
        res = request_with_retry(url, json_data, timeout_duration).json()

        url = dbbact_api + '/sequences/get_info'
        json_data = {'seqids': res["ids"]}
        seqs = request_with_retry(url, json_data, timeout_duration).json()

        if len(seqs["sequences"]) > 0:
            url = dbbact_api + '/sequences/get_annotations'
            json_data = {'sequence': seqs["sequences"][0]["seq"]}
            fast = request_with_retry(url, json_data, timeout_duration).json()
            #   print(len(fast["annotations"]))

            for annotation in fast["annotations"]:
                #   print(annotation['details'])
                found = False
                for sublist in annotation['details']:
                    if 'homo sapiens' in sublist:
                        found = True
                        break
                if found:
                    print("homo sapiens is in the list")
                    count += 1
            # print(count / len(fast["annotations"]))
            # print(count)
            if count / len(fast["annotations"]) >= 0.15:
                print("********************im a piece of the human microbiome AKA: gay")
                human_associated_bacteria.append(name)
        # Save list to a file
        with open('human_associated_bacteria.txt', 'w') as filehandle:
            for item in human_associated_bacteria:
                filehandle.write('%s\n' % item)


values = " ".join(str(value) for value in bacteria_phages_dict.values())
print(values)
print(values.count('nan'))

"""
def compare_phage():
    pathogen_bac = input("What Bacteria Do You Want To Get Rid Of?(pls use a coma to separate between bacterias):\n")
    pathogen_bac_list = pathogen_bac.split(',')
    pathogen_phage_list = []
    human_phage_list = []
    # Read list from the file
    with open('human_associated_bacteria.txt', 'r') as filehandle:
        human_associated_bacteria = [line.rstrip() for line in filehandle]

    for pathogen in pathogen_bac_list:
        for bacteria in human_associated_bacteria:
            if bacteria == pathogen:
                human_associated_bacteria.remove(bacteria)
        pathogen_phage_list.append(bacteria_phages_dict[pathogen])
    for bacteria in human_associated_bacteria:
        human_phage_list.append(bacteria_phages_dict[bacteria])
    for phage in pathogen_phage_list:
        if phage in human_phage_list:
            pathogen_phage_list.remove(phage)
    print(pathogen_phage_list)


find_human_associated_bacteria()"""
"""compare_phage()"""

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

            for annotation in fast["annotations"]:
                found = False
                for sublist in annotation['details']:
                    if 'homo sapiens' in sublist:
                        found = True
                        break
                if found:
                    print("homo sapiens is in the list")
                    count += 1
            if count / len(fast["annotations"]) >= 0.15:
                print("********************im a piece of the human microbiome AKA: gay")
                human_associated_bacteria.append(name)
        # Save list to a file
        with open('human_associated_bacteria.txt', 'w') as filehandle:
            for item in human_associated_bacteria:
                filehandle.write('%s\n' % item)


def compare_phage(pathogen_bac_list):
    pathogen_phage_list = []
    human_phage_list = []
    phage_results = {}

    with open('human_associated_bacteria.txt', 'r') as filehandle:
        human_associated_bacteria = [line.rstrip() for line in filehandle]

    for pathogen in pathogen_bac_list:
        for bacteria in human_associated_bacteria:
            if bacteria == pathogen:
                human_associated_bacteria.remove(bacteria)

    # Create human_phage_list outside the loop
    for bacteria in human_associated_bacteria:
        for phagic in bacteria_phages_dict[bacteria]:
            human_phage_list.append(phagic)

    for pathogen in pathogen_bac_list:
        # Reset pathogen_phage_list for each pathogen
        pathogen_phage_list = [phagic for phagic in bacteria_phages_dict[pathogen]]

        filtered_phage_list = [phage for phage in pathogen_phage_list if phage not in human_phage_list]

        if not filtered_phage_list:
            less_filtered_phage_list = [phage for phage in pathogen_phage_list]
            phage_results[pathogen] = {'filtered': None, 'less_filtered': less_filtered_phage_list}
        else:
            phage_results[pathogen] = {'filtered': filtered_phage_list, 'less_filtered': None}

    return phage_results
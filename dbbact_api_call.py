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


def genus_to_16s():
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


genus_to_16s()

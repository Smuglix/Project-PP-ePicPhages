import requests
"""import getting_phages_for_bacteria
from getting_phages_for_bacteria import *"""
dbbact_api = 'https://api.dbbact.org'


res = requests.get(dbbact_api + '/sequences/get_species_seqs', json={'species': 'Escherichia coli'}).json()

print(res)
print(len(res["ids"]))

seqs = requests.get(dbbact_api + '/sequences/get_info', json={'seqids': res["ids"]}).json()
print(seqs)
print(len(seqs["sequences"]))

fast = requests.get(dbbact_api + '/sequences/get_annotations', json={'sequence': "gacgaacgctggcggcgtgcctaatacatgcaagtcgaacgcttctttcctcccgagtgcttgcactcaattggaaagaggagtggcggacgggtgagtaacacgtgggtaacctacccatcagagggggataacacttggaaacaggtg"}).json()
print(fast["annotations"])
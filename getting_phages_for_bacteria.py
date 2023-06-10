# Written by Tal Or and Ilya Adamskiy
import os
import requests
import gzip
import shutil
import pandas as pd
from dotenv import load_dotenv


def download_microbe_phage_interactions():
    url = 'http://mvp.medgenius.info/Downloads/mvp_interactions.txt.gz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }

    response = requests.get(url, stream=True, headers=headers)

    # Save the gzipped file locally
    with open('mvp_interactions.txt.gz', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Decompress the gzipped file
    with gzip.open('mvp_interactions.txt.gz', 'rb') as f_in:
        with open('mvp_interactions.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def download_taxon_id_info():
    url = 'http://mvp.medgenius.info/Downloads/superkingdom2descendents.txt.gz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }

    response = requests.get(url, stream=True, headers=headers)

    # Save the gzipped file locally
    with open('superkingdom2descendents.txt.gz', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Decompress the gzipped file
    with gzip.open('superkingdom2descendents.txt.gz', 'rb') as f_in:
        with open('superkingdom2descendents.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def download_viral_clusters_id_info():
    url = 'http://mvp.medgenius.info/Downloads/mvp_viral_clusters.txt.gz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }

    response = requests.get(url, stream=True, headers=headers)

    # Save the gzipped file locally
    with open('mvp_viral_clusters.txt.gz', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Decompress the gzipped file
    with gzip.open('mvp_viral_clusters.txt.gz', 'rb') as f_in:
        with open('mvp_viral_clusters.txt', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def file_exists(file_path):
    return os.path.isfile(file_path)


microbe_phage_interactions_file = 'mvp_interactions.txt'
taxon_id_info_file = 'superkingdom2descendents.txt'
viral_clusters_id_info = 'mvp_viral_clusters.txt'

if file_exists(microbe_phage_interactions_file) and taxon_id_info_file and viral_clusters_id_info:
    print("Yo, those files already exists, bro!")
else:
    print("Oh shit man, I couldn't find those damn files. That's a bummer. Give me sec, i'm gonna download em")
    download_microbe_phage_interactions()
    download_taxon_id_info()
    download_viral_clusters_id_info()

# Read the contents of both files into pandas dataframes
interactions_df = pd.read_csv('mvp_interactions.txt', sep='\t')
taxon_info_df = pd.read_csv('superkingdom2descendents.txt', sep='\t')

# Merge the dataframes on the columns containing taxon ID in both files
merged_df = interactions_df.merge(taxon_info_df, left_on='host_taxon_id', right_on='ncbi_taxon_id')

# Drop the redundant columns and rename for clarity
columns_to_drop = ['node_rank', 'taxon_id', 'parent_taxon_id']
if 'superkingdom_y' in merged_df.columns:
    columns_to_drop.append('superkingdom_y')
merged_df = merged_df.drop(columns_to_drop, axis=1)
merged_df = merged_df.rename(columns={'superkingdom_x': 'host_superkingdom'})

patho_dict = {}
patho_list = []

# Read mvp_interactions.txt into a DataFrame
mvp_df = pd.read_csv('mvp_interactions.txt', sep='\t')

# Read superkingdom2descendents.txt into a DataFrame
taxon_df = pd.read_csv('superkingdom2descendents.txt', sep='\t')

# Merge DataFrames based on host_taxon_id and ncbi_taxon_id
merged_df = mvp_df.merge(taxon_df, left_on='host_taxon_id', right_on='ncbi_taxon_id')

# Keep only the columns you need in the output
output_df = merged_df[
    ['interaction_uid', 'host_taxon_id', 'host_rank', 'host_superkingdom', 'viral_cluster_id', 'scientific_name']]

# Save the merged dataframe to a file
merged_df.to_csv('merged_interactions_and_taxon_info.csv', sep=',', index=False)


def create_scientific_names_list(interactions_file):
    scientific_names = []

    # Read CSV file into DataFrame
    interactions_df = pd.read_csv(interactions_file)

    # Drop duplicates from the DataFrame based on host_taxon_id
    unique_interactions_df = interactions_df.drop_duplicates(subset=['host_taxon_id'])

    # Extract the scientific names into a list
    scientific_names = unique_interactions_df['scientific_name'].tolist()

    return scientific_names


def create_bacteria_phages_dict(interactions_file, clusters_file):
    # Read CSV files into DataFrames
    interactions_df = pd.read_csv(interactions_file)
    clusters_df = pd.read_csv(clusters_file, sep='\t')

    # Merge DataFrames based on the viral cluster ID
    merged_df = interactions_df.merge(clusters_df, left_on='viral_cluster_id', right_on='cluster_id')

    # Filter the merged DataFrame on the 'is_representative' column to only keep representative sequences
    rep_sequences_df = merged_df[merged_df['is_representative'] == 1]

    # Drop duplicates by 'host_taxon_id'
    unique_interactions_df = interactions_df.drop_duplicates(subset=['host_taxon_id'])

    # Group the representative sequences by bacteria NCBI ID and extract the phage sequence names
    bacteria_phages = rep_sequences_df.groupby('host_taxon_id')['seq_name'].apply(lambda x: ', '.join([str(i) for i in x])).to_dict()

    # Create a dictionary with bacteria scientific name and NCBI ID as the key (drop duplicates before setting the index)
    bacteria_info = unique_interactions_df.set_index('host_taxon_id')[['scientific_name', 'ncbi_taxon_id']].to_dict(
        'index')
    # bacteria_phages_names_and_ids = {f"{bacteria_info[k]['scientific_name']}:{bacteria_info[k]['ncbi_taxon_id']}": v for k, v in bacteria_phages.items()}
    bacteria_phages_names_and_ids = {f"{bacteria_info[k]['scientific_name']}": v for k, v in bacteria_phages.items()}

    return bacteria_phages_names_and_ids


# Usage example:
interactions_file = 'merged_interactions_and_taxon_info.csv'
clusters_file = 'mvp_viral_clusters.txt'
bacteria_phages_dict = create_bacteria_phages_dict(interactions_file, clusters_file)
scientific_names_list = create_scientific_names_list(interactions_file)

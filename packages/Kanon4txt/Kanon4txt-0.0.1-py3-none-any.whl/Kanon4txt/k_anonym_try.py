#!/usr/bin/python3

"""
K-anonymity for texts
"""


def run_imports():

    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import re
    import os
    import argparse
    from datetime import datetime
    import time
    import warnings
    from datetime import date
    import logging
    warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")


def run_k_anon(df: pd.DataFrame, k: int, col: str = 'txt', plot: bool = False, n_jobs: int = 1,
               verbose: int = 0):
    """
    The main function. Runs the anonymization.
    """
    run_imports()
    from utils import nlp_utils, cluster_utils, utilization_utils, anonym_utils

    # # getting the input arguments
    # input_file = arguments.file  # Input database
    # k = int(arguments.k)  # Desired k degree
    # stop_file = arguments.stop  # File with list of stop words
    # col = arguments.col  # The text columns  
    # n_jobs = args.n_jobs
    # plot = args.plot

    # # df from csv
    # df = pd.read_csv(input_file)

    # prefix = get_prefix(args) 

    '''
    prefix = 'temp_prefix' # TEMP
    stop_file = 'data/1000_most_common_words.txt'
    init_logger(verbose)
    logging.info('Start')  # Logging
    '''
    nlp_utils.short_stopword_list = nlp_utils.stopwords.words('english')
    nlp_utils.long_stopword_list = list(set(nlp_utils.short_stopword_list + nlp_utils.get_list_from_file(stop_file)))

    # out_str = f'Stopword list contains {len(nlp_utils.stopword_list)} words'
    out_str = f'Stopword list contains {len(nlp_utils.short_stopword_list)}, {len(nlp_utils.long_stopword_list)} words'
    logging.info(out_str)  # Logging

    # Creating the word dictionary and word list
    word_dict = nlp_utils.create_word_dict(df[col], nlp_utils.long_stopword_list)  # this function takes too long need to make more efficient
    out_str = f'Number of unique words in dataset: {len(word_dict)}'
    logging.info(out_str)  # Logging

    # Run clustering
    cluster_dict, dist_dict, _ = cluster_utils.run_clustering(word_dict, stop_list=nlp_utils.long_stopword_list, cosine=True, n_jobs=n_jobs)
    out_str = f'Number of DBSCAN clusters:\t {len(cluster_dict)}'
    logging.info(out_str)  # Logging

    # Generalization
    df, _ = nlp_utils.replace_words_in_df(df, cluster_dict, dist_dict, word_dict, prefix=prefix)
    out_str = f'Generalization completed.'
    logging.info(out_str)  # Logging

    # Find k neighbors
    # neighbor_list = anonym_utils.find_k_neighbors_using_annoy(docs=df['anon_txt'], k=k)
    neighbor_list = anonym_utils.ckmeans_clustering(docs=df['anon_txt'], k=k, n_jobs=n_jobs)

    out_str = f'Found {len(neighbor_list)} groups of {k} neighbors'
    logging.info(out_str)  # Logging
    
    # Reduction
    force_anon_txt_annoy = anonym_utils.force_anonym(docs=df['anon_txt'], neighbor_list=neighbor_list)
    curr_k, non_anon_indexes = anonym_utils.get_anonym_degree(docs=force_anon_txt_annoy, min_k=k)
    out_str = f'Anonymity after reduction:\t\t{curr_k}\t number of un-anonymized documents: \t{len(non_anon_indexes)}'
    logging.info(out_str)  # Logging

    # Logging the un-anonymized documents
    if len(non_anon_indexes) > 0: 
        out_str = f'Un-anonymized documents: {non_anon_indexes}'
        logging.info(out_str)  # Logging

    # Adding the anonymized corpus to the dataframe
    anonym_col = 'force_anon_txt'
    df[anonym_col] = force_anon_txt_annoy
    del(force_anon_txt_annoy)  # Freeing space
    df = anonym_utils.add_neighbor_list_to_df(df, neighbor_list)
    # Counting the number of words and *
    df['num_of_words_after_forcing'] = df['force_anon_txt'].apply(lambda x: len(re.findall(r'\w+', x)))
    df['num_of_deleting_after_forcing'] = df['force_anon_txt'].apply(lambda x: len(re.findall(r'\*', x)))

    # Utilization utils
    if plot:
        plot_prefix = prefix
    else:
        plot_prefix = None
    mean_dist = utilization_utils.get_mean_semantice_distance_for_corpus(df[col], df[anonym_col], prefix=plot_prefix)
    out_str = f'Mean semantic distance before and after the anonymization process: {mean_dist}'
    logging.info(out_str)  # Logging

    # # Saving
    # if arguments.out:
    #     output_name = arguments.out
    # else:
    #     output_name = f'{prefix}_anonymized.csv'
    # out_file = 'outputs/' + output_name
    # df.to_csv(out_file, index=False)

    # out_str = f'Done. Output saved to {out_file}'
    
    logging.info('Done')  # Logging
    return df

import pandas as pd 
import numpy as np
import argparse


parser = argparse.ArgumentParser(description="""PhaTYP is a python library for bacteriophages' lifestyles prediction. 
                                 PhaTYP is a BERT-based model and rely on protein-based vocabulary to convert DNA sequences into sentences for prediction.""")
parser.add_argument('--midfolder', help='folder to store the intermediate files', type=str, default='phatyp/')
parser.add_argument('--out', help='folder to store the intermediate files', type=str, default='train.txt')
inputs = parser.parse_args()



feat_df = pd.read_csv(f'{inputs.midfolder}/bert_feat.csv')
feat_df = feat_df.drop(['label'])
feat_df.to_csv(inputs.out, index=False)
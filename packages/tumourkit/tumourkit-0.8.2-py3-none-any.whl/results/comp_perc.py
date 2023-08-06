import argparse
import pandas as pd
import numpy as np


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    return parser


def main():
    parser = _create_parser()
    args = parser.parse_args()
    mat = pd.read_csv(args.file, index_col=0).to_numpy()
    total = mat.sum()
    pred = mat[:, 2].sum()
    true = mat[2, :].sum()
    pred_perc = pred / total * 100
    true_perc = true / total * 100
    print(f'True percentage: {true_perc:.2f}\%.')
    print(f'Predicted percentage: {pred_perc:.2f}\%.')
    print(f'Difference: {np.abs(true_perc - pred_perc):.2f}\%.')


if __name__ == '__main__':
    main()
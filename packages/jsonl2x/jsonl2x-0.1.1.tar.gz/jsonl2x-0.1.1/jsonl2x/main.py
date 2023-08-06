import argparse

import pandas as pd


def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True, help='input jsonl file')
    parser.add_argument('--output', '-o', type=str, required=True, help='output csv or other file')

    args = parser.parse_args()
    return args

def main():
    args = build_args()
    lines = []
    with open(args.input, 'r') as f:
        for line in lines:
            lines.append(line)
        
    df = pd.DataFrame(lines)

    file_extension = args.output.split('.')[-1]
    writer = {
        'xlsx': pd.DataFrame.to_excel,
        'csv': pd.DataFrame.to_csv,
    }[file_extension]
    
    writer(df, args.output)
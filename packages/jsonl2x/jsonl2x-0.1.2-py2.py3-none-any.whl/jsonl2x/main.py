import json
import argparse

import pandas as pd


def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True, help='input jsonl file')
    parser.add_argument('--output', '-o', type=str, required=True, help='output csv or other file')

    # 添加可以接收多个的参数
    parser.add_argument('--fields', '-f', type=str, required=False, help='fields', action='append')

    args = parser.parse_args()
    return args

def main():
    args = build_args()
    fields = args.fields
    lines = []
    with open(args.input, 'r') as fread:
        for line in fread:
            lines.append(json.loads(line))
        
    df = pd.DataFrame(lines)

    file_extension = args.output.split('.')[-1]
    writer = {
        'xlsx': pd.DataFrame.to_excel,
        'csv': pd.DataFrame.to_csv,
    }[file_extension]
    
    df = df[fields]
    writer(df, args.output, index=False)

if __name__ == '__main__':
    main()

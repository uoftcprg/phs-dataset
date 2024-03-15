from glob import glob
from pathlib import Path
from sys import argv

import pandas as pd


def main():
    for argument in argv[1:]:
        pathnames = glob(argument, recursive=True)

        for pathname in pathnames:
            path = Path(pathname)
            df = pd.read_csv(
                path,
                index_col=0,
                dtype={
                    'cards': 'string',
                    'card_count': 'int',
                    'ranks': 'string',
                    'suits': 'string',
                    'paired': 'bool',
                    'suited': 'bool',
                    'rainbow': 'bool',
                    'category': 'string',
                    'rank': 'int',
                },
            )

            del df['cards']
            del df['suits']

            duplicate_counts = df.groupby(
                df.columns.tolist(),
                as_index=False,
            ).size().rename(columns={'size': 'combination_count'})
            df = df.merge(
                duplicate_counts,
                on=df.columns.tolist(),
                how='left',
            )
            df = df.drop_duplicates(subset=df.columns[:-1], keep='last')
            df = df.reset_index(drop=True)

            df.to_csv(path.parent / 'partial.csv')


if __name__ == '__main__':
    main()

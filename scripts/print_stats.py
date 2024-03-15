from glob import glob
from pathlib import Path
from sys import argv

import pandas as pd


def main():
    for argument in argv[1:]:
        pathnames = glob(argument, recursive=True)

        for pathname in pathnames:
            path = Path(pathname)
            full_df = pd.read_csv(
                path / 'full.csv',
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
            partial_df = pd.read_csv(
                path / 'partial.csv',
                index_col=0,
                dtype={
                    'card_count': 'int',
                    'ranks': 'string',
                    'paired': 'bool',
                    'suited': 'bool',
                    'rainbow': 'bool',
                    'category': 'string',
                    'rank': 'int',
                    'combination_count': 'int',
                },
            )
            results = full_df.groupby('category').size()

            assert (
                results
                == partial_df.groupby('category')['combination_count'].sum()
            ).all()

            print(path, f'({len(full_df)})')
            print()
            print(results)
            print()
            print()


if __name__ == '__main__':
    main()

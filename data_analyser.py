import pandas as pd


def main():
    path = "~"
    print('ok')
    meta_df = pd.read_csv(path + '/data/meta_data.csv')
    holding_df = pd.read_csv(path + '/data/holding_data.csv')

    meta_df = meta_df.head(100)
    meta_df = meta_df.set_index('symbol')
    holding_df = holding_df.set_index('symbol')

    meta_df.to_csv(path + '/data/test.csv')
    holding_df = holding_df.join(meta_df, how='inner',
                                 lsuffix='_l', rsuffix='_r')

    holding_df.to_csv(path + '/data/join_data.csv')
    stock_df = holding_df.groupby('stock_name')['weight'].sum()
    stock_df = stock_df.sort_values(axis=0, ascending=False)
    stock_df.to_csv(path + '/data/stock_rank_data.csv')

    segment_df = holding_df.groupby('segment_name')['weight'].sum()
    segment_df = segment_df.sort_values(axis=0, ascending=False)
    segment_df.to_csv(path + '/data/segment_rank_data.csv')


if __name__ == '__main__':
    main()
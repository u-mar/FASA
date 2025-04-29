if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import pandas as pd

@transformer
def transform(data, data_2, data_3):
    def safe_prepare(df, rename_map, source):
        if df is None or df.empty:
            return pd.DataFrame(columns=['reviewer', 'rating', 'date', 'text', 'response', 'source'])
        df = df.copy()
        df = df.rename(columns=rename_map)
        df['source'] = source
        return df

    app_store_df = safe_prepare(
        data,
        {
            'date': 'date',
            'rating': 'rating',
            'review': 'text',
            'title': 'title',
            'userName': 'reviewer',
        },
        'app_store'
    )
    app_store_df = app_store_df.drop(columns=['isEdited'], errors='ignore')

    google_play_df = safe_prepare(
        data_2,
        {
            'reviewId': 'review_id',
            'userName': 'reviewer',
            'content': 'text',
            'score': 'rating',
            'replyContent': 'response',
            'at': 'date',
        },
        'google_play'
    )

    google_maps_df = safe_prepare(
        data_3,
        {
            'text': 'text',
            'rating': 'rating',
            'reviewer': 'reviewer',
            'date': 'date',
            'response': 'response',
        },
        'google_maps'
    )

    common_columns = ['reviewer', 'rating', 'date', 'text', 'source','company']
    combined_df = pd.concat(
        [
            app_store_df[common_columns],
            google_play_df[common_columns],
            google_maps_df[common_columns],
        ],
        ignore_index=True
    )

    combined_df['date'] = pd.to_datetime(combined_df['date'], errors='coerce')
    combined_df.to_csv('testt.csv',index=False)

    return combined_df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

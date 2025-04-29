if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from Data_Ingestion.Scrapers.google_play import play
from Data_Ingestion.Scrapers.config import JSONManager
import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    all_data = []
    j = JSONManager()
    point = j.read()
    for company,sources in point.items():
        name = sources['play_store']['app_id']
        last = sources['play_store']['last_total_reviews']
        print(name)

        first = False
        data,new_count = play(name, last,first_time=first)
        if data is not None and not data.empty:
            data['company'] = company
            all_data.append(data)
        if new_count > last:
            j.update_review_count(company,'play_store',new_count)
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
        return df
    return pd.DataFrame()


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

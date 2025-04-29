if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from Data_Ingestion.Scrapers.google_maps import scrape_google_maps
from Data_Ingestion.Scrapers.config import JSONManager
import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    all_data = []
    j = JSONManager()
    point = j.read()
    for company,sources in point.items():
        name = sources['google_maps']['query']
        last = sources['google_maps']['last_total_reviews']

        data,new_count = scrape_google_maps(name, last)
        print(data,new_count)
        if new_count > last:
            j.update_review_count(company,'google_maps',new_count)
        if data is not None:
            data['company'] = company
            all_data.append(data)
    if all_data:
        df = pd.concat(all_data,ignore_index=True)
        return df
    return pd.DataFrame()


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

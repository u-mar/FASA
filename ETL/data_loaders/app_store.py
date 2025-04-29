if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from Data_Ingestion.Scrapers.app_store import App_store
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
        app_id = sources['app_store']['app_id']

        data = App_store(app_id)
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

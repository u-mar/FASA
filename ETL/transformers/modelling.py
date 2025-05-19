if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from Data_Ingestion.model import ModelPipeline
import pandas as pd
@transformer
def transform(data, *args, **kwargs):
    model = ModelPipeline()
    predicted = data['text'].apply(model.build).apply(pd.Series)

    df = pd.concat([data,predicted],axis=1)


    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

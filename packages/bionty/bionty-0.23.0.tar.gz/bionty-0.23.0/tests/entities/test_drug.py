import pandas as pd

import bionty as bt


def test_dron_drug_inspect_name():
    df = pd.DataFrame(
        index=[
            "LILIUM LONGIFLORIUM",
            "citrus bioflavonoids",
            "Ornithine, (L)-Isomer",
            "Hyoscyamus extract",
            "This disease does not exist",
        ]
    )

    dt = bt.Drug(source="dron", version="2023-03-10")
    inspected_df = dt.inspect(df.index, field=dt.name, return_df=True)

    inspect = inspected_df["__mapped__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, True, False])

    assert inspect.equals(expected_series)

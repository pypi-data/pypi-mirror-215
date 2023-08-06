from typing import TYPE_CHECKING

import pandas as pd

from .._tools._dataframe import convert_dtypes

if TYPE_CHECKING:
    from .context_collection import ADCContext, HPAndCustInstContext


def convert_types(column: list, column_names: list) -> list:
    date_columns = [
        i
        for i, column_name in enumerate(column_names)
        if any(i for i in ["Date", "date", "_DT", "DATE"] if i in column_name)
        and all(i if i not in column_name else False for i in ["DateType", "Dates"])
    ]
    result = [i if i is not None and i != "" else pd.NA for i in column]

    if date_columns:
        for i in date_columns:
            result[i] = pd.to_datetime(result[i])

    return result


class DataDFBuilder:
    @staticmethod
    def build_df(
        adc: "ADCContext",
        hp_and_cust_inst: "HPAndCustInstContext",
    ) -> pd.DataFrame():
        if not adc.raw and not hp_and_cust_inst.raw:
            return pd.DataFrame()

        elif hp_and_cust_inst.can_build_df:
            return hp_and_cust_inst.df

        elif adc.can_build_df:
            return adc.df

        adc_headers_names = adc.headers_names
        columns = adc_headers_names + hp_and_cust_inst.columns

        if not any(columns):
            return pd.DataFrame()

        else:
            if not adc_headers_names and hp_and_cust_inst.columns:
                columns.insert(0, "Instrument")
            elif "instrument" in columns:
                columns[columns.index("instrument")] = "Instrument"

            adc_data = adc.get_data_wid_universe_as_index()

            data = []
            for universe in hp_and_cust_inst.raw:
                if universe in adc_data:
                    for column in adc_data[universe]:
                        column.extend(hp_and_cust_inst.raw[universe])
                        data.append(column)

                else:
                    tmpl = [universe] + [pd.NA] * (len(adc_headers_names) - 1) + hp_and_cust_inst.raw[universe]
                    adc_data[universe] = tmpl
                    data.append(tmpl)

            return convert_dtypes(pd.DataFrame(data, columns=columns))

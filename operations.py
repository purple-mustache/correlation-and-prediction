import pandas as pd
from data_frame_formatter import DataFrameFormatter
from column_formatter import ColumnFormatter

xls = pd.ExcelFile("data/sample_data.xlsx")

correlation_input_df = pd.read_excel(xls, 'Correlation Input Sheet')


def correlation_operations(table:pd.DataFrame, query_element:str,
                            query_value, columns_to_drop:list, 
                            new_index_column:str, new_columns:str,
                            new_values:str):
    """
    This function will work perfectly with the correlation input sheet
    but hasn't been abstracted to work with the other sheets yet.
    Args:
        data_frame: data frame to be worked on
        query_elem: name of the column in the dataframe that you'll use 
        to filter the dataframe.
        query: the value you'll use to query the data frame
        columns_to_drop: columns you want ropped from the table as they 
        don't ai analysis.
        new_index_column: desired new index column when the table is reshaped
        new_columns: desired new columns when the table is reshaped
        new_vales: desired new index column when the table is reshaped
    """
    correlation_input_df_formatter = DataFrameFormatter(table)

    # Query table
    filter_table = correlation_input_df_formatter.query_table(query_elem=query_element, query=query_value)
    result = [item for item in filter_table]
    result = pd.concat(result)
    # print(f"Table successfully filtered with query:{result}\n\n")

    # drop useless columns
    refined_df = correlation_input_df_formatter.analysis_prep(analysis_table=result, column_names=columns_to_drop)
    refined_result = [item for item in refined_df]
    refined_df = pd.concat(refined_result)
    # print(f"Table successfully dropped columns not needed\n{refined_df}\n\n")

    #enumerate items in the desired new index column
    column_formatter = ColumnFormatter(refined_df[new_index_column])
    target_map = column_formatter.enumerate_column()
    # print(f"New index column successfully enumerated\n\n")

    # replace current values in the column with their maped enumerated equivalent(it prints a confirmation message if successful)
    column_formatter.replace_column_values(target_map=target_map)

    # problem for 2003
    # reshape the table
    reshaped_table = correlation_input_df_formatter.reshape_table(data_frame=refined_df, 
                                                                    new_columns=new_columns,
                                                                    new_index=new_index_column, 
                                                                    new_values=new_values)
    result = [item for item in reshaped_table]
    reshaped_table = pd.concat(result)
    print(result)

    # fill NaN values with 0
    reshaped_table = reshaped_table.fillna(0)

    reshaped_corr = reshaped_table.corr()
    return reshaped_corr
    


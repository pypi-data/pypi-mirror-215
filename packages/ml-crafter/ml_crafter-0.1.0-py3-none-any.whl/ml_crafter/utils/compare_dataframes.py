from typing import (
    List,
    Optional
)
import logging

import pandas as pd
import numpy as np

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class CompareDataframes:

    def __init__(
            self,
            df1: pd.DataFrame,
            df2: pd.DataFrame,
            float_cols: Optional[List[str]] = None,
            rounding_places: Optional[int] = None
    ) -> None:

        """
        params
        ------
        df1 : dataframe 1
        df2 : dataframe 2
        float_cols : columns which has data with many decimal points
        rounding_places : when comparing float columns need to round them and then compare. Set the rounding places.
        """

        self.df1 = df1.copy()
        self.df2 = df2.copy()
        self.float_cols = float_cols
        self.rounding_places = rounding_places

        self.common_cols = None
        self.cols_missing_in_df1 = None
        self.cols_missing_in_df2 = None

        if float_cols is not None and rounding_places is None:
            raise ValueError('If foat cols is specified, need to specify rounding places as well')

        if float_cols is None and rounding_places is not None:
            raise ValueError('If rounding places is specified, need to specify float cols as well')

        if self.df1.equals(self.df2):
            logging.info('The two dataframes are equal')
        else:
            logging.info('The two dataframes are different')
            logging.info(
                f'The shape of dataframe 1 is {self.df1.shape} and the shape of the dataframe 2 is {self.df2.shape}')

    def compare_column_names(self) -> None:

        """
       Compare the columns of both dataframes and put following items in
       variables
       - common columns in both dataframes : common_cols
       - columns present in df1 but missing in df2 : cols_missing_in_df2
       - columns present in df2 but missing in df1 : cols_missing_in_df1

        """

        if set(list(self.df1)) == set(list(self.df2)):
            logging.info('The columns are identical in the two dataframes')
            self.common_cols = list(self.df1)
            self.cols_missing_in_df1 = []
            self.cols_missing_in_df2 = []

            if self.df1[self.common_cols].equals(self.df2[self.common_cols]):
                logging.info('The two dataframes are equal when columns are ordered')
            else:
                logging.info('The two dataframes are different even when the columns are ordered to be the same\
                             , more analysis needed to indentify the difference')

        else:
            logging.info('The columns are different in the two dataframes')
            self.common_cols = [x for x in list(self.df1) if x in list(self.df2)]
            self.cols_missing_in_df1 = [x for x in list(self.df2) if x not in list(self.df1)]
            self.cols_missing_in_df2 = [x for x in list(self.df1) if x not in list(self.df2)]

    def get_missing_cols_in_df1(self) -> List:

        """
        returns columns that are present in df2 but missing in df1
        """
        if self.cols_missing_in_df1 is None:
            raise AttributeError("Need to run 'compare_column_names' function first")
        else:
            return self.cols_missing_in_df1

    def get_missing_cols_in_df2(self) -> List:

        """
        returns columns that are present in df1 but missing in df2
        """

        if self.cols_missing_in_df2 is None:
            raise AttributeError("Need to run 'compare_column_names' function first")
        else:
            return self.cols_missing_in_df2

    def get_common_cols_in_df1_df2(self) -> List:

        """
        returns columns that are present in both df1 and df2
        """

        if self.common_cols is None:
            raise AttributeError("Need to run 'compare_column_names' function first")
        else:
            return self.common_cols

    def set_common_cols(self, common_columns: List[str]) -> None:

        """
        If required manually set the common columns in the two
        dataframes, if this set, 'get_common_cols_in_df1_df2' function is not
        required to run
        """
        self.common_cols = common_columns

    def compare_common_cols_values(self) -> pd.DataFrame:

        """
        For common columns check which columns are different in values. For this function to work
        indexes of the dataframes and the shapes should be identical

        This function returns a dataframe with column names and showing the proportion of similar
        rows for each column, and if the similar proprotion is less than 1, it will show the indexes
        where the difference are
        """

        self.similar_props = []
        self.diff_indexes = []

        self.df1 = self.df1[self.common_cols]
        self.df2 = self.df2[self.common_cols]

        if self.df1.shape != self.df2.shape:
            raise AttributeError("shapes of the dataframes should match to continue the analysis")

        if self.float_cols is not None:
            self.invalid_float_cols = [x for x in self.float_cols if x not in self.common_cols]

            if len(self.invalid_float_cols) > 0:
                logging.info(f'Invalid columns in float cols: {self.invalid_float_cols}')
                raise KeyError('Some columns specified in float cols are not in common cols')
            else:
                for i in self.float_cols:
                    self.df1[i] = self.df1[i].round(self.rounding_places)
                    self.df2[i] = self.df2[i].round(self.rounding_places)

        for i in self.common_cols:

            # cannot compare two columns if data types are different
            if type(self.df1[i].dtype) != type(self.df2[i].dtype):

                if type(self.df1[i].dtype) == pd.core.arrays.string_.StringDtype:
                    self.df1[i] = self.df1[i].astype('str')
                if type(self.df2[i].dtype) == pd.core.arrays.string_.StringDtype:
                    self.df2[i] = self.df2[i].astype('str')
                if type(self.df1[i].dtype) == pd.core.arrays.integer.Int64Dtype:
                    self.df1[i] = self.df1[i].astype('float')
                if type(self.df2[i].dtype) == pd.core.arrays.integer.Int64Dtype:
                    self.df2[i] = self.df2[i].astype('float')

            if self.df1[[i]].equals(self.df2[[i]]):
                similar_prop = 1
                diff_indexes = None

            else:
                similar_prop = (self.df1[i] == self.df2[i]).sum() / len(self.df1)

                s = self.df1[i] == self.df2[i]
                diff_indexes = s[s == False]

            self.similar_props.append(similar_prop)
            self.diff_indexes.append(diff_indexes)

        self.df_similar_props = pd.DataFrame({'column': self.common_cols
                                                 , 'similar_prop': self.similar_props
                                                 , 'different_indexes': self.diff_indexes}).set_index('column')

        return self.df_similar_props[['similar_prop', 'different_indexes']]

    def get_different_values_df1(self, diff_col_name: str) -> pd.DataFrame:

        """
        For a given column is df1 show which values are different from df2
        """
        not_matching_index = self.df_similar_props.loc[diff_col_name, 'different_indexes']

        if not_matching_index is None:
            raise KeyError("Similarity is 100% for this feature")

        else:
            return self.df1.iloc[list(not_matching_index.index), :]

    def get_different_values_df2(self, diff_col_name: str) -> pd.DataFrame:

        """
        For a given column is df2 show which values are different from df1
        """

        not_matching_index = self.df_similar_props.loc[diff_col_name, 'different_indexes']

        if not_matching_index is None:
            raise KeyError("Similarity is 100% for this feature")

        else:
            return self.df2.iloc[list(not_matching_index.index), :]

        return self.df2.iloc[list(not_matching_index.index), :]


def get_feautre_diff_df1_df2(feature, comp_df_obj):
    df_average_distance_per_month_df1 = comp_df_obj.get_different_values_df1(feature)[[feature]]
    df_average_distance_per_month_df2 = comp_df_obj.get_different_values_df2(feature)[[feature]]

    df_merged = pd.merge(df_average_distance_per_month_df1, df_average_distance_per_month_df2
                         , left_index=True, right_index=True, suffixes=('_df1', '_df2'))

    df_merged['diff'] = abs(df_merged[f'{feature}_df2'] - df_merged[f'{feature}_df1']) / df_merged[f'{feature}_df1']
    df_merged = df_merged.replace([np.inf], 100)

    return df_merged['diff'].mean(), df_merged.shape[0]


def run_dataframe_comparison(df1,
                             df2,
                             keys=None,
                             print_col_names=False,
                             columns_to_compare=None,
                             float_rounding_places=3):
    """

    columns_to_compare : Specify the required columns to compare. If this is not specified
                         all the common columns in the two dataframes will be compared

    keys : If there are columns which give identity to each row , specify them here
           ex : 'unique identified for a row' , 'name of a customer/row' , 'DoB of a customer/row'
           if this isn't specified , it is assumed the same process was followed to generate the two dataframes
           and each the locations of each row in both dataframe match (though index may or may not match)

    print_col_names: if set to true, will print the missing columns and common columns in the two
                     dataframes

    float_rounding_places : if there are float type columns to compare, round them to n number of places
                            before comparing as there can be very small differences which should be ignored


    """

    if columns_to_compare is not None:
        cols_presnt_in_df1 = all([item in df1.columns for item in columns_to_compare])
        cols_presnt_in_df2 = all([item in df2.columns for item in columns_to_compare])

        if not (cols_presnt_in_df1 and cols_presnt_in_df2):
            raise KeyError("make sure specified columns to compare are present in both dataframes")
    else:
        logging.info('All the columns are used in the comparison')

    if keys is not None:
        keys_presnt_in_df1 = all([item in df1.columns for item in keys])
        keys_presnt_in_df2 = all([item in df2.columns for item in keys])

        if keys_presnt_in_df1 and keys_presnt_in_df2:
            df1 = df1.sort_values(keys)
            df2 = df2.sort_values(keys)
        else:
            raise KeyError("make sure specified keys are present in both dataframes")

    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    float_cols1 = [col for col in df1.columns if df1[col].dtype == float]
    float_cols2 = [col for col in df2.columns if df2[col].dtype == float]
    common_float_cols = list(set(float_cols1) & set(float_cols2))

    if len(common_float_cols) == 0:
        float_rounding_places = None

    cd = CompareDataframes(df1,
                           df2,
                           float_cols=common_float_cols,
                           rounding_places=float_rounding_places)
    cd.compare_column_names()

    cols_missing_in_df1 = cd.cols_missing_in_df1
    cols_missing_in_df2 = cd.cols_missing_in_df2

    common_cols = cd.common_cols

    if print_col_names:
        print(f'missing cols in df1:{cols_missing_in_df1}')
        print(f'missing cols in df2:{cols_missing_in_df2}')
        print(f'Common cols in df1 and df2 :{common_cols}')

    if columns_to_compare is not None:
        cd.set_common_cols(columns_to_compare)

    df_similarity = cd.compare_common_cols_values()

    common_int_cols = [col for col in df1.columns if df1[col].dtype == float]
    common_int_cols = [col for col in common_int_cols if col in cd.common_cols]

    num_cols = common_float_cols + common_int_cols

    diff_mean = []
    diff_count = []

    different_cols = list(df_similarity[df_similarity['similar_prop'] < 1].index)
    different_cols = [col for col in different_cols if col in num_cols]

    for i in different_cols:
        diff_mean.append(get_feautre_diff_df1_df2(i, cd)[0])
        diff_count.append(get_feautre_diff_df1_df2(i, cd)[1])

    df_num_diff_pct = pd.DataFrame({'Feature': different_cols, 'Mean_of_diff_pct_wrt_df1': diff_mean
                                       , 'Diff_row_number': diff_count})

    return df_similarity, df_num_diff_pct, cd


"""
example

df_test1 = pd.DataFrame(
        {
            'name': ['aaa', 'bb', 'ccc', 'ddd','aaa'],
            'id': [2,1,1,1,1],
            'salary': [10, 10000,200.2341, 100.452,50000],
            'age': [20,13, 34, 45,10],
            'height': [30, 100.3421, 0, 98.7631,123.432],
        }
    )

df_test2 = pd.DataFrame(
        {
            'name': [ 'bb','aaa', 'ccc', 'ddd1','aaa'],
            'id': [1,1,1,1,2],
            'salary': [ 10000,50000,200.2342, 100.454,10],
            'height': [100.34,123.4321, 2, 98.7631,30],
            'age': [13,10, 34, 45,20],
            'extra_col': [131,102, 343, 415,123]

        },index=[12,23,42,45,1]
    )


df_simil,df_diff_num, comp_df_object = run_dataframe_comparison(df_test1,
                                      df_test2,
                                      keys=['name','id'],
                                      columns_to_compare=None,
                                      float_rounding_places=4)


# get different items in df1 for 'salary'

comp_df_object.get_different_values_df1('salary')

# get different items in df2 for 'salary'

comp_df_object.get_different_values_df2('salary')


"""



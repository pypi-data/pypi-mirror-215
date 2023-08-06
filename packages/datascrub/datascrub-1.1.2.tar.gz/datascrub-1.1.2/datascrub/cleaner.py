import pandas as pd
import numpy as np
import datetime
import charset_normalizer
import fuzzywuzzy
from fuzzywuzzy import process
import re
from scipy import stats
from pandas.api.types import is_numeric_dtype
import emoji
import string
from googletrans import Translator


class DataClean:
    def __init__(self, obj):
      if isinstance(obj, pd.DataFrame):
        # If data is a DataFrame, return it as it is
        self.raw_data = obj
      elif isinstance(obj, str):
        # If data is a string, assume it's a file path and read the file into a DataFrame
        if obj.endswith('.csv'):      #if data is a csv file
            self.raw_data = pd.read_csv(obj)
        elif obj.endswith('.xlsx'):   #if data is an excel file
            self.raw_data = pd.read_excel(obj)
      else:
        # If the object type is not recognized, raise an error or return None as per your requirement
        raise ValueError("Invalid data type. Please provide a DataFrame or a file path.")

    def clean_data(self, columns):
        """
        Cleans text data in a pandas DataFrame.

        Parameters:
        columns (str, list): Either 'all' to clean all columns or a list of column names to clean.

        Returns:
        pd.DataFrame: DataFrame with cleaned text data.
        """
        updated_data = self.raw_data.copy()

        if columns == 'all':
            text_columns = updated_data.select_dtypes(include='object').columns
            print(text_columns)
        elif isinstance(columns, list):
            text_columns = [col for col in columns if col in updated_data.columns]
        else:
            raise ValueError("Invalid value for 'clean' parameter. It should be 'all' or a list of column names.")

        # Clean text columns
        for column in text_columns:
            updated_data[column] = updated_data[column].str.strip()
            updated_data[column] = updated_data[column].str.lower()
            updated_data[column] = updated_data[column].apply(lambda x: emoji.demojize(str(x)))

        return updated_data

    def handle_missing_values(self, missing_values):
        """
        Handles missing values in a pandas DataFrame. Actions depend on the `missing_values` dictionary provided.

        Parameters:
        missing_values (dict): Dictionary with actions to be taken on missing values.
                               Keys: Column names.
                               Values: Operations to be performed on corresponding column.
                                       "replace missing value with <value>" to replace missing values with <value>.
                                       "drop" to drop rows with missing values.
                                       "fill with backward fill along rows" to fill missing values using backward fill along rows.
                                       "fill with backward fill along columns" to fill missing values using backward fill along columns.

        Returns:
        pd.DataFrame: DataFrame with handled missing values.
        """
        for column, operation in missing_values.items():
            if operation.startswith("replace missing value with "):
                value = operation.split("replace missing value with ")[1]
                try:
                    value = float(value)
                except ValueError:
                    value = str(value)
                self.raw_data[column] = self.raw_data[column].fillna(value)
            elif operation == "drop":
                self.raw_data.dropna(subset=[column], inplace=True)
            elif operation == "fill with backward fill along rows":
                self.raw_data[column] = self.raw_data[column].fillna(method='bfill', axis='rows').fillna(0)
            elif operation == "fill with backward fill along columns":
                self.raw_data[column] = self.raw_data[column].fillna(method='bfill', axis='columns').fillna(0)
            else:
                raise ValueError(f"Invalid operation '{operation}' in 'missing_values' parameter.")
        return self.raw_data

    def perform_scaling_normalization(self):
        """
        NOT COMPLETE!!!

        Performs scaling normalization on numerical columns in a pandas DataFrame using Box-Cox transformation.

        Returns:
        pd.DataFrame: DataFrame with scaled and normalized numerical data.
        """
        updated_data = self.raw_data.copy()
        for column in updated_data.columns:
            if is_numeric_dtype(updated_data[column]):
                updated_data[column] = updated_data[column].apply(lambda x: abs(x) if x != 0 else 1)
                updated_data[column] = stats.boxcox(updated_data[column])
        return updated_data

    def explode_data(self, explode):
        """
        Splits and expands data in specified columns of a pandas DataFrame.

        Parameters:
        explode (dict): Dictionary with column names as keys and separator as values for splitting.

        Returns:
        pd.DataFrame: DataFrame with exploded data.
        """
        updated_data = self.raw_data.copy()
        for column, separator in explode.items():
            updated_data[column] = updated_data[column].str.split(separator)
            updated_data = updated_data.explode(column)
        return updated_data

    def dupli(self):
        """
        Removes duplicate rows from a pandas DataFrame.

        Returns:
        pd.DataFrame: DataFrame without duplicate rows.
        """
        return self.raw_data.drop_duplicates()

    def parse_date_column(self, date_columns):
        """
        Converts specified columns in a pandas DataFrame to datetime format and formats them as 'YYYY-MM-DD'.

        Parameters:
        date_columns (dict): List of column names to be converted to datetime format.

        Returns:
        pd.DataFrame: DataFrame with parsed date columns.
        """
        updated_data = self.raw_data.copy()

        for column in date_columns:
            if column not in updated_data.columns:
                raise ValueError(f"Column '{column}' not found in the DataFrame.")

            if updated_data[column].dtype != 'datetime64[ns]':
                updated_data[column] = updated_data[column].astype(str)
                updated_data[column] = pd.to_datetime(updated_data[column], errors='coerce').dt.strftime('%Y-%m-%d')
                # updated_data[column] = pd.to_datetime(updated_data[column], format=date_format)

        return updated_data

    def translate_columns(self, translations):
        """
        Translates text in specified columns of a DataFrame to English using Google Translate.

        Parameters:
        translations (dict): Dictionary mapping column names to overwrite boolean values.
                             The key is the column name, and the value is the overwrite boolean value.

        Returns:
        pd.DataFrame: DataFrame with translated columns.
        """
        translator = Translator()
        updated_data = self.raw_data.copy()

        for column, overwrite_value in translations.items():
            if column not in updated_data.columns:
                raise ValueError(f"Column '{column}' not found in the DataFrame.")

            translated_texts = []

            for text in updated_data[column]:
                translation = translator.translate(text)
                translated_texts.append(translation.text)

            if overwrite_value:
                updated_data[column] = translated_texts
            else:
                new_column_name = column + '_translated'
                updated_data[new_column_name] = translated_texts

        return updated_data

    def prep(self, clean='all', missing_values={}, perform_scaling_normalization_bool=False, explode={}, parse_date=[], translate_column_names={}):
        """
        Main function to prepare and clean a pandas DataFrame. Can perform cleaning, handle missing values, fix inconsistencies,
        perform scaling normalization, explode data, and parse date columns based on parameters passed.

        Parameters:
        clean (str, list): Columns to clean. Either 'all' for all columns or a list of specific column names.
        missing_values (dict): Actions to be taken on missing values. Refer `handle_missing_values` for more details.
        perform_scaling_normalization (bool): If True, will perform scaling normalization on numerical columns.
        explode (dict): Columns to be exploded. Keys are column names and values are separators for splitting.
        parse_date (list): List of column names to be converted to datetime format.
        translate_column_names (dict): Dictionary mapping column names to overwrite boolean values for translation.

        Returns:
        pd.DataFrame: Updated DataFrame with cleaned and processed data.
        """
        if missing_values:
            self.raw_data = self.handle_missing_values(missing_values)

        if parse_date:
            self.raw_data = self.parse_date_column(parse_date)

        if translate_column_names:
            self.raw_data = self.translate_columns(translate_column_names)

        if clean:
            self.raw_data = self.clean_data(clean)

        if perform_scaling_normalization_bool:
            self.raw_data = self.perform_scaling_normalization()

        if explode:
            self.raw_data = self.explode_data(explode)

        self.raw_data = self.dupli()

        return self.raw_data

# Import CSV to an existing database in the instance folder using sqlite3
from pathlib import Path
import sqlite3
import pandas as pd


if __name__ == '__main__':

    # ---------------------------------------------
    # Open the database using sqlite3
    # ---------------------------------------------

    # Define the database file name and location
    db_file = Path(__file__).parent.parent.joinpath("instance", "paralympics.sqlite")

    # Connect to the database
    connection = sqlite3.connect(db_file)

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # -------------------------
    # Add the data using pandas
    # -------------------------

    # Read the noc_regions data to a pandas dataframe
    # Additional string to read as null value https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    na_values = ["",]
    noc_file = Path(__file__).parent.parent.joinpath("data", "noc_regions.csv")
    noc_regions = pd.read_csv(noc_file, keep_default_na=False, na_values=na_values)

    # Read the paralympics event data to a pandas dataframe
    event_file = Path(__file__).parent.parent.joinpath("data", "paralympic_events.csv")
    paralympics = pd.read_csv(event_file)

    # Write the data to tables in a sqlite database
    # if_exists="replace" If there is data in the table, replace it
    #  index=False Do not write the pandas index column to the database table
    noc_regions.to_sql("region", connection, if_exists="replace", index=False)
    paralympics.to_sql("event", connection, if_exists="replace", index=False)

    # close the database connection
    connection.close()

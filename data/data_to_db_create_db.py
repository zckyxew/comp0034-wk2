# Create database and import data from CSV to database table using sqlite3
from pathlib import Path
import sqlite3
import pandas as pd

# ---------------------------------------------
# Define and create the database using sqlite3
# ---------------------------------------------

# Define the database file name and location
db_file = Path(__file__).parent.joinpath("paralympics.sqlite")

# Connect to the database
connection = sqlite3.connect(db_file)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# 'region' table definition in SQL
create_region_table = """CREATE TABLE if not exists region(
                NOC TEXT PRIMARY KEY,
                region TEXT NOT NULL,
                notes TEXT);
                """

# 'event' table definition in SQL
create_event_table = """CREATE TABLE if not exists event(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    year INTEGER,
    country TEXT,
    host TEXT,
    NOC TEXT,
    start TEXT,
    end TEXT,
    duration INTEGER,
    disabilities_included TEXT,
    events INTEGER,
    sports INTEGER,
    countries INTEGER,
    participants_m INTEGER,
    participants_f INTEGER,
    participants INTEGER,
    highlights TEXT,
    FOREIGN KEY(NOC) REFERENCES region(NOC));"""

# Create the tables in the database
cursor.execute(create_region_table)
cursor.execute(create_event_table)

# Commit the changes
connection.commit()

# -------------------------
# Add the data using pandas
# -------------------------

# Read the noc_regions data to a pandas dataframe
na_values = ["",]
noc_file = Path(__file__).parent.joinpath("noc_regions.csv")
noc_regions = pd.read_csv(noc_file, keep_default_na=False, na_values=na_values)

# Read the paralympics event data to a pandas dataframe
event_file = Path(__file__).parent.joinpath("paralympic_events.csv")
paralympics = pd.read_csv(event_file)

# Write the data to tables in a sqlite database
noc_regions.to_sql("region", connection, if_exists="append", index=False)
paralympics.to_sql("event", connection, if_exists="append", index=False)

# close the database connection
connection.close()

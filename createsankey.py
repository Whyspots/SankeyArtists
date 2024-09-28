"""
Created on 09/22/2024

@author: Anne Hu
NUID: 002281701
DS3500 Advanced programming with data

Datasets used: artists.json- a json file containing information about
artists whose work was featured in the museum of contemporary art.

This program creates sankey diagrams based off specified data.

"""
import json
import pandas as pd
import math
import sankey as sk

FILENAME = "data/artists.json"


def clean_df(filename):
    """
    Generates a cleaned dataframe for artists.json given its file path.
    :param filename: The path/name for artists.json
    :return: df: The cleaned dataframe.
    """

    with open(filename, 'r') as file:
        #Saves the json data as a list of dictionaries.
        data = json.load(file)

    #Makes the list of dictionaries a dataframe, drops any empty value rows.
    df = pd.DataFrame(data)
    df = df[["ArtistBio", "Nationality","Gender"]].dropna()

    #Creates a list containing decade born values that will be in a future df column.
    decade = []

    for bio in df["ArtistBio"]:

        #For each row in ArtistBio, drop all non numeric characters.
        numeric = ''.join([char for char in bio if char.isdigit()])

        if (numeric == ''):
            numeric = '0'

        #If the death year is included, it is dropped.
        if (len(numeric) >= 4):
            numeric = numeric[:4]

        #Clean birth year value appended to decade after rounding down to closest 10.
        decade.append(str(math.floor(int(numeric) / 10) * 10))

    df["DecadeBorn"] = decade

    #Drop artistbio column as it is no longer needed.
    df = df.drop('ArtistBio', axis=1)

    #Drop any row where decadeborn is 0 (missing data).
    df = df = df[df['DecadeBorn'] != "0"]

    #Reset index for ease of navigation later on.
    df.reset_index(drop=True, inplace=True)

    #Change "male" to "Male" for consistency.
    df['Gender'].replace(['male'], 'Male' , inplace = True)

    #Sort by decade born
    df.sort_values(by=['DecadeBorn'])

    return df



def sankey_visualize(df , source_title, target_title, filter_value , *cols):
    """
    Creates sankey diagrams based off specified data.

    :param df: Dataframe containing the data for sankey.
    :param source_title: The column title for the sources.
    :param target_title: The column title for the targets.
    :param filter_value: The threshold for filtering. (Anything below is dropped)
    :param cols: A list of columns (optional) to be stacked.
    :return: NONE (Outputs diagram)
    """
    #If any cols are given, replace the normal dataframe with a stacked one.
    if cols != ():
        df = sk._stack_df(df,cols)

        #ReName source and target titles to the arbitrary labels.
        source_title = "src"
        target_title = "targ"

    #source is a string, and it is name of column that is source.
    df_agg = df.groupby([source_title, target_title]).size().reset_index(name='count')

    # Drops all rows where the count is below specified filter value.
    df_agg = df_agg[df_agg['count'] >= filter_value]

    # Make a sankey visualization:
    sk.make_sankey(df_agg, source_title, target_title, cols = cols, vals = 'count')



def main():
    df = clean_df(FILENAME)

    #Visual one
    sankey_visualize(df, "Nationality", "DecadeBorn" , 60)

    #Visual two
    sankey_visualize(df, "Nationality", "Gender" , 100 )

    #Visual three
    sankey_visualize(df, "Gender", "DecadeBorn" , 100)

    #Visual four
    sankey_visualize(df, "Gender", "DecadeBorn" ,
                     100 , "DecadeBorn" ,"Gender","Nationality")

if __name__ == '__main__':
    main()
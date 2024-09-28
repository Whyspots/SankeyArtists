"""
File: sankey.py
Author: John Rachlin (Modified by Anne Hu)

Description: A wrapper library for plotly sankey visualizations

"""

import pandas as pd
import plotly.graph_objects as go

pd.set_option('future.no_silent_downcasting', True)


def _code_mapping(df, src, targ):
    """
    Map labels in src and targ colums to integers
    :param: df: Dataframe with at least 1 column and 1 row.
    :param: src: Name of the source column.
    :param: targ: Name of the target column.
    :return: df: Maps labels in src and targ as integers.
    :return: labels: Maps labels in src and targ as integers.
    """

    # Get the distinct labels (as strings)
    labels = sorted(list(set(list(df[src].astype(str)) + list(df[targ].astype(str)))))

    # Create a label->code mapping
    codes = range(len(labels))
    lc_map = dict(zip(labels, codes))

    # Substitute codes for labels in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels



def _stack_df(df, cols):
    """
    Returns stacked df when given a dataframe and a list of column names to stack.

    :param df: A dataframe of at least 3 columns.
    :param cols: List of column names to be stacked.
    :return: stacked: A stacked dataframe.
    """

    #Initializes an empty list of dataframes.
    dfs = []

    #Iterates through indices.
    for i in range(len(cols) - 1):

        #Creates a temporary dataframe whose value is replace w/ each loop
        df_temp = pd.DataFrame()

        #Assigns arbitrary 'src' and 'targ' for the two columns added to the dataframe.
        df_temp['src'] = df[cols[i]]
        df_temp['targ'] = df[cols[i + 1]]

        #Append temp dataframe to the list of dataframes.
        dfs.append(df_temp)

    #Stacks the list of dataframes vertically. Resets their indices.
    stacked = pd.concat(dfs, axis=0).reset_index(drop=True)

    return stacked



def make_sankey(df, src, targ, vals=None, *cols, **kwargs):
    """
    Create a sankey figure
    df - Dataframe
    src - Source node column
    targ - Target node column
    vals - Link values (thickness)
    *cols - Names of columns that are to be stacked

    """

    #If desired vals are passed to the function, assign them accordingly.
    if vals:
        values = df[vals]

    #Establishes default values as 1s when vals not given.
    else:
        values = [1] * len(df)

    #Maps labels in src and targ as integers.
    df, labels = _code_mapping(df, src, targ)

    #Assigns src, targ, and values into a dictionary accordingly.
    link = {'source': df[src], 'target': df[targ], 'value': values}

    #If given in kwargs, assign thickness to thickness.
    thickness = kwargs.get("thickness", 50) # 50 is the presumed default value

    # If given in kwargs, assign pad to pad.
    pad = kwargs.get("pad", 80) #80 is the presumed default value.

    # Assigns variable values to dictionary accordingly.
    node = {'label': labels, 'thickness': thickness, 'pad': pad}

    #Creates the sankey visualization.
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()





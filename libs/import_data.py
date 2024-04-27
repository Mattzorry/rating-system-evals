from libs.google import pull_sheet_data
import re


def get_match_data():

    # pull the data
    df = pull_sheet_data()

    # format the names to make them consistent
    for col in 'p1', 'p2':
        df.loc[:, col] = df[col].apply(format_name)

    return df


def format_name(name):
    # rip out nicknames to double quotes don't break things
    name = re.sub(r"\"[^\"]+\"", '', name)

    # rip out ranks since they're not always there
    name = re.sub(r"\([^)]*\)", '', name)
    
    # get rid of extra spaces left over from the removal
    name = name.replace('  ',' ').strip()

    return name
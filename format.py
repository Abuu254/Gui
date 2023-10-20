"""
Formating the output
"""

# this function takes in a list of agents and sorts according to the pars the
# agents are associated with provided in a paranthesis
def sort_part(lst):
    """
    Sort by agent first and then part
    """
    def key_func(str_):
        words = str_.split("(")
        agent = words[0]
        if len(words) > 1:
            part = words[1].rstrip(")")
        else:
            part = ""
        return (agent, part)
    return sorted(lst, key=key_func)

# this function converts the comma separated string into a list
def string_to_list(str_):
    """
    A function that sorts a string separated by comma by putting it into list
    """
    str_to_list = str_.split(",")
    return str_to_list



def format_row(row):
    """
    A function that format a row as specified in the problem set
    """
    output = []
    output.append(row[0])
    output.append(row[1])
    output.append(row[2])
    output.append(','.join(sort_part(string_to_list(row[3]))))
    output.append(','.join(sorted(string_to_list(row[4]))))
    return output



def format_date(start_date, end_date):
    """
    # A function that formats date in the appropriate format
    """
    # Slice, take the only first part of the date
    start_year = start_date[:4] if start_date is not None else ""
    end_year = end_date[:4] if end_date is not None else ""
    if start_year == "" and end_year != "":
        return "-" + end_year
    elif start_year != "" and end_year == "":
        return start_year + "-"
    elif start_year != "" and end_year != "":
        return start_year + "-" + end_year
    else:
        return "-"

def sort_list(lst):
    """
    Sorts the given list in ascending order of second index of the sublists,
    then first index, then third and finally by fourth.
    """
    new_list = sorted(lst, key=lambda x: (x[1], x[0], x[2], x[4]))

    formated_produced = []
    for value in new_list:
        entry = {}
        entry["part"] = value[0]
        entry["name"] = value[1]
        entry["timespan"] = format_date(value[2], value[3])
        entry["nationalities"] = value[4]
        formated_produced.append(entry)
    return formated_produced


def format_class(words):
    """A function that formats classification"""
    lst = string_to_list(words)
    sorted_lst = sorted(lst)
    return ",".join(sorted_lst)


def format_info(lst):
    """a function that formats info"""
    new_list = sorted(lst, key=lambda x: (x[0], x[1]))
    formated_info = []
    for value in new_list:
        entry = {}
        entry["type"] = value[0]
        entry["content"] = value[1]
        formated_info.append(entry)

    return formated_info

# Stolen from https://github.com/rhysmeister/mmo/blob/master/python/app/mm
def create_format_string(headers, header_lookup, list_of_documents):
    """
    This function attempts to create an appropriate format stirng for displaying data on the screen in a efficient way.
    The space required for each column should be either (header + 1) or (maximum length of the data item + 1) which ever is greater
    Need to check positions rather than names as column header don't always match the keys names <- Needs rethinking!
    :param headers:
    :param header_lookup: Dictionary containing header and the name of the actual data item
    :param list_of_documents:
    :return:
    """
    # have we got what we expect
    isinstance(headers, list)
    isinstance(list_of_documents, list)
    isinstance(list_of_documents[0], dict)
    debug = False
    if debug:
        print list_of_documents
    format_string = ""
    header_lengths = {}
    for item in headers:
        header_lengths[item] = len(item)
    for doc in list_of_documents:
        for mydict in header_lookup: # Only check the keys provided in the headers
            for item in mydict.keys():
                if mydict[item].count(".") > 0: # Multi-depth keys
                    try:
                        if mydict[item].count(".") == 1: # TODO Must be a better way of doing this dynamically?
                            if len(str(doc["command_output"][mydict[item].split(".")[1]])) > header_lengths[item]:
                                header_lengths[item] = len(str(doc["command_output"][mydict[item].split(".")[1]]))
                        elif mydict[item].count(".") == 2:
                            if len(str(doc["command_output"][mydict[item].split(".")[1]][mydict[item].split(".")[2]])) > header_lengths[item]:
                                header_lengths[item] = len(str(doc["command_output"][mydict[item].split(".")[1]][mydict[item].split(".")[2]]))
                        else:
                            raise Exception("command_output keys of greater than 2 are not supported!")
                            sys.exit(-1)
                    except Exception as excep:
                        if debug:
                            print "This is here for the situation when certain keys don't exist. For example if the MMAP engine is used or not"
                            print excep
                        pass
                else:
                    if len(str(doc[mydict[item]])) > header_lengths[item]:
                        header_lengths[item] = len(str(doc[mydict[item]]))
    field_counter = 0
    for mydict in header_lookup:
        for item in mydict.keys():
            format_string = format_string + " {" +str(field_counter) + ":<" + str(header_lengths[item] + 1) + "}"
            field_counter += 1 # Add so we can support python 2.6
    format_string = format_string.strip()
    if debug:
        print format_string
    return format_string

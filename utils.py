def get_width(elem):
    """
    Extract width data from the width css settings.
    """
    if '%' in elem:
        width = float(elem.replace('%', ''))/100
    elif 'ch' in elem:
        width = int(elem.replace('ch', ''))

    return width


def get_width_for_each_col(row):
    # if no width settings, default is average width
    try:
        widths = list(map(lambda x: get_width(x['width']), row))
    except:
        widths = [float(1/len(row)) for _ in range(len(row))]

    return widths


def add_tabs(table_size, widths, row, i):
    """
    Add empty characters 
    """
    if widths[i] <= 1:
        tabs = ' ' * int(table_size*widths[i]-len(row[i]))
    else:
        tabs = ' ' * int(widths[i]-len(row[i]))
    return tabs


def draw_table(tbl_header_adj, tbl_data_adj, widths, table_size):

    tbl_str = ''

    # make row-wise border
    middle = []
    for i, w in enumerate(widths):
        if w <= 1:
            length = table_size*w
        else:
            length = w

        if i == 0:
            middle.append('=' * int(length-2))
        else:
            middle.append('=' * int(length-1))
    header_border = '+' + '+'.join(middle) + '+\n'
    
    # draw table header
    tbl_str += header_border
    tbl_str += ''.join(tbl_header_adj)
    tbl_str += '\n'
    tbl_str += header_border
    
    # draw table rows
    row_border = header_border.replace('=', '-')
    for row in tbl_data_adj:
        tbl_str += ''.join(row)
        tbl_str += '\n'
        tbl_str += row_border
    
    return tbl_str
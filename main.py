#========================================================#
# Run: $python main.py -f [html file path]
#      or 
#      $python main.py -f [html file path] > output.txt
#========================================================#

import bs4
import argparse
import collections
from bs4 import BeautifulSoup

from utils import get_width, get_width_for_each_col, add_tabs, draw_table


def parse_table_width(table_elem):
    """
    Parse table element with table size specified in width='100%' format.
    """
    tbl_data = []
    widths = []
    rows = table_elem.find_all('tr')

    for i, row in enumerate(rows):
        if i == 0:
            header = row.find_all("th", width=True)
            if len(header) == 0:
                header = row.find_all("th")

            tbl_header = [ele.text.strip() for ele in header]
            widths = get_width_for_each_col(header)
        else:
            cols = row.find_all('td', width=True)
            if len(cols) == 0:
                cols = row.find_all('td')

            cols = [ele.text.strip() for ele in cols]
            tbl_data.append([ele for ele in cols if ele]) # Get rid of empty values
            widths = get_width_for_each_col(cols)
    
    return tbl_header, tbl_data, widths


def make_table(tbl_header, tbl_data, widths, table_size):
    """
    Render table with different size setting.
    """
    tbl_header_adj, tbl_data_adj = [], []
    
    # make header
    for i in range(len(tbl_header)):
        tabs = add_tabs(table_size, widths, tbl_header, i)
        if i == 0:
            tbl_header_adj.append('|' + tbl_header[i] + tabs[:-2] + '|')
        else:
            tbl_header_adj.append(tbl_header[i] + tabs[:-1] + '|')
    
    # make data rows
    for row in tbl_data:
        new_row = []
        for i in range(len(row)):
            tabs = add_tabs(table_size, widths, row, i)
            if i == 0:
                new_row.append('|' + row[i] + tabs[:-2] + '|')
            else:
                new_row.append(row[i] + tabs[:-1] + '|')
        tbl_data_adj.append(new_row)

    tbl_str = draw_table(tbl_header_adj, tbl_data_adj, widths, table_size)
    
    return tbl_str


def bfs_parse_html(soup):
    """
    Parse html file in BFS (Breadth First Search) order.
    """
    queue = collections.deque([([], soup)])

    out = []

    while queue:
        path, element = queue.popleft()
        if hasattr(element, 'children'):  # check for leaf elements
            for child in element.children:
                if isinstance(child, bs4.element.Tag):
                    queue.append((path + [child.name if child.name is not None else type(child)],
                                  child))
        if len(path) > 0:
            if path[-1] == 'title':
                out.append(element.text.strip())
            elif path[-1] == 'p':
                out.append(element.text.strip() if isinstance(element, bs4.element.Tag) else element)
            elif path[-1] == 'table':
                try:
                    table_size = get_width(element['width'])
                    if table_size <= 1:
                        table_size *= 80  # default full width table is of 80 characters wide
                except:
                    table_size = 80

                tbl_header, tbl_data, widths = parse_table_width(element)
                tbl_str = make_table(tbl_header, tbl_data, widths, int(table_size))
                out.append(tbl_str)
#         print(path, repr(element.string[:50]) if element.string else type(element))
    
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="html file path")
    args = parser.parse_args()

    html_path = args.file

    # open html file
    with open(html_path, 'r') as f:
        html_text = f.read()

    # parse html file
    soup = BeautifulSoup(html_text, "html.parser")
    out = bfs_parse_html(soup)

    # print txt format html page to screen
    out_text = ''
    for row in out:
        out_text += row
        out_text += '\n\n'

    print(out_text)
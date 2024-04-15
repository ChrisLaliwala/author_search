"""Contains command line utility"""

import click
from .utils import get_works, get_h_index, make_author_list, sort_authors


@click.command(
    help="Search for authors with keywords. Pass up to 3 strings. \
        Adding more keywords will expand search \
        (all authors associated with any keyword will be returned). \
        Ex: author_search choose, 'three keywords', max"
)
@click.argument("keywords", nargs=-1, type=click.STRING)
@click.option("--num_authors", default=5, help="max no. of authors to return.")
def main(keywords, num_authors):
    """Command line utility that searches for authors from keywords."""
    # get works related to chosen keywords
    data_list = get_works(keywords)

    # make a list of authors associated with those works
    author_list = make_author_list(data_list)
    print("Total number of authors found: ", len(author_list))

    # make a dict mapping author to corresponding h-index
    hindex_dict = dict.fromkeys(author_list)
    # make a dict mapping author to corresponding data from openAlex
    author_data_dict = dict.fromkeys(author_list)

    for author in author_list:
        author_data, author_hindex = get_h_index(author)
        author_data_dict[author] = author_data
        hindex_dict[author] = author_hindex

    # sort dictionary of authors by their h_index in descending order.
    sorted_hindex_dict = sort_authors(hindex_dict)

    # print out authors with highest h-indices (top 5)
    print("\n")
    for count, author in enumerate(sorted_hindex_dict):
        display_name = author_data_dict[author]["display_name"]
        hindex = sorted_hindex_dict[author]
        if count < num_authors:
            author_name_str = f"{count+1}) {display_name},"
            author_info_str = f"orcid: {author}, h-index: {hindex}"
            print(author_name_str + " " + author_info_str)

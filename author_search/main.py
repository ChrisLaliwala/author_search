"""Contains command line utility"""

import click
from .utils import get_works, get_h_index, make_author_list, sort_authors


@click.command(
    help="""Search for authors with keywords. Pass up to 3 strings. 
        Adding more keywords will expand search 
        (all authors associated with any keyword will be returned). 
        Ex: author_search choose, 'three keywords', max
        """
)
@click.argument("keywords", nargs=-1, type=click.STRING)
@click.option(
    "--num_authors", default=5, help="max no. of authors that can be returned."
)
@click.option(
    "--save_output_file",
    default=None,
    type=click.Path(),
    help="specify path to file where output will be saved.",
)
def main(keywords, num_authors, save_output_file):
    """Command line utility that searches for authors from keywords."""
    # get works related to chosen keywords
    data_list, keyword_search_str = get_works(keywords)

    # make a list of authors associated with those works
    author_list = make_author_list(data_list)
    num_authors_found = len(author_list)
    authors_found_str = f"Total number of authors found: {num_authors_found}"
    print(authors_found_str)

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

    # print out authors with highest h-indices
    str_list = []
    print("\n")
    for count, author in enumerate(sorted_hindex_dict):
        display_name = author_data_dict[author]["display_name"]
        hindex = sorted_hindex_dict[author]
        if count < num_authors:
            author_name_str = f"{count+1}) {display_name},"
            author_info_str = f"orcid: {author}, h-index: {hindex}"
            print(author_name_str + " " + author_info_str)
            str_list.append(author_name_str + " " + author_info_str)

    # save to file if not None
    if save_output_file is not None:
        try:
            with open(save_output_file, "w") as file:
                file.write(keyword_search_str)
                file.write("\n")
                file.write(authors_found_str)
                file.write("\n")
                for str in str_list:
                    file.write("\n")
                    file.write(str)
        except Exception as error:
            click.echo(f"Error writing file: {error}")

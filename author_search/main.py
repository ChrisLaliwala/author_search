import click
from .utils import get_works, get_h_index, make_author_list, sort_authors


@click.command(
    help="author keywords. Pass up to 3 separated by spaces. Ex: author_search three keywords max"
)
@click.argument("keywords", nargs=-1, type=click.STRING)
def main(keywords):

    # get works related to chosen keywords
    data = get_works(keywords)
    # make a list of authors associated with those works
    author_list = make_author_list(data)

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
        if count < 5:
            print(f"{count+1}) {display_name}, orcid: {author}, h-index: {hindex}")

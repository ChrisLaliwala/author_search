"""Define utility functions for our package."""
import time
import sys
import requests


def get_works(keywords):
    """
    Function that takes in keywords and returns
    works data from openAlex.
    """
    # make sure no more than 3 keywords have been passed.
    if len(keywords) > 3:
        sys.exit("ERROR. More than three keywords have been chosen.")

    print("The keyword(s) that will be used in the search is/are: ", keywords)

    data_list = []
    for keyword in keywords:
        time.sleep(0.1)
        query = "+".join(keyword.split())
        url = f"https://api.openalex.org/works?filter=keywords.keyword:{query}"
        req = requests.get(url)
        data = req.json()
        data_list.append(data)

    return data_list


def make_author_list(data_list):
    """
    Function that makes a list of authors
    based on the works that were returned
    from openAlex.
    """
    author_list = []
    for data in data_list:
        for work in data["results"]:
            for author in work["authorships"]:
                author_id = author["author"]["orcid"]
                # print(author_id)

                # check to see if author is
                # already added to list to avoid duplicates.
                # check to see if author has an orcid, if not, won't be added.
                if (author_id in author_list) is False:
                    if author_id is not None:
                        author_list.append(author_id)

    return author_list


def get_h_index(author):
    """
    Function that returns the h-index of an author.
    """
    time.sleep(0.1)
    url = f"https://api.openalex.org/authors/https://orcid.org/{author}"
    req = requests.get(url)
    data = req.json()

    return data, data["summary_stats"]["h_index"]


def sort_authors(hindex_dict):
    """
    This function takes in an unsorted dictionary of
    authors and sorts them in descending order by h-index.
    """
    # sort authors by h_index in descending order.
    sorted_h_index_dict = dict(
        sorted(hindex_dict.items(), key=lambda x: x[1], reverse=True)
    )

    return sorted_h_index_dict

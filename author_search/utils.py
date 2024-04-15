import requests
import time
import sys


def get_works(keywords):
    # make sure no more than 3 keywords have been passed.
    if len(keywords) > 3:
        sys.exit("ERROR. More than three keywords have been chosen.")

    # TEMPORARY
    word = keywords[0]
    print("The keyword that will be used in the search is: ", word)
    query = "+".join(word.split())

    url = f"https://api.openalex.org/works?filter=keywords.keyword:{query}"
    req = requests.get(url)
    data = req.json()

    return data


def get_h_index(author):
    time.sleep(0.1)
    url = f"https://api.openalex.org/authors/https://orcid.org/{author}"
    req = requests.get(url)
    data = req.json()

    return data, data["summary_stats"]["h_index"]


def make_author_list(data):
    author_list = []
    for work in data["results"]:
        for author in work["authorships"]:
            author_id = author["author"]["orcid"]

            # check to see if author is
            # already added to list to avoid duplicates.
            # check to see if author has an orcid, if not, won't be added.
            if (author_id in author_list is False) and (author_id is not None):
                author_list.append(author_id)

    return author_list


def sort_authors(hindex_dict):
    # sort authors by h_index in descending order.
    sorted_h_index_dict = dict(
        sorted(hindex_dict.items(), key=lambda x: x[1], reverse=True)
    )

    return sorted_h_index_dict

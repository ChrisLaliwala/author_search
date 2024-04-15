"""Tests for package."""

import requests
import pytest
from .utils import get_works, get_h_index, make_author_list, sort_authors


def load_data():
    """get data for tests."""
    keywords = "outer-approximation"
    url = f"https://api.openalex.org/works?filter=keywords.keyword:{keywords}"
    try:
        req = requests.get(url, timeout=5)  # 5 seconds
    except requests.exceptions.Timeout:
        print("Request timed out.")
    test_data = req.json()
    return test_data


def load_author_data():
    """ "get author data for tests."""
    orcid = "https://orcid.org/0000-0003-3875-4441"
    url = f"https://api.openalex.org/authors/{orcid}"
    try:
        req = requests.get(url, timeout=5)  # 5 seconds
    except requests.exceptions.Timeout:
        print("Request timed out.")
    test_author_data = req.json()
    return test_author_data


def test_get_works():
    """
    Test if get_works function is working properly.
    """
    test_data = load_data()

    first_elem_test = test_data["results"][0]

    data_list, _ = get_works(("outer-approximation",))
    data = data_list[0]
    first_elem = data["results"][0]

    assert first_elem["id"] == first_elem_test["id"]


def test_make_author_list():
    """
    Function to test if make_author_list function is working properly.
    """

    test_data = load_data()

    test_author_list = []
    for work in test_data["results"]:
        for author in work["authorships"]:
            author_id = author["author"]["orcid"]
            # print(author_id)

            # check to see if author is
            # already added to list to avoid duplicates.
            # check to see if author has an orcid, if not, won't be added.
            if (author_id in test_author_list) is False:
                if author_id is not None:
                    test_author_list.append(author_id)

    author_list = make_author_list([test_data])

    assert author_list == test_author_list


def test_get_h_index():
    """
    Function to check if get_h_index function is working correctly.
    """

    test_author_data = load_author_data()
    test_author_h_index = test_author_data["summary_stats"]["h_index"]

    _, author_h_index = get_h_index("https://orcid.org/0000-0003-3875-4441")

    assert test_author_h_index == author_h_index


def test_sort_authors():
    """
    Function to test if sort_authors is working properly.
    """

    test_unsorted = {"a": 50, "b": 72, "c": 1, "d": 55}
    test_sorted = {"c": 1, "a": 50, "d": 55, "b": 72}

    sort_authors_dict = sort_authors(test_unsorted)

    assert sort_authors_dict == test_sorted


def test_too_many_keywords():
    """
    This function that get_works correctly raises system exit error
    if more than three keywords are passed.
    """
    with pytest.raises(SystemExit):
        keywords = ("This", "is", "a", "test.")
        get_works(keywords=keywords)

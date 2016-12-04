import string

# TODO: Expand blacklist to clear out other garbage tokens
token_blacklist = ['urlLink', '']


# Return post's token list, removing punctuation and whitespace, but preserving contraction apostrophes
def get_token_list(post):
    # TODO: Plenty of additional string processing to get better tokens
    # TODO: Stemming (if desired), etc.
    return [x.strip(string.punctuation).lower() for x in post.split() if x not in token_blacklist]


if __name__ == "__main__":
    from file_handler import filename_iterator
    from xml_handler import get_posts_from_xml_file

    # f = filename_iterator('./../blogs')
    # p = get_posts_from_xml_file(f.next())

    count = 0
    for f in filename_iterator('./../blogs', group=""):
        # print f
        for p in get_posts_from_xml_file(f):
            count += 1

    print count

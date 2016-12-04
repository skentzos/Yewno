import math

from file_handler import filename_iterator
from xml_handler import get_posts_from_xml_file
from string_handler import get_token_list


class similar_word_finder(object):
    def __init__(self, path, group):
        self.total_posts = 0.0
        self.posts_with_word = {}
        self.posts_with_both_words = {}

        for filename in filename_iterator(path, group=group):
            for post in get_posts_from_xml_file(filename):
                self.total_posts += 1.0                                     # Track total number of posts seen

                tokens = list(set(get_token_list(post)))                    # Remove duplicate tokens within same post

                for index in range(len(tokens)):
                    token = tokens.pop(index)                               # Iterate over tokens
                    self.posts_with_word[token] = self.posts_with_word.get(token, 0.0) + 1.0
                    self.posts_with_both_words.setdefault(token, {})

                    for other_token in tokens:
                        self.posts_with_both_words[token][other_token] = \
                            self.posts_with_both_words[token].get(other_token, 0.0) + 1.0

                    tokens.insert(index, token)

    def get_similarity_score(self, x, y):

        # x, y case
        pxy = self.posts_with_both_words[x].get(y, 0.0) / self.total_posts
        px = self.posts_with_word[x] / self.total_posts
        py = self.posts_with_word[y] / self.total_posts
        pp = self.calculate_score(pxy, px, py)

        # x, not y case
        pxy = (self.posts_with_word[x] - self.posts_with_both_words[x].get(y, 0.0)) / self.total_posts
        px = self.posts_with_word[x] / self.total_posts
        py = (self.total_posts - self.posts_with_word[y]) / self.total_posts
        pn = self.calculate_score(pxy, px, py)

        # not x, y case
        pxy = (self.posts_with_word[y] - self.posts_with_both_words[y].get(x, 0.0)) / self.total_posts
        px = (self.total_posts - self.posts_with_word[x]) / self.total_posts
        py = self.posts_with_word[y] / self.total_posts
        np = self.calculate_score(pxy, px, py)

        # not x, not y case
        pxy = (self.total_posts -
               self.posts_with_word[x] -
               self.posts_with_word[y] +
               self.posts_with_both_words[x].get(y, 0.0)) / self.total_posts
        px = (self.total_posts - self.posts_with_word[x]) / self.total_posts
        py = (self.total_posts - self.posts_with_word[y]) / self.total_posts
        nn = self.calculate_score(pxy, px, py)

        print pp
        print pn
        print np
        print nn

        return pp + pn + np + nn

    @staticmethod
    def calculate_score(pxy, px, py):
        return pxy*math.log(pxy/(px*py))

if __name__ == "__main__":
    from pprint import pprint

    swf = similar_word_finder(path="./../blogs", group='30s')

    pprint(swf.total_posts)
    pprint(swf.posts_with_word['winnipeg'])
    pprint(swf.posts_with_word['with'])
    pprint(swf.posts_with_both_words['winnipeg']['with'])

    pprint(swf.get_similarity_score('winnipeg', 'with'))
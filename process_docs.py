import math

from file_handler import filename_iterator
from xml_handler import get_posts_from_xml_file
from string_handler import get_token_list


class SimilarWordFinder(object):
    def __init__(self, path, group):
        self.total_posts = 0                                                # Post counter is also postID.
        self.posts_with_word = {}

        fi = filename_iterator(path, group=group)

        # for filename in [fi.next(), fi.next(), fi.next(), fi.next()]:      # Grab a few files for debugging
        for filename in fi:                                                 # Iterate over files
            for post in get_posts_from_xml_file(filename):
                self.total_posts += 1                                       # Track total number of posts seen.

                tokens = list(set(get_token_list(post)))                    # Remove duplicate tokens within same post.

                for token in tokens:                                        # Iterate over tokens.
                    self.posts_with_word.setdefault(token, set())
                    self.posts_with_word[token].add(self.total_posts)       # Add postID to set of posts with token.

        self.total_posts = float(self.total_posts)                          # For later non-integer division

        self.counts = {}
        for key in self.posts_with_word:
            self.counts[key] = len(self.posts_with_word[key])               # Precompute number of posts with token

    def get_similarity_score(self, x, y):

        # x, y case
        pxy = len(self.posts_with_word[x] & self.posts_with_word[y]) / self.total_posts
        px = self.counts[x] / self.total_posts
        py = self.counts[y] / self.total_posts
        pp = self.calculate_score(pxy, px, py) if pxy * px * py > 0 else 0

        # x, not y case
        pxy = len(self.posts_with_word[x] - self.posts_with_word[y]) / self.total_posts
        px = self.counts[x] / self.total_posts
        py = (self.total_posts - self.counts[y]) / self.total_posts
        pn = self.calculate_score(pxy, px, py) if pxy * px * py > 0 else 0

        # not x, y case
        pxy = len(self.posts_with_word[y] - self.posts_with_word[x]) / self.total_posts
        px = (self.total_posts - self.counts[x]) / self.total_posts
        py = self.counts[y] / self.total_posts
        np = self.calculate_score(pxy, px, py) if pxy * px * py > 0 else 0

        # not x, not y case
        pxy = (self.total_posts -
               self.counts[x] -
               self.counts[y] +
               len(self.posts_with_word[x] & self.posts_with_word[y])) / self.total_posts
        px = (self.total_posts - self.counts[x]) / self.total_posts
        py = (self.total_posts - self.counts[y]) / self.total_posts
        nn = self.calculate_score(pxy, px, py) if pxy * px * py > 0 else 0

        return pp + pn + np + nn

    @staticmethod
    def calculate_score(pxy, px, py):
        return pxy * math.log(pxy / (px * py))

    def get_most_similar_words(self, probe, num_words):
        similarity_scores = {}
        for key in self.posts_with_word:
            if key != probe:
                similarity_scores[key] = self.get_similarity_score(probe, key)

        return sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[0:num_words]


if __name__ == "__main__":
    from pprint import pprint
    from time import time

    print "30s blogs"
    timestamp = time()
    swf = SimilarWordFinder(path="./../blogs", group='30s')
    pprint(swf.get_most_similar_words('winnipeg', 5))
    print "Time: ", time() - timestamp

    print "20s blogs"
    timestamp = time()
    swf = SimilarWordFinder(path="./../blogs", group='20s')
    pprint(swf.get_most_similar_words('winnipeg', 5))
    print "Time: ", time() - timestamp

    print "10s blogs"
    timestamp = time()
    swf = SimilarWordFinder(path="./../blogs", group='10s')
    pprint(swf.get_most_similar_words('winnipeg', 5))
    print "Time: ", time() - timestamp

    print "All blogs"
    timestamp = time()
    swf = SimilarWordFinder(path="./../blogs", group='all')
    pprint(swf.get_most_similar_words('winnipeg', 5))
    print "Time: ", time() - timestamp

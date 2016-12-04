import os


# Instantiate a generator over the filenames in path... that meet the group criterion
def filename_iterator(path, group="all"):
    min_age = 0
    max_age = 100

    if group == "10s":
        min_age = 10
        max_age = 20

    if group == "20s":
        min_age = 20
        max_age = 30

    if group == "30s":
        min_age = 30
        max_age = 50

    for fname in [fname for fname in os.listdir(path) if min_age < int(fname.split(".")[2]) < max_age]:
        yield os.path.join(path, fname)

if __name__ == '__main__':
    fi = filename_iterator('./../blogs/', group="")
    print fi.next()
    print len(list(fi))

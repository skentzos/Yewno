from lxml import etree


def get_posts_from_xml_file(fname):
    file_handle = open(name=fname, mode='r')
    string = file_handle.read()                                 # Ingest file text as string
    unicode_string = unicode(string, errors="ignore")           # Convert to unicode

    parser = etree.XMLParser(encoding='utf-8', recover=True)

    tree = etree.fromstring(unicode_string, parser)             # Use resilient parser to parse unicode

    for post in tree.findall('post'):
        yield post.text


if __name__ == '__main__':
    from file_handler import filename_iterator

    fi = filename_iterator('./../blogs/', group="")
    pi = get_posts_from_xml_file(fi.next())

    print pi.next()
    print len(list(pi))
# Yewno

Caveats:

Mostly pep8-compliant, but I don't think it matters much.

File handler has hard-coded cutoffs, base on corpus definition. Wouldn't work on any corpus.

XML handler could be better with weird encoding issues for parsing. I figured a few errors was fine.

String handler could be a lot more sophisticated. TODOs were left in to describe some ways to improve.

In a production environment, I'd save the processed corpus stats in process_docs to avoid recomputing each time.
Also, the task of determining the posts in which a term occurs would be parallelized and reduced,
 since the term search is completely parallelizable. As is calculation of similarity scores.
Also, I'd add in tests and whatever else is part of the code architecture.



The test script processes the documents first by age group and then once for overall.
I used 'winnipeg' as the word probe and asked for the 5 most-similar words.

Output:

Steves-MBP:Yewno steveskentzos$ python process_docs.py
30s blogs
[('oliver', 0.00027145740462621596),
 ('manitoba', 0.0001955605753253042),
 ('canadian', 0.00016485678557945322),
 ('inter-country', 0.0001323847969231966),
 ('canada-ophile', 0.0001323847969231966)]
Time:  53.0784549713
20s blogs
[('manitoba', 0.0003803245198176938),
 ('canada', 0.0001727726190716684),
 ('toronto', 0.00015317302855550452),
 ('saskatoon', 0.0001127949146408492),
 ('regina', 0.0001103439626238524)]
Time:  158.141891956
10s blogs
[('manitoba', 0.00011101956085779731),
 ('sinful_misery', 8.971413948233797e-05),
 ('vancouver', 8.342602565657417e-05),
 ('from', 8.304091067223176e-05),
 ('canada', 7.9793669892996e-05)]
Time:  127.032253027
All blogs
[('manitoba', 0.0002572340285539801),
 ('canada', 0.00012585331540310992),
 ('toronto', 9.324037809157771e-05),
 ('ontario', 7.683919044317009e-05),
 ('vancouver', 7.494338337162167e-05)]
Time:  302.42445612

Timing ends up being on the order of 50 blogs per second.
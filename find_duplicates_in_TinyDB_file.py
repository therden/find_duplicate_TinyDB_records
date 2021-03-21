# This program finds duplicate records in a TinyDB database.
#
from collections import Counter
from tinydb import TinyDB, Query

source_file = "sample_file_containing_dupes.json"

db = TinyDB(source_file)

repr_list = []
for each in db.all():
    repr_list.append(each.__repr__())
instance_counter = Counter(repr_list)
dupes = [eval(k) for k, c in instance_counter.items() if c > 1]
del repr_list, instance_counter

if not dupes:
    print(f"\nNo duplicate entries found in file '{source_file}'.\n")

results = []
for dupe in dupes:
    doc_ids = []
    matches = db.search(Query().fragment(dupe))
    for match in matches:
        doc_ids.append(match.doc_id)
    results.append((dupe, doc_ids))

print("\n")
for each in results:
    print(f"Record:  {each[0]}")
    print(f"doc_ids: {each[1]}\n")

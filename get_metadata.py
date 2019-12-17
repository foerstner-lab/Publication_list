import urllib.request
import json

base_url = "https://api.crossref.org/works/"

for line in open("Publications.tsv"):
    if line.startswith("DOI"):
        continue
    doi = line.split()[0]
    full_url = base_url + doi
    try:
        doi_json_data = urllib.request.urlopen(full_url).read()
        doi_data = json.loads(doi_json_data)
        journal_title = doi_data["message"]["container-title"][0]
        title = doi_data["message"]["title"][0]
    except urllib.error.HTTPError:
        journal_title = "-"
        title = "-"
    print(f"{doi}\t{journal_title}\t{title}")

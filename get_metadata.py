import urllib.request
import json


def main():
    base_url = "https://api.crossref.org/works/"
    print_html = True
    if print_html:
        print("<table>\n"
              "<tr>\n"
              "<th></th>\n"
              "<th>#</th>\n"
              "<th>Publication Year</th>\n"
              "<th>Title</th>\n"
              "<td>Authors</td>\n"
              "<td>Journal</td> \n"
              "<td>Link</td>\n"
              "</tr>\n"
        )
    counter = 1
    for line in open("Publications.tsv"):
        if line.startswith("DOI") or line.startswith("-") or line.startswith("10.18420/inf2019_26"):
            continue
        counter = process_line(line, base_url, print_html, counter)
        
    if print_html:
        print("</table>")


def process_line(line, base_url, print_html, counter):
    split_line = line.split()
    doi = split_line[0]
    pmid = line.split()[1]
    wikidata_id = line.split()[2]
    pmcid = line.split()[3]
    full_url = base_url + doi
    doi_data = get_doi_data(doi)

    try:
        journal_title = doi_data["message"]["container-title"][0]
        title = doi_data["message"]["title"][0]
        authors = generate_author_string(doi_data)
    except KeyError:
        journal_title = "-"
        title = "-"
        authors = "-"
    try:
        publication_year = doi_data[
            "message"]["published-online"]["date-parts"][0][0]
    except KeyError:
        publication_year = doi_data[
            "message"]["published-print"]["date-parts"][0][0]
    except TypeError:
        publication_year = "-"
        authors = "-"
        return
    if print_html:
        print(f"<tr>\n"
              f"  <td><div class='altmetricdonotimage'><div class='altmetric-embed' data-badge-popover='bottom' data-badge-type='donut' data-doi='{doi}'></div></td>\n"
              f"  <td>{counter}</td>\n"              
              f"  <td>{publication_year}</td>\n"
              f"  <td>{title}</td>\n"
              f"  <td>{authors}</td>\n"              
              f"  <td><i>{journal_title}</i></td>\n"
              f"  <td><a title='DOI - got to full text' href=\"https://doi.org/{doi}\">{doi}</br></a>\n"
              f"      <a title='Metadata at PubMed' href=\"https://pubmed.ncbi.nlm.nih.gov/25146723\"/>25146723</a></br>\n"
              f"      <a title='Fulltext at PubMedCentral' href=\"http://www.ncbi.nlm.nih.gov/pmc/articles/pmc6435200/\"/>PMC6435200</a></br>\n"
              f"      <a title='Wikidata' href=\"https://www.wikidata.org/wiki/Q22951230\"/>Q13132</a></td>\n"
              f"  </tr>\n")
    else:
        print(f"{doi}\t{publication_year}\t{journal_title}\t{title}")
    counter += 1
    return counter


def get_doi_data(doi):
    base_url = "https://api.crossref.org/works/"
    full_url = base_url + doi
    json_file = f"metadata_json/{doi.replace('/', '_')}.json"

    doi_json_data = open(json_file).read()
    
    # Try to look for local file
    try:
        doi_json_data = open(json_file).read()
    except IOError:
        # Otherwise download and save data
        try:
            doi_json_data = urllib.request.urlopen(full_url).read()
            with open(json_file, "w") as json_fh:
                json_fh.write(doi_json_data.decode("utf-8"))
        except urllib.error.HTTPError:
            print("HTTP error: ", doi)
            return
    doi_data = json.loads(doi_json_data)
    return doi_data

    
def generate_author_string(doi_data):
    authors = [f"{author['given']} {author['family']}"
               for author in doi_data["message"]["author"]]
    return(", ".join(authors))


main()

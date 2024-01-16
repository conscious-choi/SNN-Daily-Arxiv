from paperswithcode import PapersWithCodeClient
import time

def json_creator(results):

    for result in results:
        pass


if __name__ == "__main__":

    client = PapersWithCodeClient()

    keywords = input("Enter keyword: ")

    start = time.time()

    print(f"Searching {keywords}...")

    papers = client.paper_list(keywords, items_per_page=10000)

    end = time.time()

    print("Find {} results. Took {:.3f} sec".format(papers.count, end - start))

    import pdb; pdb.set_trace();
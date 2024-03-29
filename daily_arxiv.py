import datetime
import requests
import json
import arxiv
import os
from repo_search import proceeder

base_url = "https://arxiv.paperswithcode.com/api/v0/papers/"

def get_authors(authors, first_author = False):
    output = str()
    if first_author == False:
        output = ", ".join(str(author) for author in authors)
    else:
        output = authors[0]
    return output

# key has year information. e.g) '2209.00413' '2312.14954'
def sort_papers(papers):
    output = dict()
    keys = list(papers.keys())
    keys.sort(reverse=True)
    for key in keys:
        output[key] = papers[key]
    return output

def conference_name_changer(input):
    conference = input.split("-")[0]
    year = input.split("-")[1][-2:]

    if conference == "neurips":
        conference = "NeurIPS"
    else:
        conference = conference.upper()
        
    conference = conference + " " + year
    return conference

def get_daily_papers(topic,query="SNN", max_results=2):
    """
    @param topic: str
    @param query: str
    @return paper_with_code: dict
    """

    # output 
    content = dict() 

    # content
    output = dict()

    client = arxiv.Client()
    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)

    cnt = 0

    # for result in search_engine.results():
    for result in results:

        paper_id            = result.get_short_id()
        paper_title         = result.title
        paper_url           = result.entry_id
        code_url            = base_url + paper_id
        paper_abstract      = result.summary.replace("\n"," ")
        paper_authors       = get_authors(result.authors)
        paper_first_author  = get_authors(result.authors,first_author = True)
        primary_category    = result.primary_category
        publish_time        = result.published.date()
        update_time         = result.updated.date()
        comments            = result.comment

        proceeding = proceeder(paper_title)

      
        print("Time = ", update_time ,
              " title = ", paper_title,
              " author = ", paper_first_author)

        # eg: 2108.09112v1 -> 2108.09112
        ver_pos = paper_id.find('v')
        if ver_pos == -1:
            paper_key = paper_id
        else:
            paper_key = paper_id[0:ver_pos]    

        try:
            r = requests.get(code_url).json()

            """
            Edited by S.Choi - We don't need content_to_web (not used) + Comments
            """
            if "official" in r and r["official"]:
                cnt += 1
                repo_url = r["official"]["url"]

                if proceeding != None:
                    proceeding = conference_name_changer(proceeding)
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|**[link]({repo_url})**|**{proceeding}**|\n"
                else:
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|**[link]({repo_url})**|null|\n"
            else:
                if proceeding != None:
                    proceeding = conference_name_changer(proceeding)
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|null|**{proceeding}**|\n"
                else:
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|null|null|\n"

        except Exception as e:
            print(f"exception: {e} with id: {paper_key}")

    data = {topic:content}
    return data

def update_json_file(filename,data_all):
    with open(filename,"r") as f:
        content = f.read()
        if not content:
            m = {}
        else:
            m = json.loads(content)
            
    json_data = m.copy() 
    
    # update papers in each keywords         
    for data in data_all:
        for keyword in data.keys():
            papers = data[keyword]

            if keyword in json_data.keys():
                json_data[keyword].update(papers)
            else:
                json_data[keyword] = papers

    with open(filename,"w") as f:
        json.dump(json_data,f)
    
def json_to_md(filename,md_filename,
               to_web = False, 
               use_title = True, 
               use_tc = True,
               show_badge = False):
    """
    @param filename: str
    @param md_filename: str
    @return None
    """
    
    DateNow = datetime.date.today()
    DateNow = str(DateNow)
    DateNow = DateNow.replace('-','.')
    
    with open(filename,"r") as f:
        content = f.read()
        if not content:
            data = {}
        else:
            data = json.loads(content)

    # clean README.md if daily already exist else create it
    with open(md_filename,"w+") as f:
        pass

    # write data into README.md
    with open(md_filename,"a+") as f:
                
        if use_title == True:
            f.write("## Updated on " + DateNow + "\n\n")
        else:
            f.write("> Updated on " + DateNow + "\n\n")
        
        
        for keyword in data.keys():
            full_lists = data[keyword]
            if not full_lists:
                continue
            # the head of each part
            f.write(f"## {keyword}\n\n")

            # sort papers by date
            full_lists = sort_papers(full_lists)

            proceedings_dict = {
                "NeurIPS": {},
                "ECCV": {},
                "CVPR": {},
                "ICCV": {},
                "ICLR": {},
                "AAAI": {},
                "ICML": {},
                "PMLR": {},
                "IJCAI": {}
            }
        
            for k, v in full_lists.items():

                proceedings = v.split("|")[-2]

                if proceedings != "null":
                    for key, dict in proceedings_dict.items():
                            if key in proceedings:
                                    dict[k] = v
                                    break
                    
            # go to the first line?

            for key, conferences in proceedings_dict.items():
                
                f.write(f"### {key}\n")
                    
                f.write("|Publish Date|Title|Authors|PDF|Code|Conference\n" + "|---|---|---|---|---|---|\n")
                for k, v in sort_papers(conferences).items():
                    f.write(v)

            f.write(f"\n")
            
            f.write(f"### Full Papers\n")
            f.write("|Publish Date|Title|Authors|PDF|Code|Conference\n" + "|---|---|---|---|---|---|\n")

            for _,v in full_lists.items():
                if v is not None:
                    f.write(v)

            
            #Add: back to top
            top_info = f"#Updated on {DateNow}"
            top_info = top_info.replace(' ','-').replace('.','')
            f.write(f"<p align=right>(<a href={top_info}>back to top</a>)</p>\n\n")
                
    print("finished")        

 

if __name__ == "__main__":

    data_collector = []
    
    keywords = dict()
    keywords["Spiking Neural Network"] = "\"Spiking Neural Network\"OR\"Spiking Neural Networks\""

    for topic,keyword in keywords.items():
 
        # topic = keyword.replace("\"","")
        print("Keyword: " + topic)

        data = get_daily_papers(topic, query = keyword, max_results = 2000)
        data_collector.append(data)

        print("\n")

    # 1. update README.md file
    json_file = "snn-arxiv-daily.json"
    md_file   = "README.md"
    # update json data
    update_json_file(json_file,data_collector)
    # json data to markdown
    json_to_md(json_file,md_file)
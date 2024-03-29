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

def sort_papers(papers):
    output = dict()
    keys = list(papers.keys())
    keys.sort(reverse=True)
    for key in keys:
        output[key] = papers[key]
    return output    

def get_daily_papers(topic,query="SNN", max_results=2):
    """
    @param topic: str
    @param query: str
    @return paper_with_code: dict
    """

    # output 
    content = dict() 
    content_to_web = dict()

    # content
    output = dict()

    # Edited by S.Choi
    # https://lukasschwab.me/arxiv.py/arxiv.html
    
    # search_engine = arxiv.Search(
    #     query = query,
    #     max_results = max_results,
    #     sort_by = arxiv.SortCriterion.SubmittedDate
    # )
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

        ## add by s.choi
        proceeding = proceeder(paper_title)
        
        # import pdb; pdb.set_trace();
        """
        (Pdb) result.__dict__.keys()
        dict_keys(['entry_id', 'updated', 'published', 'title', 'authors', 'summary', 'comment', 'journal_ref', 'doi', 'primary_category', 'categories', 'links', 'pdf_url', '_raw'])
        (Pdb) result
        arxiv.Result(entry_id='http://arxiv.org/abs/2401.06563v1', updated=datetime.datetime(2024, 1, 12, 13, 20, 1, tzinfo=datetime.timezone.utc), published=datetime.datetime(2024, 1, 12, 13, 20, 1, tzinfo=datetime.timezone.utc), title='Resource-Efficient Gesture Recognition using Low-Resolution Thermal Camera via Spiking Neural Networks and Sparse Segmentation', authors=[arxiv.Result.Author('Ali Safa'), arxiv.Result.Author('Wout Mommen'), arxiv.Result.Author('Lars Keuninckx')], summary='This work proposes a novel approach for hand gesture recognition using an\ninexpensive, low-resolution (24 x 32) thermal sensor processed by a Spiking\nNeural Network (SNN) followed by Sparse Segmentation and feature-based gesture\nclassification via Robust Principal Component Analysis (R-PCA). Compared to the\nuse of standard RGB cameras, the proposed system is insensitive to lighting\nvariations while being significantly less expensive compared to high-frequency\nradars, time-of-flight cameras and high-resolution thermal sensors previously\nused in literature. Crucially, this paper shows that the innovative use of the\nrecently proposed Monostable Multivibrator (MMV) neural networks as a new class\nof SNN achieves more than one order of magnitude smaller memory and compute\ncomplexity compared to deep learning approaches, while reaching a top gesture\nrecognition accuracy of 93.9% using a 5-class thermal camera dataset acquired\nin a car cabin, within an automotive context. Our dataset is released for\nhelping future research.', comment=None, journal_ref=None, doi=None, primary_category='cs.CV', categories=['cs.CV', 'cs.HC'], links=[arxiv.Result.Link('http://arxiv.org/abs/2401.06563v1', title=None, rel='alternate', content_type=None), arxiv.Result.Link('http://arxiv.org/pdf/2401.06563v1', title='pdf', rel='related', content_type=None)])
        (Pdb) result.entry_id
        'http://arxiv.org/abs/2401.06563v1'
        """


      
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
            # source code link
            # if "official" in r and r["official"]:
            #     cnt += 1
            #     repo_url = r["official"]["url"]
            #     content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|**[link]({repo_url})**|\n"
            #     content_to_web[paper_key] = f"- {update_time}, **{paper_title}**, {paper_first_author} et.al., Paper: [{paper_url}]({paper_url}), Code: **[{repo_url}]({repo_url})**"

            # else:
            #     content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|null|\n"
            #     content_to_web[paper_key] = f"- {update_time}, **{paper_title}**, {paper_first_author} et.al., Paper: [{paper_url}]({paper_url})"

            """
            Edited by S.Choi - We don't need content_to_web (not used) + Comments
            """
            if "official" in r and r["official"]:
                cnt += 1
                repo_url = r["official"]["url"]

                if proceeding != None:
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|**[link]({repo_url})**|**{proceeding}\n"
                    # content_to_web[paper_key] = f"- {update_time}, **{paper_title}**, {paper_first_author} et.al., Paper: [{paper_url}]({paper_url}), Code: **[{repo_url}]({repo_url})**"
                else:
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|**[link]({repo_url})**|\n"
                    # content_to_web[paper_key] = f"- {update_time}, **{paper_title}**, {paper_first_author} et.al., Paper: [{paper_url}]({paper_url}), Code: **[{repo_url}]({repo_url})**"
            else:
                if proceeding != None:
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|null|**{proceeding}**\n"
                else:
                    content[paper_key] = f"|**{update_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|null|\n"
                # content_to_web[paper_key] = f"- {update_time}, **{paper_title}**, {paper_first_author} et.al., Paper: [{paper_url}]({paper_url})"

            # # TODO: select useful comments
            # comments = None
            # if comments != None:
            #     content_to_web[paper_key] = content_to_web[paper_key] + f", {comments}\n"
            # else:
            #     content_to_web[paper_key] = content_to_web[paper_key] + f"\n"

        except Exception as e:
            print(f"exception: {e} with id: {paper_key}")

    data = {topic:content}
    data_web = {topic:content_to_web}
    return data,data_web 

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

        ################ we don't have to care about this #################
        if (use_title == True) and (to_web == True):
            f.write("---\n" + "layout: default\n" + "---\n\n")
        
        if show_badge == True:
            f.write(f"[![Contributors][contributors-shield]][contributors-url]\n")
            f.write(f"[![Forks][forks-shield]][forks-url]\n")
            f.write(f"[![Stargazers][stars-shield]][stars-url]\n")
            f.write(f"[![Issues][issues-shield]][issues-url]\n\n")    
        ################ we don't have to care about this #################
                
        if use_title == True:
            f.write("## Updated on " + DateNow + "\n\n")
        else:
            f.write("> Updated on " + DateNow + "\n\n")
        
        #Add: table of contents
        if use_tc == True:
            f.write("<details>\n")
            f.write("  <summary>Table of Contents</summary>\n")
            f.write("  <ol>\n")
            for keyword in data.keys():
                day_content = data[keyword]
                if not day_content:
                    continue
                kw = keyword.replace(' ','-')      
                f.write(f"    <li><a href=#{kw}>{keyword}</a></li>\n")
            f.write("  </ol>\n")
            f.write("</details>\n\n")
        
        for keyword in data.keys():
            day_content = data[keyword]
            if not day_content:
                continue
            # the head of each part
            f.write(f"## {keyword}\n\n")

            if use_title == True :
                if to_web == False: # default false
                    # f.write("|Publish Date|Title|Authors|PDF|Code|\n" + "|---|---|---|---|---|\n")
                    """
                    Edited By S.Choi
                    """
                    f.write("|Publish Date|Title|Authors|PDF|Code|Conference\n" + "|---|---|---|---|---|---|\n")
                else:
                    f.write("| Publish Date | Title | Authors | PDF | Code |\n")
                    f.write("|:---------|:-----------------------|:---------|:------|:------|\n")

            # sort papers by date
            day_content = sort_papers(day_content)

            """
            Edited by S.Choi
            """
            nips = []
        
            for _,v in day_content.items():
                if v is not None:
                    f.write(v)
                """
                Edited by S.Choi
                """
                if "neurips" in v:
                    nips.append(v)

            if use_title == True :
                if to_web == False: # default false
                    # f.write("|Publish Date|Title|Authors|PDF|Code|\n" + "|---|---|---|---|---|\n")
                    """
                    Edited By S.Choi
                    """
                    f.write("### NeurIPS\n")
                    f.write("|Publish Date|Title|Authors|PDF|Code|Conference\n" + "|---|---|---|---|---|---|\n")
                else:
                    f.write("| Publish Date | Title | Authors | PDF | Code |\n")
                    f.write("|:---------|:-----------------------|:---------|:------|:------|\n")

            for v in nips:
                if v is not None:
                    f.write(v)

            f.write(f"\n")
            
            #Add: back to top
            top_info = f"#Updated on {DateNow}"
            top_info = top_info.replace(' ','-').replace('.','')
            f.write(f"<p align=right>(<a href={top_info}>back to top</a>)</p>\n\n")
        
        if show_badge == True:
            f.write(f"[contributors-shield]: https://img.shields.io/github/contributors/SpikingChen/snn-arxiv-daily.svg?style=for-the-badge\n")
            f.write(f"[contributors-url]: https://github.com/SpikingChen/snn-arxiv-daily/graphs/contributors\n")
            f.write(f"[forks-shield]: https://img.shields.io/github/forks/SpikingChen/snn-arxiv-daily.svg?style=for-the-badge\n")
            f.write(f"[forks-url]: https://github.com/SpikingChen/snn-arxiv-daily/network/members\n")
            f.write(f"[stars-shield]: https://img.shields.io/github/stars/SpikingChen/snn-arxiv-daily.svg?style=for-the-badge\n")
            f.write(f"[stars-url]: https://github.com/SpikingChen/snn-arxiv-daily/stargazers\n")
            f.write(f"[issues-shield]: https://img.shields.io/github/issues/SpikingChen/snn-arxiv-daily.svg?style=for-the-badge\n")
            f.write(f"[issues-url]: https://github.com/SpikingChen/snn-arxiv-daily/issues\n\n")
                
    print("finished")        

 

if __name__ == "__main__":

    data_collector = []
    data_collector_web= []
    
    keywords = dict()
    keywords["Spiking Neural Network"]                 = "\"Spiking Neural Network\"OR\"Spiking Neural Networks\""

    for topic,keyword in keywords.items():
 
        # topic = keyword.replace("\"","")
        print("Keyword: " + topic)

        data,data_web = get_daily_papers(topic, query = keyword, max_results = 10)
        data_collector.append(data)
        data_collector_web.append(data_web)

        print("\n")

    # 1. update README.md file
    json_file = "snn-arxiv-daily.json"
    md_file   = "README.md"
    # update json data
    update_json_file(json_file,data_collector)
    # json data to markdown
    json_to_md(json_file,md_file, to_web=True)

    # later do it with data_web?
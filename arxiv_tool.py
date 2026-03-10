import requests


def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            print(f"Invalid character '{char}' in query: {query}")
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")
    url = (
            "https://export.arxiv.org/api/query"     #arXiv’s public API endpoint
            f"?search_query=all:{query}"              #All the limits to filter out the papers
            f"&max_results={max_results}"
            "&sorBy=submittedDate"
            "&sortOrder=descending"
        )
    
    print(f"Making request to archive API: {url}")
    resp = requests.get(url)
    if not resp.ok:
        print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
        raise ValueError(f"Bad response from ArXiv API: {resp}\n{resp.text}")
    # print("Status Code:",resp.status_code)
    # print("Status Text:",resp.text)
    
    data = parse_arxiv_xml(resp.text)
    return data

import xml.etree.ElementTree as ET  
def parse_arxiv_xml(xml_content: str) -> dict:
    """Parse the XML content from arXiv API response"""
    
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_content)
    #Loop through each <entry> in each namespace
    for entry in root.findall("atom:entry", ns):
        #Extract authors
        authors = [
            authors.findtext("atom:name", namespaces=ns)
            for authors in entry.findall("atom:author", ns)
        ]
    
        # Extract categories (term attribute)
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category", ns)
        ]
        
        # Extract PDF link (rel="related" and type="application/pdf")
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break

        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "authors": authors,
            "categories": categories,
            "pdf": pdf_link
        })

    return {"entries": entries}

# print(search_arxiv_papers(topic="Prompt Engineering", max_results = 5))


#Step3: Convert the funtionality into a tool
from langchain_core.tools import tool
@tool
def arxiv_search(topic: str) -> list[dict]:
    """Search from recently uploaded arXiv papers
    
    Args:
        topic: The topic to search for papers about 
        
    Return: 
        List of papers with their metadata including title, authors, summary. etc.  
    """
    print("ArXiv Agent Called")
    print(f"Searching arXiv for papers about: {topic}")
    papers=search_arxiv_papers(topic)
    if len(papers) == 0:
        print(f"No papers found for topic: {topic}")
        raise ValueError(f"No papers found for topic: {topic}")
    print(f"Found {len(papers['entries'])} papers about {topic}")
    return papers
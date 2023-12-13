from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType
from pydantic import BaseModel
import requests
import json
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain.schema import SystemMessage
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")

query = "Trending headlines on innovation, growth, challenges, opportunities in banking, technology, fintech, healthcare, economy"
def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.text

system_message = SystemMessage(
        content="""You are a news agent who acquires only relevant urls of current trending headlines belonging only to Healthcare, Technology 
                   and Finance sectors that will be useful for market analysis.

                Please make sure you complete the objective above with the following rules:
                1/ You should do enough research to gather as much information as possible about the objective
                2/ You should filter the urls which belong only to current trends in healthcare, technology and finance sectors
                3/ The urls should have html image tags with heading so that the image and with heading can be displayed in the front end using the url"""
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")
tools = [
    Tool(
        name="Search",
        func=search,
        description="useful when you need to answer questions about current events, data. You should ask targeted questions"
    ),
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=False,
)


class Query(BaseModel):
    query: str


def get_trending_headlines():
    content = agent({"input": query})
    actual_content = content['output']
    print("Actual Content is:", actual_content)
    # Extracting titles, URLs, and image URLs using regular expressions and BeautifulSoup
    pattern = r'"([^"]+)"|\[([^]\n]*)(?<!Read more)\]\((https?[^)]+)\)'
    matches = re.findall(pattern, actual_content)

    # Creating a list of dictionaries with titles, URLs, and image URLs
    data = []
    for match in matches:
        title = match[0] if match[0] else match[1]
        url = match[2]
        image_url = get_image_url(url)
        data.append({"title": title, "url": url, "image_url": image_url})

    # Converting the list to JSON
    json_data = json.dumps(data, indent=2)

    return json_data


def get_image_url(url):
    # Make a request to the webpage
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first image tag and extract its source (URL)
    img_tag = soup.find('img')

    if img_tag:
        # Check if src attribute is present before accessing it
        if 'src' in img_tag.attrs:
            image_url = img_tag['src']

            # Make the image URL absolute if it's relative
            if not image_url.startswith('http'):
                image_url = urljoin(url, image_url)

            return image_url

    # If no image tag or src attribute is found, return None
    return None


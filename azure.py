import streamlit_analytics
from open_ai_service import OpenAIService
import streamlit as st
from pptx import Presentation
from io import BytesIO
from pptx.util import Inches, Pt
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
import docx
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests as r
import pinecone
import langchain
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAIChat
from langchain import PromptTemplate
from embedchain import App
# from google.oauth2 import service_account
# import json
import os
import spacy
import nlp
import pandas as pd

from spacy.lang.en import English

pd.set_option("max_colwidth", 300)
nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler")
patterns = [{"label": "ORG", "pattern": "Eightfold"},{"label": "ORG", "pattern": "SAP Successfactors"},{"label": "ORG", "pattern": "SAP"},
            {"label": "GPE", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]}]
ruler.add_patterns(patterns)


# #from gsheetsdb import connect
# google_json = {
#   "type": "service_account",
#   "project_id": "chatty-394114",
#   "private_key_id": "1c92a38dd9adbea24a4379feda95abb80a3034ff",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDCzuL50Fu2TCF8\nl4rCOvb6NDsXUWN0jUR2ti9gThzL38K+IMVnfOfIBHtxlWNcbc0Z8Ui14NhLU2gr\nJZEDYltiXL7HiCHhE7JkGvk5MWXKiNSivinbngEjLO6bjvzJ2Pmt9wfz0o1eV5b7\nrrnFo45t3LRiHF86bk7eZUj1vybHG4QRF3wedp/nwzbGO1x0CD38AP1Saks0ELPo\n+Q571nzM7m/E2Hb+Xxp7Pj72xrvKqZhqJyllJFYfIhZY/8oWrKT2ZY+/sx3trULZ\nPpLuaow2jzHA545JzMLPVmVn1sHyzWVfQTa03DDQfg7yK7uszFD7WCjI009tgmJN\nVdjbZYoBAgMBAAECggEAFzvFveXigkKLKIkJqgeOnCGYPebdizGBTafbIku+oHaz\n4FQX5widEMcEEp8D+3/hmxX38Np7lrmVrgusGLC61bzaSKwiNO38nnbJwXn0OhcJ\nRng9QBg/P3rk4ZWd7X7crFRO1P6yuzfhZcFIHlusKXXN56Oa8eTlBXN5Tkx5a1Er\nLa69UR0oaRri/zQ4glZWIwCU5TgmEeX+OXrM7jOoBBDQSLVbVNK13K1oKxWVouf5\nNwYVxzUhggPn0XYCsatacQ37Mo22ddXEruS4nPcOovIZeJk+s9WzhwPzKVSja8in\nPJhlRW2RLnPMAwWs6Vqj2g9ulTftvHAAqLsi9l3SrwKBgQDyjo5zhzIi53vpnYpd\niK0Psj1gWWlZIwvnSdPynabUUHk314hsfr9r+2F74t3CCbNUFWr6Q7G7e7L+Yy5N\n3/IUxgSl9MJYq4tToOq1GcaggiHhiJ6X7Iyf7iGG5yku2C7xvDx6M/MMycjsLg8D\n/22sa6zginESwExEBe+WJWBrIwKBgQDNmty9BkL1guAWzZEC5ZuRYCYairaWbxqk\nKuex9lPU7f64CyxI5bZbVVMCcCIYK5s86aEvoPTl2wHQf5Ta4oPGfvAyn123W9X8\naJjhrazso123BLbhmLMf051rsKabQEKc16XL2pvsPgyehx19RdpzsXR84hYh33qX\nBlUGwHQKiwKBgQDKdK72QwxYEftdnX+WXrSE+3M7bqX+HsCaxwa/5VMQuDLVp3NZ\ni9nfGa3eqBgNE+e48T+fsM0y/icDKmnF2nzHVhkfJFLrjBP5M8F0dBVUeAoro8ss\nZ+dgvnUBkwTO8ucMIuAf6CigrfSlHjSuU4+JcT6VFTkYO6XsyT+XhY8bHQKBgEeB\nya2wJM+QUfF8UyfHxWA9KWNnxPLy9zgLeAOL4UIX99P4htFfmxmOxkz9xM3VNKtt\nsdKHz0S1856ZEKNDzoLVmSJyDLz9oqGjmzA6H/85HhnN+PDjE8FI7uIKUReDtOcp\nlQ8eG8aBGhB0e4wbJEvCdvoMA5iKSe+Gk0HC41jbAoGBAI2DoRGMeIBq1YmW7j43\ng2YiZt/HvC6LzYrzpGHpCCxHlNOmiN4yMKZW/U3RzGbk5CnHuHL4OGgRN+iOF6CS\nrkX0fDwek5iAvYXBspLXJJFak8w6G+3VDefEpFCPeIlo8Aq68HTwqeYTjlGgVo/1\nSzPU2zOSFhbHUgpALiZLObSi\n-----END PRIVATE KEY-----\n",
#   "client_email": "test-727@chatty-394114.iam.gserviceaccount.com",
#   "client_id": "106916054558122231861",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-727%40chatty-394114.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }

sap_options1 = ["", "What are the main features of the 1H 2023 release of the SAP SuccessFactors HXM Suite",
                "How does the SAP SuccessFactors Opportunity Marketplace help employees",
                "How can I get ready for Talent Intelligence Hub?",
                "How does Talent Intelligence Hub interact with other SAP SuccessFactors modules?",
                "What is the SAP SuccessFactors Innovation Strategy?",
                "What are some examples of SAP Solution Extensions",
                "What is Eightfold and how does it integrate with SAP?",
                "What is Beamery and how does it integrate with SAP?",
                "List HR software companies in Middle East and North Africa region listing their strengths in the region",
                "What is the learning plan to be become a Successfactors LMS consultant? What skills do I need?",
                "What are the different types of partnerships that SAP offers? What is a solution extension partner?",
                "How do I change the theme in the Successfactors application? Provide steps for an adminstrator"]
sap_options2 = ["", "You are an HR industry expert. Provide the top HR challenges facing the retail industry",
                "Write a 300-word SEO-friendly blog with right keywords, title, meta-description, h1,h2 details and  5 examples on how the gig economy will change the retail industry.",
                "Write an outline for an ebook with 10 chapters on how the future of hybrid work can be improved by Web3 and Metaverse. Provide detailed titles and sites as references.",
                "Provide a short blog post on job functions that may be displaced by AI in the financial sector with an intro, description and conclusion section"]
sap_options3 = ["",
                "Rewrite this demo script for a Retail customer  \n Introduction: \n HXM, Human Experience Management, is an evolution of HCM. HXM is about creating individualized, dynamic experiences for all users - whether candidates, new hires, employees, managers or HR leaders.Because our people determine whether an organization succeeds or fails, the experiences we deliver and how we address the moments that matter for every individual impact everything from top line business growth to profitability to how quickly an organization can adapt to change.With HXM we enable customers to move beyond simply facilitating transactions and supporting HR-driven processes, to focus on creating a human-centered approach.\nThis means putting your people and their experiences at the center of everything, listening to their needs and providing them with the tools and information to be productive and make a real impact on the business. Our HXM Suite helps you redefine experiences -- making everyone (candidates, new hires, employees, managers, and HR leaders) feel connected, engaged, empowered, and supported at every step in their employee journey. \nAbout This Demo Script:\nThis script follows one persona, Alex Smith, through the journey from candidate to new hire to employee and, finally, to manager.While the story assumes that you will show Alex as the same persona throughout the demo, you may prefer to show different personas. If so, you will need to adjust the accompanying slide deck and talk track accordingly.\nVignette 1 \n- Intro to Candidate ExperienceAs a candidate, you ask yourself: Can you imagine yourself working for this organization?\n You are driven by meaningful work, supportive management, fantastic work environment, and growth opportunities amongst other things. Will this Company offer that to you? \n You want to understand this company’s culture: does their Corporate Culture align with your priorities? You want to get a sense of their culture including work/life balance, purpose, diversity, etc. through the recruitment experience.\nDemo Flow Demo Story/Message\n. What we want to highlight through this story and solution demonstration is how human experience management (HXM) helps organizations go beyond simply facilitating transactions to truly reinvent experiences in ways that accelerate business growth and drive engagement. \n We do this by shifting the focus from supporting top-down, HR-driven processes to delivering individualized experiences designed completely around the needs of the people in your organization.As we think about how you are going to meet the expectations of your workforce, we need to think about what the ideal experience is for them. \n In fact, we need to start with the experience before they even become an employee. What exactly are candidates looking for?When you think about critical moments for a candidate – searching for a job, the application process, multiple interviews, etc., each of those typically result in many questions and uncertainties. \n  But many organizations offer a less than engaging candidate experience.When it comes to attracting the right talent and offering an engaging candidate experience, many companies struggle with challenges such as a requisition-centric process, high cost of candidate acquisition, long time to hire, and competing with other organizations trying to attract the same high-quality candidates.Organizations face a continued need to attract workers with technological and other specialized skills, yet many have an inability to effectively convey their employer brand.\n Poor sourcing methodologies often lead to ineffective talent pools. Many have antiquated recruiting systems that tend to be limited to applicant tracking and lack complete applicant marketing and mobile capabilities.\n With the current talent shortages, we’re all reading about, this leaves many organizations unable to compete in what some are now calling a new “War for Talent”.",
                "Provide a audio script track for the SuccessFactors recruiting solution for a fashion retail business. Include a headline, intro, description and outro",
                "Provide 10 limbic openings for a presentation about talent management, learning and payroll.",
                "Provide a talk track introducing Successfactors HR to retail customers with HR leaders in the audience",
                "Write an email talking about the perennial HR challenges with a thematic tie-in to the World Cup finals.",
                "You are a presales expert. Write an email to [person] with some facts about how SuccessFactors has over 3000 EC Customers with a thematic tie-in to Christmas.",
                "Write an email talking about the perennial HR challenges around hiring, motiving and guiding employees in English and German",
                "Generate a sample Non Disclosure Agreement document for retail company 'Best Run' for its external contractors",
                "Help me generate a AI image prompt similar to - Award-winning mix-use complex contemporary designed by the best architects in England, stunning London riverside, high resolution, ultra-detailed, 8k, architectural photography Archdaily, Hyper-realistic, intricate detail, photorealistic",
                "Write a twitter thread on the benefits of blockchain based verified employee credentials",
                "Craft an SEO friendly Linkedin post about diversity and inclusion in the workplace. Provide the target keywords."]
sap_options4 = ["",
                "Please generate a job description for a [Digital Marketing Specialist].The ideal candidate should have skills in [SEO/SEM, marketing database, email, social media, and display advertising campaigns]. \n They must be able to have experience in [leading integrated digital marketing campaigns from concept to execution] and have additional experience in [ knowledge of website analytics tools]. Please include the job responsibilities and required qualifications.Ensure the job description does not have bias and is inclusive.",
                "Write me python and abap code to make a REST API call and authenticate via Microsoft Active Directory",
                "Provide in a table format an Employee table with the following columns and 10 randomized entries \n [EmployeeId, Employee Name, Job Classification, Cost Center, Region, Job Location, Department, Average Tenure, Total YOE, Pay Grade, Total CTC, Compa- ratio. Impact-of-leaving, Cost-to-train/year, Performance Rating, Future Leader]",
                "Write me a VBA macro to create a presentation for a startup.",
                "Generate a sample google sheet with sample movies dataset that can be used for exploratory analysis."]

bool_search=""
count_str=""
result_str=""
response=""
st.set_page_config(page_title="Ask Chatty McChatface", page_icon=':bar_chart:', layout='wide')


st.header("👋 Ask Chatty McChatface v1")
st.caption("Demo app that showcases how to do prompt engineering with Open AI and how to build an enterprise knowledge base using custom embeddings.")


with st.expander("💬 Features and Help"):
    st.write('''
Features :
1. **Prompt Engineering** - Primed prompts to provide factual information and cite references. 
2. **Prompt List** - Out of the box 20+ prompts based on job functions and roles.
2. **Enterprise Search** - Link to an enterprise knowledge base. Shows how business domain and up to date information can be provided.
3. **Hide PII and Confidential Information** - Redact feature to hide PII data and other confidential information.
4. **Save Results** - Export responses to a Word Document.
5. **History** - View history of requests made.
***
Prompts : 

🕳 **Consultants and Partners**
1. What was <<enter company>> revenue in 2020.
2. Compare <<enter company>> and <<enter company>> against Successfactors in the North America region.
3. List HR software companies in Middle East and North Africa region listing their strengths in the region.
4. What is the learning plan to be become a Successfactors LMS consultant? What skills do I need?
5. What are the different types of partnerships that SAP offers? What is a solution extension partner?
6. How do I change the theme in the Successfactors application? Provide steps for an adminstrator.
7. You are HustleGPT, an entrepreneurial AI. You have $200, and your goal is to turn that into as much money as possible in the shortest time possible without doing anything illegal. Provide detailed steps.
***                 
💡 **Industry & Emerging Trends**
1. You are an HR industry expert. Provide the top HR challenges facing the retail industry.
2. Write a 300-word SEO-friendly blog with right keywords, title, meta-description, h1,h2 details and  5 examples on how the gig economy will change the retail industry.
3. Provide a short blog post on job functions that may be displaced by AI in the financial sector with an intro, description and conclusion section.
4.Write an outline for an ebook with 10 chapters on how the future of hybrid work can be improved by Web3 and Metaverse. Provide detailed titles and sites as references.
***
🗯 **Content Generation (Sales & Marketing)**
1. Provide a audio script track for the SuccessFactors recruiting solution for a fashion retail business. Include a headline, intro, description and outro.
2. Provide 10 limbic openings for a presentation about talent management, learning and payroll.
3. Provide a talk track introducing Successfactors HR to retail customers with HR leaders in the audience.
4. Write an email talking about the perennial HR challenges with a thematic tie-in to the World Cup finals.
5. You are a presales expert. Write an email to [person] with some facts about how SuccessFactors has over 3000 EC Customers with a thematic tie-in to Christmas.
6. Write an email talking about the perennial HR challenges around hiring, motiving and guiding employees in English and German.
7. Help me generate a Midjourney prompt similar to - Award-winning mix-use complex contemporary designed by the best architects in England, stunning London riverside, high resolution, ultra-detailed, 8k, architectural photography Archdaily, Hyper-realistic, intricate detail, photorealistic
8. Write a twitter thread on the benefits of blockchain based verified employee credentials
9.Rewrite this demo script for a Retail customer  \n Introduction: \n HXM, Human Experience Management, is an evolution of HCM. HXM is about creating individualized, dynamic experiences for all users - whether candidates, new hires, employees, managers or HR leaders.Because our people determine whether an organization succeeds or fails, the experiences we deliver and how we address the moments that matter for every individual impact everything from top line business growth to profitability to how quickly an organization can adapt to change.With HXM we enable customers to move beyond simply facilitating transactions and supporting HR-driven processes, to focus on creating a human-centered approach.\nThis means putting your people and their experiences at the center of everything, listening to their needs and providing them with the tools and information to be productive and make a real impact on the business. Our HXM Suite helps you redefine experiences -- making everyone (candidates, new hires, employees, managers, and HR leaders) feel connected, engaged, empowered, and supported at every step in their employee journey. \nAbout This Demo Script:\nThis script follows one persona, Alex Smith, through the journey from candidate to new hire to employee and, finally, to manager.While the story assumes that you will show Alex as the same persona throughout the demo, you may prefer to show different personas. If so, you will need to adjust the accompanying slide deck and talk track accordingly.\nVignette 1 \n- Intro to Candidate ExperienceAs a candidate, you ask yourself: Can you imagine yourself working for this organization?\n You are driven by meaningful work, supportive management, fantastic work environment, and growth opportunities amongst other things. Will this Company offer that to you? \n You want to understand this company’s culture: does their Corporate Culture align with your priorities? You want to get a sense of their culture including work/life balance, purpose, diversity, etc. through the recruitment experience.\nDemo Flow Demo Story/Message\n. What we want to highlight through this story and solution demonstration is how human experience management (HXM) helps organizations go beyond simply facilitating transactions to truly reinvent experiences in ways that accelerate business growth and drive engagement. \n We do this by shifting the focus from supporting top-down, HR-driven processes to delivering individualized experiences designed completely around the needs of the people in your organization.As we think about how you are going to meet the expectations of your workforce, we need to think about what the ideal experience is for them. \n In fact, we need to start with the experience before they even become an employee. What exactly are candidates looking for?When you think about critical moments for a candidate – searching for a job, the application process, multiple interviews, etc., each of those typically result in many questions and uncertainties. \n  But many organizations offer a less than engaging candidate experience.When it comes to attracting the right talent and offering an engaging candidate experience, many companies struggle with challenges such as a requisition-centric process, high cost of candidate acquisition, long time to hire, and competing with other organizations trying to attract the same high-quality candidates.Organizations face a continued need to attract workers with technological and other specialized skills, yet many have an inability to effectively convey their employer brand.\n Poor sourcing methodologies often lead to ineffective talent pools. Many have antiquated recruiting systems that tend to be limited to applicant tracking and lack complete applicant marketing and mobile capabilities.\n With the current talent shortages, we’re all reading about, this leaves many organizations unable to compete in what some are now calling a new “War for Talent”."
***
💛 **Data & Code Generation**
1. Please generate a job description for a [Digital Marketing Specialist].The ideal candidate should have skills in [SEO/SEM, marketing database, email, social media, and display advertising campaigns]. They must be able to have experience in [leading integrated digital marketing campaigns from concept to execution] and have additional experience in [ knowledge of website analytics tools]. Please include the job responsibilities and required qualifications.Ensure the job description does not have bias and is inclusive.
2. Provide in a table format an Employee table with the following columns and 10 randomized entries EmployeeId, Employee Name, Job Classification, Cost Center, Region, Job Location, Department, Average Tenure, Total YOE, Pay Grade, Total CTC, Compa- ratio. Impact-of-leaving, Cost-to-train/year, Performance Rating, Future Leader.
3. Write me python and abap code to make a REST API call and authenticate via Microsoft Active Directory.
4. Write me a VBA macro to create a presentation for a startup.
5. Generate a sample google sheet with sample movies dataset that can be used for exploratory analysis.
    ''')

sidebar_placeholder = st.sidebar.container()

if 'response' not in st.session_state:
    st.session_state.response = ''

if 'key' not in st.session_state:
    st.session_state['key'] = ''

sidebar_placeholder.header('🍁 History:')

selected_value1 = ''
selected_value2 = ''
selected_value3 = ''
selected_value4 = ''

conversation=[{"role": "system", "content": "You are a helpful assistant that provides detailed answers based on facts. Always cite references for your responses towards the end of the response. "}]
user_input=''


def replace_ner(mytxt):
    clean_text = mytxt
    doc = nlp(mytxt)
    for ent in reversed(doc.ents):
        clean_text = clean_text[:ent.start_char] +ent.label_ + clean_text[ent.end_char:]
    return clean_text
def enterprise_search():
    index_name = 'demo-index'

    # initialize connection (get API key at app.pinecone.io)
    pinecone.init(
        api_key="5e6a8cb6-f036-4a23-9b34-c95aec8e317f",
        environment="us-west1-gcp-free"  # find next to API key
    )

    # connect to index

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
    docsearch = Pinecone.from_existing_index(index_name, embeddings)

    llm = OpenAIChat(temperature=0, openai_api_key=os.environ['OPENAI_API_KEY'], model_name='gpt-3.5-turbo',
                     model_kwargs={'max_tokens': 1000})

    query = "You are a friendly knowledge bot that provides factual responses from the given context in sentences and bullet points. Always end with a line that cites references and paragraphs used for your results." + st.session_state.prompt
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = docsearch.similarity_search(st.session_state.prompt)
    # print(docs)
    st.session_state.docs = docs
    st.session_state.response = chain.run(input_documents=docs, question=query)
    print(st.session_state.response)
    # total_tokens = response.get("total_tokens")
    # # pricing logic: https://openai.com/pricing#language-models
    #     if st.session_state.model == "gpt-3.5-turbo":
    #         cost = total_tokens * 0.002 / 1000

def bing_search():
    query = st.session_state.prompt.replace(" ", "+")  # replacing the spaces in query result with +

    if query:  # Activates the code below on hitting Enter/Return in the search textbox
        try:  # Exception handling
            req = r.get(f"https://www.bing.com/search?q={query}",
                        headers={
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"})
            result_str = '<html><table style="border: none;">'  # Initializing the HTML code for displaying search results
            print (req.status_code)
            if req.status_code == 200:  # Status code 200 indicates a successful request
                bs = BeautifulSoup(req.content,
                                   features="html.parser")  # converting the content/text returned by request to a BeautifulSoup object
                search_result = bs.find_all("li",
                                            class_="b_algo")  # 'b_algo' is the class of the list object which represents a single result
                search_result = [str(i).replace("<strong>", "") for i in search_result]  # removing the <strong> tag
                search_result = [str(i).replace("</strong>", "") for i in search_result]  # removing the </strong> tag
                result_df = pd.DataFrame()  # Initializing the data frame that stores the results

                for n, i in enumerate(search_result):  # iterating through the search results
                    individual_search_result = BeautifulSoup(i,
                                                             features="html.parser")  # converting individual search result into a BeautifulSoup object
                    h2 = individual_search_result.find('h2')  # Finding the title of the individual search result

                    print (h2)

                    href = h2.find('a').get('href')  # title's URL of the individual search result
                    cite = f'{href[:50]}...' if len(href) >= 50 else href  # cite with first 20 chars of the URL
                    url_txt = h2.find('a').text  # title's text of the individual search result
                    # In a few cases few individual search results doesn't have a description. In such cases the description would be blank
                    description = "" if individual_search_result.find('p') is None else individual_search_result.find(
                        'p').text
                    # Appending the result data frame after processing each individual search result
                    result_df = result_df.append(
                        pd.DataFrame({"Title": url_txt, "URL": href, "Description": description}, index=[n]))
                    count_str = f'<b style="font-size:20px;">Bing Search returned {len(result_df)} results</b>'
                    ########################################################
                    ######### HTML code to display search results ##########
                    ########################################################
                    result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_txt}</a></h3></tr>' + \
                                  f'<tr style="border: none;"><strong style="color:green;">{cite}</strong></tr>' + \
                                  f'<tr style="border: none;">{description}</tr>' + \
                                  f'<tr style="border: none;"><td style="border: none;"></td></tr>'
                result_str += '</table></html>'
                print (result_str)
            # if the status code of the request isn't 200, then an error message is displayed along with an empty data frame
            else:
                result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
                result_str = '<html></html>'
                count_str = '<b style="font-size:20px;">Looks like an error!!</b>'

        # if an exception is raised, then an error message is displayed along with an empty data frame
        except Exception as e:
            result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
            result_str = f'<html>caught {type(e)}: e</html>'
            count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
            print (e)


        # # st.markdown(f'{count_str}', unsafe_allow_html=True)
        # st.markdown(f'{result_str}', unsafe_allow_html=True)
        # st.markdown('<h3>Data Frame of the above search result</h3>', unsafe_allow_html=True)
        # st.dataframe(result_df)

# def google_sheets():
#     # Create a connection object.
#     # service_account_info = json.loads(google_json)
#     credentials = service_account.Credentials.from_service_account_info(google_json)
#
#     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#     creds_with_scope = credentials.with_scopes(scope)
#
#     client = gspread.authorize(creds_with_scope)
#     # Perform SQL query on the Google Sheet.
#     # Uses st.cache_data to only rerun when the query changes or after 10 min.
#     @st.cache_data(ttl=600)
#     def run_query(query):
#         spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1twXfKk7IcMMVw2uv1arnqjZKDLjoHw8PepTThX0yBdo/edit?usp=sharing')
#         worksheet = spreadsheet.get_worksheet(0)
#         records_data = worksheet.get_all_records()
#         print(records_data)

def save_to_pptx(ai_content: str):
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    # print(ai_content)
    title.text = "Generated Content"
    subtitle.text = "By Chatty McChatface"

    # adding text
    if st.session_state.response:
        # for i in range(len(st.session_state.response)):
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            title = slide.shapes.title
            title.text = "Response from AI"
            # For adjusting the  Margins in inches
            left = top = width = height = Inches(1)

            # creating textBox
            txBox = slide.shapes.add_textbox(left-0.5, top - 0.5,
                                              width * 9, height * 7)
             # creating textFrames
            tf = txBox.text_frame
            tf.word_wrap = True
            tf.text = st.session_state.prompt
            p = tf.add_paragraph()
            p.font.size = Pt(14)
            p.text = st.session_state.response
            p.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT

    # save the output into binary form
    binary_output = BytesIO()
    prs.save(binary_output)


    return binary_output.getvalue()

def download_docx():
    doc = docx.Document()

    # Add Title Page followed by section summary
    doc.add_heading("Generated Output", 0)
    doc.add_paragraph(f'Authored By: Chatty McChatface')

    doc.add_heading("Request", 1)
    doc.add_paragraph(st.session_state.prompt.capitalize())

    doc.add_heading("Response", 1)
    doc.add_paragraph(st.session_state.response)
    binary_output = BytesIO()
    doc.save(binary_output)
    return binary_output.getvalue()

def send_click():
    with st.spinner("Fetching response..."):
        if bool_search:
            enterprise_search()
        else:
            st.session_state['key'] = st.session_state['key'] + '~~~' + st.session_state.prompt.capitalize()
            user_input = st.session_state.prompt
            #   print( st.session_state['key'])
            with sidebar_placeholder:
                for keys in st.session_state['key'].split('~~~'):
                    if ( keys != ''):
                        sidebar_placeholder.info(keys)

            # sidebar_placeholder.write(st.session_state['key'])
            st.session_state.competitor = sap_options1[0]
            st.session_state.industry = sap_options2[0]
            st.session_state.talk = sap_options3[0]
            st.session_state.demo = sap_options4[0]

            conversation.append({"role": "user", "content": user_input})
            # print(st.session_state.bool_search)

            st.session_state.response = OpenAIService.open_ai_query(query='',model='gpt-4',gpt_conversation_history=conversation)
            conversation.append({"role": "assistant", "content": st.session_state.response})


##print(OpenAIService.open_ai_get_embeddings("Some sample texts"))
c1, c2, c3, c4 = st.columns(4)

with c1:
    selected_value1 = st.selectbox("🕳 Consultants and Partners", sap_options1, key='competitor')
with c2:
    selected_value2 = st.selectbox("💡 Industry & Emerging Trends", sap_options2, key='industry')
with c3:
    selected_value3 = st.selectbox("🗯 Content Generation (Sales & Marketing)", sap_options3, key='talk')
with c4:
    selected_value4 = st.selectbox("💛 Data & Code Generation", sap_options4, key='demo')

if (selected_value1 != ''):
    st.session_state.prompt = selected_value1
if (selected_value2 != ''):
    st.session_state.prompt = selected_value2
if (selected_value3 != ''):
    st.session_state.prompt = selected_value3
if (selected_value4 != ''):
    st.session_state.prompt = selected_value4

with streamlit_analytics.track():
    c = st.container()
    c.text_area("🦋 Ask something: ", key='prompt')
    bool_search = c.checkbox('Include Enterprise Search', key='bool_search')
    redact = c.checkbox('Redact Confidential Information')
    c.button("✅ Send", on_click=send_click)
    # google_sheets()



if st.session_state.response:
    if redact:
        response = replace_ner(st.session_state.response)
    else:
        response = st.session_state.response

    # nlp.add_pipe('sentencizer')  # updated
    # doc = nlp(response)
    # sentences = [sent.text.strip() for sent in doc.sents]
    # response = ""
    # for sentence in sentences:
    #     response = response + sentence
    if bool_search:
        st.success(response)
        # st.success(st.session_state.docs)
    else:
        st.info(response)
    # st.download_button(
    #     label="Download",
    #     data=save_to_pptx("\n".join([str(d) for d in st.session_state.response])),
    #     file_name="chatty.pptx",
    #     mime="application/pptx",
    # )

    st.download_button(
            label="⬇️ Download",
            data=download_docx(),
            file_name="Chatty McChatface Response-" + datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S") + ".docx",
            mime="docx"
        )
    # pyperclip.copy(st.session_state.response)
    # st.info("Response copied to clipboard")


    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**Contact Me: [@sidbhat5](https://twitter.com/sidbhat5)**', icon="💡")
    with c2:
        st.info('**Prompts Guide: [Prompts](https://sidbhat.blog/10-chat-gpt-prompts-to-help-you-succeed/)**', icon="💻")
    with c3:
        st.info('**Google Collab: [Code](https://colab.research.google.com/drive/)**', icon="🧠")

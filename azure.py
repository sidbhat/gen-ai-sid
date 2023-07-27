import streamlit_analytics
from open_ai_service import OpenAIService
import streamlit as st
from pptx import Presentation
from io import BytesIO
from pptx.util import Inches, Pt
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
import docx
import datetime
# from google.oauth2 import service_account
# import json

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

sap_options1 = ["", "You are HustleGPT, an entrepreneurial AI. You have $200, and your goal is to turn that into as much money as possible in the shortest time possible without doing anything illegal. Provide detailed steps.",
                "What was <<enter company>> revenue in 2020", "How many companies has <<enter company>> acquired so far?",
                "Compare <<enter company1>> and <<enter company2>> against Successfactors in the North America region",
                "List HR software companies in Middle East and North Africa region listing their strengths in the region",
                "What is the learning plan to be become a Successfactors LMS consultant? What skills do I need?",
                "What are the different types of partnerships that SAP offers? What is a solution extension partner?",
                "How do I change the theme in the Successfactors application? Provide steps for an adminstrator"]
sap_options2 = ["", "You are an HR industry expert. Provide the top HR challenges facing the retail industry",
                "Write a 300 word blog with 5 examples on how the gig economy will change the retail industry",
                "Write an outline for an ebook with 10 chapters on how the future of hybrid work can be improved by Web3 and Metaverse. Provide detailed titles and sites as references.",
                "Provide a short blog post on job functions that may be displaced by AI in the financial sector with an intro, description and conclusion section"]
sap_options3 = ["",
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

st.set_page_config(page_title="Ask Chatty McChatface", page_icon=':bar_chart:', layout='wide')

st.subheader("👋 Ask Chatty McChatface v1")
st.warning(
    "👀 All the training data used is from the public domain on this page. Do not share any confidential information."

)
with st.expander("💬 Help on prompts"):
    st.write('''
***
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
2. Write a 300 word blog with 5 examples on how the gig economy will change the retail industry.
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
#openai.api_key='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'


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
        st.session_state['key'] = st.session_state['key'] + '~~~' + st.session_state.prompt.capitalize()
        user_input = st.session_state.prompt
        #   print( st.session_state['key'])
        with sidebar_placeholder:
            for keys in st.session_state['key'].split('~~~'):
                sidebar_placeholder.info(keys)

        # sidebar_placeholder.write(st.session_state['key'])
        st.session_state.competitor = sap_options1[0]
        st.session_state.industry = sap_options2[0]
        st.session_state.talk = sap_options3[0]
        st.session_state.demo = sap_options4[0]
        conversation.append({"role": "user", "content": user_input})
        print(conversation)

        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=conversation
        # )
        st.session_state.response = OpenAIService.open_ai_query(query='',model='gpt-4',gpt_conversation_history=conversation)
        #   print(st.session_state.response)
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
    st.text_area("🦋 Ask something: ", key='prompt')
    st.button("✅ Send", on_click=send_click)
    # google_sheets()

if st.session_state.response:
    st.markdown(st.session_state.response)
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

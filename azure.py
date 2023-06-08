import streamlit_analytics
from open_ai_service import OpenAIService
import streamlit as st
import os
import openai

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

def send_click():
    with st.spinner("Fetching response..."):
        st.session_state['key'] = st.session_state['key'] + '~~~' + st.session_state.prompt.capitalize()
        user_input = st.session_state.prompt
        #   print( st.session_state['key'])
        with sidebar_placeholder:
            for keys in st.session_state['key'].split('~~~'):
                sidebar_placeholder.write(keys)
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
        st.session_state.response = OpenAIService.open_ai_query(query='',model='gpt-4-32k',gpt_conversation_history=conversation)
        #   print(st.session_state.response)
        conversation.append({"role": "assistant", "content": st.session_state.response})
        st.session_state.prompt = ''

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
    st.button("Send", on_click=send_click)

if st.session_state.response:
    st.markdown(st.session_state.response)
    # pyperclip.copy(st.session_state.response)
    # st.info("Response copied to clipboard")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**Contact Me: [@sidbhat5](https://twitter.com/sidbhat5)**', icon="💡")
    with c2:
        st.info('**Prompts Guide: [Prompts](https://sidbhat.blog/10-chat-gpt-prompts-to-help-you-succeed/)**', icon="💻")
    with c3:
        st.info('**Google Collab: [Code](https://colab.research.google.com/drive/)**', icon="🧠")

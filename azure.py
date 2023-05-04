import streamlit_analytics
from open_ai_service import OpenAIService
import streamlit as st
import pyperclip

sap_options1 = ["", "What was Workday's revenue in 2020", "How many companies has Workday acquired so far?",
                "Compare Workday and Oracle against Successfactors in the North America region",
                "List HR software companies in Middle East and North Africa region listing their strengths in the region"]
sap_options2 = ["", "Top HR challenges facing the retail industry",
                "Write a 300 word blog with 5 examples on how the gig economy will change the retail industry",
                "Provide a short blog post on job functions that may be displaced by AI in the financial sector with an intro, description and conclusion section"]
sap_options3 = ["",
                "Provide a audio script track for the SuccessFactors recruiting solution for a fashion retail business. Include a grabber headline, intro, description and outro",
                "Provide 10 limbic openings for a presentation about talent management, learning and payroll.",
                "Provide a talk track introducing Successfactors HR to retail customers with HR leaders in the audience",
                "Write an email talking about the perennial HR challenges with a thematic tie-in to the World Cup finals.",
                "You are a presales expert. Write an email to [person] with some facts about how SuccessFactors has over 3000 EC Customers with a thematic tie-in to Christmas.",
                "Write an email talking about the perennial HR challenges around hiring, motiving and guiding employees in English and German"]
sap_options4 = ["",
                "Please generate a job description for a [Digital Marketing Specialist].The ideal candidate should have skills in [SEO/SEM, marketing database, email, social media, and display advertising campaigns]. \n They must be able to have experience in [leading integrated digital marketing campaigns from concept to execution] and have additional experience in [ knowledge of website analytics tools]. Please include the job responsibilities and required qualifications.Ensure the job description does not have bias and is inclusive.",
                "Provide in a table format an Employee table with the following columns and 10 randomized entries \n [EmployeeId, Employee Name, Job Classification, Cost Center, Region, Job Location, Department, Average Tenure, Total YOE, Pay Grade, Total CTC, Compa- ratio. Impact-of-leaving, Cost-to-train/year, Performance Rating, Future Leader]"]

st.set_page_config(page_title="Ask Chatty McChatface", page_icon=':bar_chart:', layout='wide')

st.subheader("👋 Ask Chatty McChatface")
st.warning(
    "👀 All the training data used is from the public domain on this page. Do not share any confidential information."
)
with st.expander("💬 Help on prompts"):
    st.write('''
***
🕳 **Competitor Specific Prompts**
1. What was Workday's revenue in 2020.
2. Compare Workday and Oracle against Successfactors in the North America region.
3. List HR software companies in Middle East and North Africa region listing their strengths in the region.
4. How many companies has Workday acquired so far.
***                 
💡 **Industry Specific Prompts**
1. Top HR challenges facing the retail industry.
2. Write a 300 word blog with 5 examples on how the gig economy will change the retail industry.
3. Provide a short blog post on job functions that may be displaced by AI in the financial sector with an intro, description and conclusion section.
***
🗯 **Talk track Specific Prompts**
1. Provide a audio script track for the SuccessFactors recruiting solution for a fashion retail business. Include a grabber headline, intro, description and outro.
2. Provide 10 limbic openings for a presentation about talent management, learning and payroll.
3. Provide a talk track introducing Successfactors HR to retail customers with HR leaders in the audience.
4. Write an email talking about the perennial HR challenges with a thematic tie-in to the World Cup finals.
5. You are a presales expert. Write an email to [person] with some facts about how SuccessFactors has over 3000 EC Customers with a thematic tie-in to Christmas.
6. Write an email talking about the perennial HR challenges around hiring, motiving and guiding employees in English and German.
***
💛 **Demo Specific Prompts**
1. Please generate a job description for a [Digital Marketing Specialist].The ideal candidate should have skills in [SEO/SEM, marketing database, email, social media, and display advertising campaigns]. They must be able to have experience in [leading integrated digital marketing campaigns from concept to execution] and have additional experience in [ knowledge of website analytics tools]. Please include the job responsibilities and required qualifications.Ensure the job description does not have bias and is inclusive.
2. Provide in a table format an Employee table with the following columns and 10 randomized entries EmployeeId, Employee Name, Job Classification, Cost Center, Region, Job Location, Department, Average Tenure, Total YOE, Pay Grade, Total CTC, Compa- ratio. Impact-of-leaving, Cost-to-train/year, Performance Rating, Future Leader.
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


def send_click():
    with st.spinner("Fetching response..."):
        st.session_state['key'] = st.session_state['key'] + '~~~' + st.session_state.prompt.capitalize()
        #   print( st.session_state['key'])
        with sidebar_placeholder:
            for keys in st.session_state['key'].split('~~~'):
                sidebar_placeholder.write(keys)
        # sidebar_placeholder.write(st.session_state['key'])
        st.session_state.competitor = sap_options1[0]
        st.session_state.industry = sap_options2[0]
        st.session_state.talk = sap_options3[0]
        st.session_state.demo = sap_options4[0]
        st.session_state.response = OpenAIService.open_ai_query(st.session_state.prompt)
        st.session_state.prompt = ''


c1, c2, c3, c4 = st.columns(4)

with c1:
    selected_value1 = st.selectbox("🕳 Select from Competitor list", sap_options1, key='competitor')
with c2:
    selected_value2 = st.selectbox("💡 Select from Industry list", sap_options2, key='industry')
with c3:
    selected_value3 = st.selectbox("🗯 Select from Talk track list", sap_options3, key='talk')
with c4:
    selected_value4 = st.selectbox("💛 Select from Demo Data", sap_options4, key='demo')

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
    st.success(st.session_state.response, icon="🤖")
#    pyperclip.copy(st.session_state.response)
#    st.info("Response copied to clipboard")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**Contact Me: [@sidbhat5](https://twitter.com/sidbhat5)**', icon="💡")
    with c2:
        st.info('**Open AI: [@openai](https://twitter.com/openai)**', icon="💻")
    with c3:
        st.info('**Report Bugs: Email [sid](mailto:siddhartha.bhattacharya@sap.com)**', icon="🧠")

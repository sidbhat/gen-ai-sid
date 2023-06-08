import streamlit as st

query = ''
model = ''

def click():
    st.write(st.session_state.query)

with st.form(key='open_ai',clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            query = c1.selectbox(label='Select Query', key="query", options=['','Generate a 300 word essay on', 'Write a twitter thread'], on_change=click())
            model=''
            st.session_state.prompt = query
        with c2:
            model = c1.selectbox(label='Select Model', key="model", options=['','gpt3.5', 'gpt4'])
            query=''
            st.session_state.prompt = model

        st.text_input("Ask something: ", key='prompt')
        st.form_submit_button('Enter', on_click=click())
        st.write(st.session_state.prompt)
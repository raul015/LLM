from langchain_test import get_agent
import streamlit as st 


st.title("Prova")

question = st.text_input("Question: ")
if question:

    agent = get_agent()
    answer = agent.invoke(question)

    st.header("Answer: ")
    st.write(answer)
    
# # Funzione con cui lancerò Streamlit
# def main():
#     fill_db()
#     pass
#     # print('Sei dentro il main')

# if __name__ == "__main__":

#     main()
import os
from langchain_community.utilities import SQLDatabase
# FUNZIONE PEE LA PULIZIA DEI CARATTERI ''' 
import re
from langchain_google_genai import GoogleGenerativeAI


# Stringa di connessione per PostgreSQL
db_uri = f"postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"

# Creare un'istanza del database con LangChain
db = SQLDatabase.from_uri(db_uri)

# Test: Esegui una query per verificare la connessione
# query = "SELECT * FROM t_shirts"
query = """ CREATE TABLE IF NOT EXISTS t_shirts ( t_shirts_id SERIAL PRIMARY KEY,brand_shirt TEXT CHECK (brand_shirt IN ('Van Huesen', 'Levi', 'Nike', 'Adidas')) NOT NULL, 
        color_shirt TEXT CHECK (color_shirt IN ('Red', 'Blue', 'Black', 'White')) NOT NULL, 
        size_shirt TEXT CHECK (size_shirt IN ('XS', 'S', 'M', 'L', 'XL')) NOT NULL, 
        price_shirt INT CHECK (price_shirt BETWEEN 10 AND 50), 
        stock_quantity INT NOT NULL, 
        CONSTRAINT unique_brand_color_size UNIQUE (brand_shirt, color_shirt, size_shirt) 
        ); """

results = db.run(query)

# Stampa i risultati
print("✅ Tabelle disponibili nel database:")
print(results)


query = """CREATE TABLE IF NOT EXISTS  discount(
    discount_id SERIAL PRIMARY KEY,
    tshirts_id INT NOT NULL,
    discount_percentage DECIMAL(5,2) CHECK (discount_percentage BETWEEN 0 AND 100)
    ); """
results = db.run(query)

# Stampa i risultati
print("✅ Tabelle disponibili nel database:")
print(results)

# Query di controllo 

query = "SELECT * FROM t_shirts"
results = db.run(query)

# Stampa i risultati
print("SELECT * FROM t_shirts:  ")
print(results)


query = "SELECT * FROM t_shirts"
results = db.run(query)

# Stampa i risultati
print("SELECT * FROM discount:  ")
print(results)

api_key = os.getenv("GOOGLE_API_KEY")



print("INZIO DELLA PARTE CON MODELLO GEMINI FORNITO DA GOOGLE")


if not api_key:
    raise ValueError("API Key non trMostrami tutti i prodotti Nike nel database.ovata! Assicurati di impostare GEMINI_API_KEY come variabile d'ambiente.")

# Scegli un modello disponibile per la tua API Key
model_name = "gemini-2.0-flash-001"  

# Inizializza il modello con LangChain
llm = GoogleGenerativeAI(model=model_name, api_key=api_key)

# Adesso creo la catena che collega gemini al dataBAse
# Questo mi serve per interrogare direttamente il database
# in modo conversionare, così Gemini capisce la struttura del DataBase 

from langchain_community.agent_toolkits.sql.base import create_sql_agent, SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# db agent è qualcosa di nuovo che non ho ancora visto,
# nelle versioni precedenti non c'era infatti molte funzioni
# ho visto che sono state deprecate...

db_agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True)

# Questo serve per rispettare i limiti di richieste con l'API di GEMINI
import time
# question = "Show me all the products Nike in the database and give me the finale count of this products, give me also the query that you used, please not limit"



# Qui il modello sbaglia... non tiene conto dei pezzi disponibili 
# question1 = "Il prezzo totale delle tshirts con taglia s? dammi anche la query"

# response1 = db_agent.invoke({"input": question1})
# print("\n✅ Risposta dal database:")
# print(response1)

# time.sleep(2)
# response2 = db_agent.invoke({"input": "SELECT SUM(price_shirt*stock_quantity) FROM t_shirts WHERE size_shirt = 'S' "})
# print("\n✅ Risposta dal database2:")
# print(response2)


# time.sleep(2)
# response3 = db_agent.invoke({"input": "Se dobbiamo vendere tutte le T-shirts Levi's oggi con lo sconto applicato. quanto guadagno?"})

# print("\n✅ Risposta dal database3:")
# print(response3)


# time.sleep(2)
# response4 = db_agent.invoke({"input": "Quante t-shirt Levi's bianche/white ho disponibili?"})

# print("\n✅ Risposta dal database4:")
# print(response4)


time.sleep(2)


# response5 = db_agent.invoke({"input": "SELECT sum(stock_quantity) FROM t_shirts where brand_shirt='Levi' and color_shirt='White'"})

# print("\n✅ Risposta dal database4:")
# print(response5)



# Gli esempi che ho appena fatto li inserisco all'interno di un dizionario

# Aprire PGAdming o da terminale interrogare il proprio database 
risposta1 = 111
risposta2 = 12701

few_shots = [  
    {
         'Question': "Quante t-shirt Nike di colore white ho disponibili?",
         'SQLQuery':  "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand_shirt = 'Nike' AND color_shirt = 'White'",
         'SQLResult': "Result of the SQL query",
         'Answer': str(risposta1)  # Convert integer to string
    },
    {
         'Question': "Il prezzo totale delle tshirts con taglia S?",
         'SQLQuery':  "SELECT SUM(price_shirt*stock_quantity) FROM t_shirts WHERE size_shirt = 'S' ",
         'SQLResult': "Result of the SQL query",
         'Answer': str(risposta2)  # Convert integer to string
    }
]

# Adesso che ho le ambiguità trovate all'interno di un vettore posso fare al seguente cosa: 
# Hugging phase oer generare gli embedding 

# from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-l6-v2',
            model_kwargs={'device': 'cpu'})

# Example embedding
e = embeddings.embed_query("Quante t-shirt Nike bianche/white ho disponibili?")
print(f"Embedding size: {len(e)}")

# HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-l6-v2')

# few_shots lielaborato per essere tutto contenuto in una sola stringa 
# to_vectorize = [" ".join( example.values()) for example in few_shots]
# print(to_vectorize[0])

# Convert few_shots into strings for vectorization
to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
print("First vectorized example:", to_vectorize[0])


# Ora utilizzo Vector database Chroma 

from langchain_community.vectorstores import Chroma

vectorsStore = Chroma.from_texts(
    texts=to_vectorize,
    embedding=embeddings,
    metadatas=few_shots  # Ensure metadatas are dictionaries
)
# Il lavoro di vectorStore è prendere in input una domanda,, lo convertirà in un 
# embedding ci fornirà il pi simile tra i few_shots di esempio, vrediamo ora come funziona 

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

# Initialize example selector
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorsStore,
    k=2  # Get the 2 most similar examples
)
# K=2 sta a significare dammi 2 esempi simili 

# example_selector.select_examples("quante Tshirts Adidas sono rimaste nello store?")
# print(example_selector)

selected_examples = example_selector.select_examples({"question": "Quante Tshirts Adidas sono rimaste nello store?"})
# Print results
# print("Selected Examples:")
# for ex in selected_examples:
#     print(ex)


PROMPT_SUFFIX = """
Use the following format:

Question: "Your question here"
SQLQuery: "The SQL query to execute"
SQLResult: "Result of the SQL query"
Answer: "Final answer here"
"""

_mysql_prompt = """
You are an AI assistant that translates natural language questions into MySQL queries.
"""


from langchain.prompts import PromptTemplate

# Question è un placeholder che verrà sostituito dalla domanda dell'utente
# La risposta sarà un prompt pronto a generare una query SQL 
example_prompt = PromptTemplate(
    input_variables=["question","SQLQuery", "SQLResult", "Answer"],
    template="""

    Question: {question}
    SQLQuery: {SQLQuery}
    SQLResult: {SQLResult}
    Answer: {Answer}
    
    """
)



from langchain.prompts import FewShotPromptTemplate

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix= PROMPT_SUFFIX,
    input_variables=["input","table_info", "top_k"]
)


new_chain = SQLDatabaseToolkit(db=db, llm=llm, prompt=few_shot_prompt)

# Adesso usa sum()
db_agent = create_sql_agent(
    llm=llm,
    toolkit=new_chain,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True)


# db_agent.invoke("quanti magleitte levi di colore bianco ci sono?")

db_agent.invoke("quanto è il prezzo dell'inventario per tutte le taglie s di tshirts?")

# Ora vedo che anche le Query che prima non andavano funzionano, non ci tocca che creare
#una piccola interfaccia grafica per l'utente.

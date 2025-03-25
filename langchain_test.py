import os
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent, SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate



#importo il vettore few_shots

from shots import few_shots



def get_agent():

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




    query = """INSERT INTO t_shirts( t_shirts_id, brand_shirt, color_shirt ,size_shirt,price_shirt,stock_quantity) VALUES 

    (1, 'Van Huesen', 'Red', 'S', 15, 70),
    (2, 'Adidas', 'Black', 'XS', 17, 46),
    (3, 'Levi', 'White', 'XS', 44, 94),
    (4, 'Van Huesen', 'White', 'L', 39, 78),
    (5, 'Nike', 'Black', 'L', 31, 48),
    (6, 'Nike', 'Blue', 'XL', 38, 94),
    (7, 'Nike', 'Red', 'XL', 49, 32),
    (8, 'Levi', 'White', 'S', 13, 51),
    (9, 'Van Huesen', 'Black', 'M', 10, 83),
    (10, 'Adidas', 'Black', 'L', 49, 71),
    (11, 'Adidas', 'Blue', 'L', 34, 92),
    (12, 'Adidas', 'Red', 'L', 32, 87),
    (13, 'Nike', 'White', 'M', 29, 56),
    (14, 'Levi', 'Blue', 'S', 41, 66),
    (15, 'Van Huesen', 'Red', 'XL', 22, 49),
    (16, 'Adidas', 'White', 'M', 35, 79),
    (17, 'Nike', 'Black', 'S', 30, 72),
    (18, 'Levi', 'Red', 'XS', 47, 60),
    (19, 'Van Huesen', 'Blue', 'L', 39, 90),
    (20, 'Adidas', 'Red', 'S', 28, 84),
    (21, 'Nike', 'White', 'XL', 50, 55),
    (22, 'Levi', 'Black', 'M', 19, 73),
    (23, 'Van Huesen', 'White', 'S', 26, 64),
    (24, 'Adidas', 'Blue', 'M', 31, 82),
    (25, 'Nike', 'Red', 'L', 45, 70),
    (26, 'Levi', 'Black', 'XL', 38, 47),
    (27, 'Van Huesen', 'Blue', 'XS', 18, 95),
    (28, 'Adidas', 'White', 'L', 44, 62),
    (29, 'Nike', 'Blue', 'S', 27, 78),
    (30, 'Levi', 'Red', 'M', 36, 59)

    ON CONFLICT (t_shirts_id) DO NOTHING;"""
    results = db.run(query)

        # Stampa i risultati
    print("✅ Tabelle T-SHIRT RIEMPITA:")
    print(results)

    



    query = """INSERT INTO discount( discount_id, tshirts_id, discount_percentage) VALUES 

    (1, 1, 10.50),
    (2, 2, 5.00),
    (3, 3, 15.75),
    (4, 4, 8.00),
    (5, 5, 12.25),
    (6, 6, 20.00),
    (7, 7, 18.50),
    (8, 8, 7.75),
    (9, 9, 25.00),
    (10, 10, 30.00),
    (11, 11, 5.50),
    (12, 12, 14.00),
    (13, 13, 9.25),
    (14, 14, 22.00),
    (15, 15, 17.75),
    (16, 16, 11.50),
    (17, 17, 6.25),
    (18, 18, 13.00),
    (19, 19, 28.00),
    (20, 20, 19.75),
    (21, 21, 9.00),
    (22, 22, 16.50),
    (23, 23, 23.25),
    (24, 24, 4.75),
    (25, 25, 10.00),
    (26, 26, 21.00),
    (27, 27, 12.75),
    (28, 28, 5.25),
    (29, 29, 27.50),
    (30, 30, 8.50)

    ON CONFLICT (discount_id) DO NOTHING;"""
    results = db.run(query)

    # Stampa i risultati
    print("✅ Tabella DISCOUNT riempita:")
    print(results)


    # INIZIO A LAVORARE SUL MODELLO LLM

    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("API Key non trMostrami tutti i prodotti Nike nel database.ovata! Assicurati di impostare GEMINI_API_KEY come variabile d'ambiente.")

    # Scegli un modello disponibile per la tua API Key
    model_name = "gemini-2.0-flash-001"  

    # Inizializza il modello con LangChain
    llm = GoogleGenerativeAI(model=model_name, api_key=api_key)
    
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # db agent è qualcosa di nuovo che non ho ancora visto,
    # nelle versioni precedenti non c'era infatti molte funzioni
    # ho visto che sono state deprecate...

    # db_agent = create_sql_agent(
    # llm=llm,
    # toolkit=toolkit,
    # agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # verbose=True)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-l6-v2',
            model_kwargs={'device': 'cpu'})
    

    # Convert few_shots into strings for vectorization
    to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
    print("First vectorized example:", to_vectorize[0])

    vectorsStore = Chroma.from_texts(
    texts=to_vectorize,
    embedding=embeddings,
    metadatas=few_shots  # Ensure metadatas are dictionaries
    )

    # Initialize example selector
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorsStore,
        k=2  # Get the 2 most similar examples
    )
    selected_examples = example_selector.select_examples({"question": "Quante Tshirts Adidas sono rimaste nello store?"})

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

    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix= PROMPT_SUFFIX,
    input_variables=["input","table_info", "top_k"]
    )

    chain = SQLDatabaseToolkit(db=db, llm=llm, prompt=few_shot_prompt)

    db_agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True)
    return db_agent


# Qui è dove vado testare l'agente
# Inoltre prima di passare a Streamlit è meglio testare in questo punto 
# if __name__ == "__main__":
#     agent = get_agent()
#     agent.invoke("How many total t-shirts are left in total in stock?")

    # Adesso usa sum()
    # db_agent = create_sql_agent(
    #     llm=llm,
    #     toolkit=chain,
    #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True)
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


def clean_sql_query(query):
    """
    Rimuove eventuali backticks, blocchi di codice markdown e spazi superflui dalla query generata.
    """
    query = query.strip()  # Rimuove spazi iniziali e finali
    query = re.sub(r"```[a-zA-Z]*", "", query)  # Rimuove blocchi di codice ```sql o simili
    query = query.replace("\n", " ").strip()  # Rimuove i ritorni a capo per una query più pulita
    return query

# Definisci il prompt per generare query SQL
def generate_sql_query(richiesta):

    prompt = f"""
    You are an expert of SQL. Generate a valid SQL query for PostgresSQL referring to richiesta:
    Request: {richiesta}
    The query must be syntactically correct and optimized.
    """   
    response = llm.invoke(prompt)
    return clean_sql_query(response)
    # return response.strip()  # Rimuove spazi bianchi superflui

# Esegui una query generata da Gemini

def run_generated_query(domanda):

    sql_query = generate_sql_query(domanda)
    print(f"\n🟢 Query generata:\n{sql_query}\n")
    try:
        result = db.run(sql_query)
        print("Risultato della query:")
        print(result)
    except Exception as e:
        print(f"Errore durante l'esecuzione della query: {e}")



if not api_key:
    raise ValueError("API Key non trMostrami tutti i prodotti Nike nel database.ovata! Assicurati di impostare GEMINI_API_KEY come variabile d'ambiente.")

# Scegli un modello disponibile per la tua API Key
model_name = "gemini-2.0-flash-001"  

# Inizializza il modello con LangChain
llm = GoogleGenerativeAI(model=model_name, api_key=api_key)




# Esegui il codice con una domanda

# Questa mi cercherà dalla tabella producst che non esiste nel mio caso, quindi devo gestirlo
# user_input = "Show me all the products Nike in the database"

user_input = "Show me all the products Nike in the database from the table t_shirts e la colonna è brand_shirt"
run_generated_query(user_input)















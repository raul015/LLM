# La prima cosa che faccio è collegarmi con POSTGRESQL TRAMITE PYTHON
import psycopg2
import os

# Per non rendere visibili i miei dati sullo script 
# connection = psycopg2.connect(host="localhost",
#                                dbname= "LLMDatabase",
#                                  user ="postgres",
#                                  password="unibg",
#                                  port=5432)

# # 
# fare gli export delle seguenti variabili, consigliato fare un file.sh
connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
# Per eseguire i comandi
cursor = connection.cursor()


# Creazione della tabella t_shirts 
cursor.execute(""" CREATE TABLE IF NOT EXISTS t_shirts (
    t_shirts_id SERIAL PRIMARY KEY,
    brand_shirt TEXT CHECK (brand_shirt IN ('Van Huesen', 'Levi', 'Nike', 'Adidas')) NOT NULL,
    color_shirt TEXT CHECK (color_shirt IN ('Red', 'Blue', 'Black', 'White')) NOT NULL,
    size_shirt TEXT CHECK (size_shirt IN ('XS', 'S', 'M', 'L', 'XL')) NOT NULL,
    price_shirt INT CHECK (price_shirt BETWEEN 10 AND 50),
    stock_quantity INT NOT NULL,
    CONSTRAINT unique_brand_color_size UNIQUE (brand_shirt, color_shirt, size_shirt)
    );
""")


# Creazione della tabella discount
cursor.execute("""CREATE TABLE IF NOT EXISTS  discount(
    discount_id SERIAL PRIMARY KEY,
    tshirts_id INT NOT NULL,
    discount_percentage DECIMAL(5,2) CHECK (discount_percentage BETWEEN 0 AND 100)
    );
""")

# SELECT * FROM t_shirts  --< per vedere i campi del DB da fare su postgres


# Adesso riempo il database 


# STO RIEMPENDO IL DATABASE DELLE TSHIR 
cursor.execute(""" INSERT INTO t_shirts( t_shirts_id, brand_shirt, color_shirt ,size_shirt,price_shirt,stock_quantity) VALUES 

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

ON CONFLICT (t_shirts_id) DO NOTHING;

""")

# Adesso riempo anche il DB dei discount 

cursor.execute(""" INSERT INTO discount( discount_id, tshirts_id, discount_percentage) VALUES 

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

ON CONFLICT (discount_id) DO NOTHING;

"""
)

api_key = os.getenv("GOOGLE_API_KEY")

# PRIMO METODO PER UTILIZZARE LE API DI GOOGLE PALM PER IL MODELL OGEMINI 
import requests
import json 



if not api_key:
    raise ValueError("API Key non trovata! Assicurati di impostare GEMINI_API_KEY come variabile d'ambiente.")

# Scegli un modello disponibile per la tua API Key
#model_name = "gemini-1.5-flash"  # Prova anche con "gemini-2.0-flash-001"

model_name = "gemini-2.0-flash-001"
# URL API per la richiesta
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"


# Corpo della richiesta JSON
data = {
    "contents": [{
        "parts": [{"text": "Explain how AI works"}]  # Modifica il prompt qui
    }]
}

response = requests.post(api_url, headers={"Content-Type": "application/json"}, json=data)


# Controlla la risposta
if response.status_code == 200:
    result = response.json()
    print("✅ Risposta AI:")
    print(json.dumps(result, indent=4))  # Stampa il risultato in formato leggibile
else:
    print(f" Errore {response.status_code}: {response.text}")




# Faccio qualcosa 
connection.commit()
cursor.close()
connection.close()




    
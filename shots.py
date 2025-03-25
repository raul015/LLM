
few_shots = [  
    {
         'Question': "Quante t-shirt Nike di colore white ho disponibili?",
         'SQLQuery':  "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand_shirt = 'Nike' AND color_shirt = 'White'",
         'SQLResult': "Result of the SQL query",
         'Answer': "111"  # Convert integer to string
    },
    {
         'Question': "Il prezzo totale delle tshirts con taglia S?",
         'SQLQuery':  "SELECT SUM(price_shirt*stock_quantity) FROM t_shirts WHERE size_shirt = 'S' ",
         'SQLResult': "Result of the SQL query",
         'Answer': "12701"  # Convert integer to string
    }
]

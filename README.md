# LLM
A test on the potential of LLM


## Setup key Google Palm
-   Entrare con il proprio account dentro aistudio(MakerSuite)
-   Creare una API Key (la genera per il modello gemini)

## Ambiente virtuale 
Per non avere problemi con le dipendeze di python, creare un ambiente virtuale: python3 -m venv myenv   (per esempio)
Successivamente prima di runnare il codice python ricordarsi di fare source myenv/bin/activate 
Nel mio caso ho craeto un altro file .sh che ho chiamato source.sh

## Dipendenza Python
pip install -r requirements.txt

## Variabili d'ambiente 
Per non rendere disponibile i miei dati ho creato un file .sh che contiene i seguenti campi:
-   export DB_HOST=""
-   export DB_NAME=""
-   export DB_USER=""
-   export DB_PASSWORD=""
-   export DB_PORT=""
-   export GOOGLE_API_KEY=""
Riempire i campi con i propri dati e successivamente da terminale fare . file.sh 

## generale
Mi collego ad un database locale con postgres ed allo stesso tempo faccio un setup del modell MLL tramite API_KEY

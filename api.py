# Importation des modules
from fastapi import FastAPI
from locust import HttpUser, task, between
import requests
import uvicorn

# Initialisation de l'application
app = FastAPI()
# Lien de l'API
hostAPI = "https://labonnealternance.apprentissage.beta.gouv.fr/api/V1/"
# code ROME
code_rome = "M1805"

# Récupération des formations en fonction du code ROME
@app.get('/formations/{ROME}')
async def get_formations(ROME: str):
    response = requests.get(hostAPI + "formations?romes=" + ROME + "&caller=contact%40domaine%20nom_de_societe")
    return response.json()

# Récupération des métiers en fonction du code ROME
@app.get('/metiers/{ROME}')
async def get_metiers(ROME: str):
    response = requests.get(hostAPI + "metiers?romes=" + ROME)
    return response.json()

# Tests de l'API
class WebsiteUser(HttpUser):
    wait_time=between(1,5)
    @task
    def metiers(self):
        self.client.get(url="/metiers/"+code_rome)
    @task
    def formations(self):
        self.client.get(url="/formations/"+code_rome)

# Lancement de l'application
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
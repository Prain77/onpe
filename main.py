from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"ok": True, "mensaje": "API ONPE funcionando"}

@app.get("/onpe/presidente")
def presidente():
    return {
        "ok": True,
        "tipo": "Presidente",
        "mensaje": "Aquí luego irá el scraping ONPE"
    }

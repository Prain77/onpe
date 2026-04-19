from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import traceback

app = FastAPI()

URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/mesa/totales?tipoFiltro=eleccion"
URL_VOTOS = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/eleccion-presidencial/participantes-ubicacion-geografica-nombre?idEleccion=10&tipoFiltro=eleccion"

def fetch_json_with_browser(url: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()

            response_holder = {"json": None}

            def handle_response(response):
                if response.url == url:
                    try:
                        response_holder["json"] = response.json()
                    except Exception:
                        pass

            page.on("response", handle_response)
            page.goto(url, wait_until="networkidle", timeout=60000)

            if response_holder["json"] is None:
                content = page.content()
                browser.close()
                return {
                    "ok": False,
                    "mensaje": "No se pudo leer JSON",
                    "respuesta_html_inicio": content[:500]
                }

            browser.close()
            return {
                "ok": True,
                "data": response_holder["json"]
            }

    except Exception as e:
        return {
            "ok": False,
            "mensaje": str(e),
            "trace": traceback.format_exc()
        }

@app.get("/")
def home():
    return {"ok": True, "mensaje": "API ONPE funcionando"}

@app.get("/onpe/presidente")
def presidente():
    cabecera = fetch_json_with_browser(URL_TOTALES)
    votos = fetch_json_with_browser(URL_VOTOS)

    return {
        "ok": cabecera.get("ok") and votos.get("ok"),
        "tipo": "Presidente",
        "cabecera": cabecera,
        "votos": votos
    }

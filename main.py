import os
from src.search_tool import MecanismoBusca
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path=".env")

# Acessar APIS
SERPPAPI_API_KEY = os.getenv("SERPAPI_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


buscador = MecanismoBusca(SERPPAPI_API_KEY)
resultados_serpapi = buscador.serpapi_search("Hospital João XXIII")
for i in resultados_serpapi:
    print(i)

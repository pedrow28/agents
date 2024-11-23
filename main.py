import os
from src.search_tool import MecanismoBusca
from src.agents import CuradorConteudo
from dotenv import load_dotenv
import warnings
from langchain.globals import set_verbose

# Suprimir avisos específicos
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Desativar a verbosidade do LangChain
set_verbose(False)

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path=".env")

# Acessar APIS
SERPPAPI_API_KEY = os.getenv("SERPAPI_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

## Buscando no google
buscador = MecanismoBusca(SERPPAPI_API_KEY)
resultados = buscador.serpapi_search("Hospital João XXIII")


## Curadoria

curador = CuradorConteudo(OPENAI_API_KEY)

conteudo_curado = curador.curar_conteudo(resultados)

## Resultado

for item in conteudo_curado:
    print(f"Snippet: {item['snippet']}")
    print(f"Avaliação: {item['avaliacao']}\n")

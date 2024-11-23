import httpx
import pandas as pd
import os
import json
from typing import Dict, List, Any
from serpapi import GoogleSearch

class MecanismoBusca:


    def __init__(self, api_key: Dict):
        """
        Inicializa um objeto MecanismoBusca com os parâmetros da pesquisa
        
        Parameters
        ----------
        params : Dict
            Dicionário com os parâmetros da pesquisa. Deve conter a chave "api_key" com a chave da API do Google Books.
        """
        self.key = api_key
        self.search_engine_id = "google"
        # Parametros pesquisa
        

    def serpapi_search(self, query, **kwargs):
        """
        Faz uma pesquisa no SerpAPI com os parâmetros especificados.
        
        Parameters
        ----------
        query : str
            Termo de busca.
        **kwargs
            Parâmetros adicionais para a pesquisa.
            
        Returns
        -------
        List[Dict]
            Resultados da pesquisa.
        """

        params = {
            "key": self.key,
            "cx": self.search_engine_id,
            "q": query,
            "tbm":"nws",
            "tbs":"qdr:d",
            **kwargs
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        snippets = [item['snippet'] for item in results['news_results']]
        return snippets
    

    def google_search(self, query, **kwargs):
        base_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.key,
            "cx": self.search_engine_id,
            "q": query,
            "tbs":"qdr:d",
            **kwargs
        }

        response = httpx.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
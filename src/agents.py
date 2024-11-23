from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOpenAI

class CuradorConteudo:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(openai_api_key=api_key)
        self.agente = self.criar_agente()

    def criar_agente(self):
        return Agent(
            role='Curador de Conteúdo',
            goal='Analisar e selecionar conteúdo relevante sobre o Hospital João XXIII',
            backstory="""Você é um especialista em análise de mídia e comunicação em saúde. 
            Sua tarefa é avaliar notícias e menções sobre o Hospital João XXIII, 
            identificando informações relevantes e impactantes para a reputação e 
            operações do hospital.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def avaliar_relevancia(self, snippet):
        task = Task(
            description=f"""Analise o seguinte snippet de notícia e determine sua relevância 
            para um relatório sobre o Hospital João XXIII. Considere os seguintes critérios:
            1. Menção direta ao Hospital João XXIII
            2. Impacto na reputação do hospital
            3. Informações sobre serviços ou operações do hospital
            4. Eventos ou incidentes relacionados ao hospital
            
            Snippet: {snippet}
            
            Retorne uma avaliação no formato:
            Relevância: [Alta/Média/Baixa]
            Justificativa: [Breve explicação da sua avaliação]
            """,
            agent=self.agente,
            expected_output="Uma avaliação da relevância do snippet com justificativa."
        )
        crew = Crew(
            agents=[self.agente],
            tasks=[task],
            verbose=True
        )
        result = crew.kickoff()
        return result

    def curar_conteudo(self, snippets):
        conteudo_curado = []
        for snippet in snippets:
            avaliacao = self.avaliar_relevancia(snippet)
            if "Relevância: Alta" in avaliacao or "Relevância: Média" in avaliacao:
                conteudo_curado.append({
                    'snippet': snippet,
                    'avaliacao': avaliacao
                })
        return conteudo_curado
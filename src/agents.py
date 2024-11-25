from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOpenAI
from crewai_tools import WebsiteSearchTool



class CuradorConteudo:
    def __init__(self, api_key):
        self.llm = ChatOpenAI(openai_api_key=api_key)
        #self.agente = self.criar_agente()

    def criar_extrator_url(self, tool):
        return Agent(
            role='Extrator de URL',
            goal='Extrair íntegra do conteúdo de notícias',
            backstory="""Você é um agente especializado em extrair
            o conteúdo de URLs para repassar para um curadoria. Você deve extrair todo o 
            conteúdo relacionado à notícia veiculada na URL, e esse texto deve ser extraído e organizado
            para ser repassado para o Curador de Conteúdo.""",
            tools=[tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def criar_agente_curador(self):
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

    def avaliar_relevancia(self, url):

        tool = WebsiteSearchTool(url)

        agent_url = self.criar_extrator_url(tool)

        agent_curador = self.criar_agente_curador()

        task_url = Task(
            description=f"""A partir da URL recebida, acesse o endereço
            e extraia todo o conteúdo da notícia veiculada na URL.
            
            URL: {url}
            
            Retorne o texto formatado de forma a facilitar a task de curadoria.
            """,
            agent=agent_url,
            expected_output="Um texto com o conteúdo completo da notícia veiculada na URL."
        )

        task_curadoria = Task(
            description=f"""Analise a notícia recebida e determine sua relevância 
            para um relatório sobre o Hospital João XXIII. Considere os seguintes critérios:
            1. Menção direta ao Hospital João XXIII
            2. Impacto na reputação do hospital
            3. Informações sobre serviços ou operações do hospital
            4. Eventos ou incidentes relacionados ao hospital
            
            Retorne uma avaliação no formato:
            Relevância: [Alta/Média/Baixa]
            Justificativa: [Breve explicação da sua avaliação]
            """,
            agent=agent_curador,
            expected_output="Uma avaliação da relevância da notícia com justificativa.",
            context=[task_url]
        )
        crew = Crew(
            agents=[agent_url, agent_curador],
            tasks=[task_url, task_curadoria],
            verbose=True
        )
        result = crew.kickoff()
        return result

    def curar_conteudo(self, urls):
        conteudo_curado = []
        for url in urls:
            avaliacao = self.avaliar_relevancia(url)
            if "Relevância: Alta" in avaliacao or "Relevância: Média" in avaliacao:
                conteudo_curado.append({
                    'URL': url,
                    'avaliacao': avaliacao
                })
        return conteudo_curado
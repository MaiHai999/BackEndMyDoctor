from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LoadLLM:
    def __init__(self , base_url = "http://192.168.1.14:9999/v1" , temperature = 0.7):
        self.llm = ChatOpenAI(
            base_url = base_url,
            temperature = temperature,
            api_key="not-needed"
        )

        self.output_parser = StrOutputParser()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system","Your name is Safa.Please create the correct answer. The answer must be Vietnamese"),
            ("user", "{input}")
        ])

    def customPrompt(self , message):
        self.prompt = ChatPromptTemplate.from_messages(message)

    def customOutput(self):
        self.output_parser = StrOutputParser()

    def CreatChain(self):
        chain = self.prompt | self.llm | self.output_parser
        return chain



if __name__ == "__main__":
    llm = LoadLLM()
    chain = llm.CreatChain()

    for chunk in chain.stream({"input" : "Bệnh tiểu đường là gì"}):
        print(chunk, end="", flush=True)
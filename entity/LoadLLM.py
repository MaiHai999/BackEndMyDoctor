from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LoadLLM:
    def __init__(self , base_url , temperature = 0.5):
        self.llm = ChatOpenAI(
            base_url = base_url,
            temperature = temperature,
            api_key="not-needed"
        )

        self.output_parser = StrOutputParser()
        self.prompt = None

    def setPrompt(self , message):
        self.prompt = ChatPromptTemplate.from_messages(message)

    def setOutput(self):
        self.output_parser = StrOutputParser()

    def CreatChain(self):
        chain = self.prompt | self.llm | self.output_parser
        return chain



if __name__ == "__main__":
    llm = LoadLLM()
    prompt_general = [
        ("system", "Bạn tên là Safa. Bạn là trợ lý ảo chỉ cung cấp các thông tin về y tế."),
        ("user", "{input}")
    ]
    llm.setPrompt(prompt_general)

    chain = llm.CreatChain()

    for chunk in chain.stream({"input" : "Bệnh tiểu đường là gì"}):
        print(chunk, end="", flush=True)
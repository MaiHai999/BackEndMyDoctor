from langchain.schema import StrOutputParser



class BuildChain:
    @staticmethod
    def build_simple_chain(llm , prompt):
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        return chain
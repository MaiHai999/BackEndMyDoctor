from BackEnd.source.entity.LoadVectorDB import LoadVectorDB
from BackEnd.source.entity.LoadLLM import LoadLLM
from underthesea import classify
from translate import Translator
from langchain_core.prompts import ChatPromptTemplate


class LLMController:
    def __init__(self):
        self.db = LoadVectorDB()
        self.loadLLM = LoadLLM()
        self.translator = Translator(to_lang="en", from_lang="vi")

    def check_text(self , text):
        result = classify(text)
        return 'suc_khoe' == result[0]

    def query_message(self , message):
        if self.check_text(message):
            translated_text = self.translator.translate(message)
            list_of_context = self.db.querying(translated_text , k=2)
            context = ' '.join(list_of_context)

        else:
            pass


if __name__ == "__main__":
    LmController = LLMController()
    LmController.query_message("Làm sao để hết bệnh đau đầu ?")






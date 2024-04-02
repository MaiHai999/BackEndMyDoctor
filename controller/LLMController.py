from BackEnd.source.entity.LoadVectorDB import LoadVectorDB
from BackEnd.source.entity.LoadLLM import LoadLLM
from underthesea import classify
from translate import Translator
from langchain_core.prompts import ChatPromptTemplate

import threading
stop_event = threading.Event()



class LLMController:
    def __init__(self,url):
        self.db = LoadVectorDB()
        self.loadLLM = LoadLLM(base_url=url)
        self.translator = Translator(to_lang="en", from_lang="vi")

        prompt_healthy = [
            ("system", "Bạn tên là Safa. Bạn là trợ lý ảo chỉ cung cấp các thông tin về y tế. "
                       "Phàn hồi của bạn có thể dựa trên ngữ cảnh này nhé:{context}"),
            ("user", "{input}")
        ]
        self.loadLLM.setPrompt(prompt_healthy)
        self.chain_main = self.loadLLM.CreatChain()

        prompt_general = [
            ("system", "Bạn tên là Safa. Bạn là trợ lý ảo chỉ cung cấp các thông tin về y tế."),
            ("user", "{input}")
        ]
        self.loadLLM.setPrompt(prompt_general)
        self.chain_general = self.loadLLM.CreatChain()

    def check_text(self , text):
        result = classify(text)
        return 'suc_khoe' == result[0]

    def query_message(self , message):
        stop_event.clear()
        if self.check_text(message):
            translated_text = self.translator.translate(message)
            list_of_context = self.db.querying(translated_text , k=2)
            context = ' '.join(list_of_context)
            for chunk in self.chain_main.stream({"input": message, "context" : context}):
                if not stop_event.is_set():
                    yield chunk
                else:
                    raise Exception("Hàm đã bị huỷ.")

        else:
            for chunk in self.chain_general.stream({"input": message}):
                if not stop_event.is_set():
                    yield chunk
                else:
                    raise Exception("Hàm đã bị huỷ.")

    def stop(self):
        stop_event.set()


if __name__ == "__main__":
    base_url = "http://192.168.1.7:9999/v1"
    LmController = LLMController(base_url)
    while True:
        message = input("Prompt message: ")
        print("Bot:" , end=" ")
        LmController.query_message(message)
        print("\n")






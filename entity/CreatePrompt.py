from langchain.prompts import PromptTemplate


class CreatePrompt:
    @staticmethod
    def creat_prompt_VinaLLaMA():
        template = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
            {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        return prompt

    @staticmethod
    def creat_prompt(template , variables):
        prompt = PromptTemplate(template=template, input_variables=variables)
        return prompt




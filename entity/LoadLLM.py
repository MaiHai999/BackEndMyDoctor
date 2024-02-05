from langchain_community.llms import CTransformers
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

class LoadModel:

    @staticmethod
    def load_ctransformers(path ,model_type="llama" , max_new_tokens = 1024, temperature=0.01 ):
        llm = CTransformers(
            model = path,
            model_type = model_type,
            max_new_tokens = max_new_tokens,
            temperature = temperature
        )

        return llm

    @staticmethod
    def load_llm_huggingface(path , gpu = -1 , accelerate = False , max_new_tokens = 1024):
        if accelerate is False:
            llm = HuggingFacePipeline.from_model_id(
                model_id = path,
                task="text-generation",
                device = gpu,
                pipeline_kwargs={"max_new_tokens": max_new_tokens},
            )
            return llm

        else:
            gpu_llm = HuggingFacePipeline.from_model_id(
                model_id= path,
                task="text-generation",
                device_map="auto",  # replace with device_map="auto" to use the accelerate library.
                pipeline_kwargs={"max_new_tokens": max_new_tokens},
            )
            return gpu_llm



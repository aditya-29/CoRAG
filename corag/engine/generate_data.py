from .. import Prompts
from .. import Task
from .. import BaseChat

class GenerateData:
    def __init__(self, model: BaseChat, task: Task):
        self.model = model
        self.task = task
        self.task_description = task.get_description()


    def _generate_sub_query(self, query: str, interim_qa: dict = None) -> str:
        sub_query_prompt = Prompts.SUB_QUERY_GENERATION

        formatted_interim_qa = []
        for i, (key, value) in interim_qa.items():
            temp = f"Intermediate Question {str(i)}:\n"
            temp += key
            temp += f"\nAnswer: {value}"

        sub_query_prompt = sub_query_prompt.format(intermediate_queries_and_answers = interim_qa,
                                                   task_description = self.task_description,
                                                   query = query)
        
        model_input = {
            "user" : [sub_query_prompt]
        }

        output = self.model.chat(chat_inputs = model_input, raw_output=False, logprobs=None)
        return output
    
    def _generate_sub_answer(self, retrieved_docs: list, sub_query: str) -> str:
        sub_answer_prompt = Prompts.INTER_ANS_GENERATION

        formatted_retrieved_documents = []
        for i, doc in enumerate(retrieved_docs):
            temp = f"Document {str(i)}:\n"
            temp += doc
            formatted_retrieved_documents.append(temp)
        
        formatted_retrieved_documents = "\n\n".join(formatted_retrieved_documents)

        sub_answer_prompt = sub_answer_prompt.format(retrieved_documents = formatted_retrieved_documents,
                                                     sub_query = sub_query)
        
        model_input = {
            "user" : [sub_answer_prompt]
        }
        output = self.model.chat(chat_inputs=model_input, raw_output=False, logprobs=None)
        return output
        
    def _generate_final_answer(self, 
                               retrieved_docs:list, 
                               interim_qa: dict,
                               query: str) -> str:
        

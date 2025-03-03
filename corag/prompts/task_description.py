class Task:
    def __init__(self, task):
        self.task_map = {
            ("HotpotQA", "2WikiMulti-hopQA")        : "answer multi-hop questions", 
            ("NQ")                                  : "answer natural questions from google search",
            ("AidaYago 2", "WnWi", "WnCw", "Blink") : "link the mention surrounded by [START_ENT] and [END_ENT] to the title of the correct Wikipedia page",
            ("FEVER")                               : "verify if the claim is supported or refuted",
            ("T-REx", "Zero-Shot RE")               : "given head entity and relation seperated by [SEP], find the correct tail entity, return the title of its Wikipedia page",
            ("Trivia QA")                           : "answer the trivia questions",
            ("MuSiQue", "Bamboogle")                : "answer multi-hop questions"
        }

        self.task = task

    def get_description(self):
        for k, v in self.taks_map.items():
            if self.task in k:
                return v
            
        print("[INFO] Direct match not found, checking closest match")
        # if exact match not found, try closest match
        task = ''.join(char for char in self.task if char.isalnum())
        task = task.lower()

        for k, v in self.taks_map.items():
            if task in k:
                return v
        
        raise Exception("Task not found")
    
        





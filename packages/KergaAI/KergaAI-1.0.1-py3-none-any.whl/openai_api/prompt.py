class PROMPTS:
    ENCLOSE = "Enclose your answers between '#stj' and '#enj'."
    JSON = "Write your answer in a JSON compatible format."
    EN = "Answer in english."
    FR = "Answer in french."

    @staticmethod
    def get_dict():
        m = "Write a dictionnary mapping 3 words in english to their french translation."
        return " ".join([m, PROMPTS.ENCLOSE, PROMPTS.JSON])
    
    @staticmethod
    def get_text():
        m = "Tell me a story in 3 sentences."
        return " ".join([m, PROMPTS.FR])

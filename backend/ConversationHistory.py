class ConversationHistory:

   

    def __init__(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        self.total_estimated_cost = 0

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message):
        self.messages.append({"role": "assistant", "content": message})

    def get_messages(self):
        return self.messages
    
    #let's add setter and getter for total_estimated_cost
    def set_total_estimated_cost(self, cost):
        self.total_estimated_cost = cost

    def get_total_estimated_cost(self):
        return self.total_estimated_cost
    
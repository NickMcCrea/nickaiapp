

class UserSessionState:

    app_state = "Default"

    current_data_pipeline = None
   

    def __init__(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        self.messages.append({"role": "system", "content": "You are helping the user explore data sets, and answer questions about them."})
        self.messages.append({"role": "system", "content": "You can answer questions about what data is available, and also help the user explore the data."})
        self.messages.append({"role": "system", "content": "If the user tries to talk about other topics, gently explain what your purpose is."})

        self.last_executed_query = ""
        
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
    
    def set_last_executed_query(self, query):
        self.last_executed_query = query

    def get_last_executed_query(self):
        return self.last_executed_query
    
    def get_app_state(self):
        return self.app_state
    
    def set_app_state(self, state):
        self.app_state = state

    def get_current_data_pipeline(self):
        return self.current_data_pipeline
    
    def set_current_data_pipeline(self, pipeline):
        self.current_data_pipeline = pipeline
    

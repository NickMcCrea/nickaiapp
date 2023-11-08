def build_basic_message_list(prompt):
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.append({"role": "system", "content": "You are helping the user explore data sets, and answer questions about them."}) 
        messages.append({"role": "user", "content": prompt})
        return messages


def build_data_analysis_prompt(convo_history, user_input, data_str):
    return f"""
        Given the following data:
        {data_str}
        And the previous conversation history:
        {convo_history.messages}
        and the user's input:
        {user_input}
        Please very briefly comment on the data, given the context. Provide any analysis you think is relevant. Keep it to a couple hnundred words or less.
        When commenting on the data, stick to insights gleaned from the data, rather than the structure or schema of the data itself.
        """


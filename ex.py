import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables from .env file
load_dotenv()

# 1. Initialize the Large Language Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 2. Define the Chat Prompt with room for conversational history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and witty AI assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 3. Chain the prompt and the model together using LCEL
chain = prompt | model

# 4. Set up an in-memory dictionary to manage session state
session_store = {}

def get_session_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

# 5. Wrap the chain with message history functionality
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# 6. Run the terminal loop
def start_chat():
    print("🤖 Chatbot initialized! Type 'exit' or 'quit' to end the conversation.\n")
    config = {"configurable": {"session_id": "user_session_1"}}
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        # Stream or invoke the response
        response = conversational_chain.invoke(
            {"input": user_input},
            config=config
        )
        print(f"Chatbot: {response.content}\n")

if __name__ == "__main__":
    start_chat()

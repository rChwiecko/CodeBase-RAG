import os
import streamlit as st
from dotenv import load_dotenv
from codebase_rag_completed import perform_rag_with_namespace, add_repo_to_pinecone  # Import necessary functions

# Load environment variables
load_dotenv()

# Default namespace
DEFAULT_NAMESPACE = "https://github.com/CoderAgent/SecureAgent"

# Initialize session state for namespace
if "namespace" not in st.session_state:
    st.session_state.namespace = DEFAULT_NAMESPACE

# Utility function to list repositories in the content directory
def list_repositories():
    """Lists all repositories in the 'content' directory."""
    content_dir = "./content"
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)
    return [d for d in os.listdir(content_dir) if os.path.isdir(os.path.join(content_dir, d))]

# Streamlit UI with tabs
st.title("Codebase RAG Chatbot")
tab1, tab2 = st.tabs(["Select Repo", "Chat"])

# Tab 1: Select Repository
with tab1:
    st.header("Select a Repository")

    # Dropdown menu for existing repositories
    existing_repos = list_repositories()
    selected_repo = st.selectbox("Select an existing repository:", [""] + existing_repos)

    # Text input for a new repository URL
    repo_url = st.text_input("Or enter a new repository URL to clone:")

    # Confirm button to select or clone repository
    if st.button("Select or Clone Repository"):
        if repo_url.strip():
            # Clone and add repository to Pinecone
            try:
                st.info(f"Cloning repository: {repo_url}")
                namespace = add_repo_to_pinecone(repo_url.strip())  # Add repo to Pinecone
                st.session_state.namespace = namespace  # Persist the namespace in session state
                st.success(f"Repository cloned and indexed successfully: {repo_url}")
            except Exception as e:
                st.error(f"Error cloning repository: {e}")
        elif selected_repo:
            # Use existing repository
            st.session_state.namespace = f"https://github.com/CoderAgent/{selected_repo}"
            st.success(f"Switched to existing repository: {selected_repo}")
        else:
            st.warning("Please select a repository or enter a new repository URL.")

    st.write(f"Currently using namespace: {st.session_state.namespace}")

# Tab 2: Chat
with tab2:
    st.header("Chat with the Codebase")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []  # To store the conversation history

    # Button to clear chat history
    if st.button("Clear Chat"):
        st.session_state.messages = []  # Clear the messages session state
        st.success("Chat cleared successfully!")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input box for the user query
    user_input = st.chat_input("Enter your question here...")

    if user_input:
        # Add user's input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user's message in the chat
        with st.chat_message("user"):
            st.write(user_input)

        # Perform RAG and display the response
        with st.spinner("Thinking..."):
            try:
                # Call the RAG function with the current namespace
                response = perform_rag_with_namespace(user_input, st.session_state.namespace)
            except Exception as e:
                response = f"An error occurred: {e}"

        # Add model's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display model's response in the chat
        with st.chat_message("assistant"):
            st.write(response)

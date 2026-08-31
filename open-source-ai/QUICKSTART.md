# Open Source AI - Quickstart Guide

Get up and running with open-source AI tools in minutes.

## ⚡ 5-Minute Setup (Choose One)

### Option 1: Local LLM with Ollama (Easiest)

```bash
# Install Ollama
# Windows: Download from https://ollama.ai
# Mac/Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# Pull and run a model
ollama pull llama3.2
ollama run llama3.2
```

### Option 2: RAG with Chroma + LangChain

```bash
pip install langchain langchain-community chromadb openai

python -c "
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load and split documents
loader = TextLoader('your_doc.txt')
docs = loader.load()
splits = CharacterTextSplitter(chunk_size=1000).split_documents(docs)

# Create vector store
vectordb = Chroma.from_documents(splits, OpenAIEmbeddings())
print(f'Indexed {len(splits)} chunks')
"
```

### Option 3: Agent with LangGraph

```bash
pip install langgraph langchain-openai

python -c "
from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

model = ChatOpenAI(model='gpt-4o-mini')

def chatbot(state: MessagesState):
    return {'messages': [model.invoke(state['messages'])]}

graph = StateGraph(MessagesState)
graph.add_node('agent', chatbot)
graph.set_entry_point('agent')
app = graph.compile()
print('Agent ready!')
"
```

---

## 🎯 Stack Recommendations by Use Case

### Chatbot / Customer Support
- **LLM**: Ollama + Llama 3.2
- **Framework**: LangChain
- **Storage**: ChromaDB
- **Observability**: Langfuse

### Document Q&A / RAG
- **LLM**: OpenAI or Anthropic
- **Framework**: LlamaIndex
- **Vector DB**: Qdrant or Pinecone
- **Evaluation**: Ragas

### Multi-Agent System
- **Framework**: AutoGen or CrewAI
- **Orchestration**: LangGraph
- **Memory**: Redis
- **Monitoring**: Arize Phoenix

### Enterprise Production
- **Serving**: vLLM or TGI
- **Orchestration**: Kubernetes + Ray Serve
- **Feature Store**: Feast
- **MLOps**: MLflow + Kubeflow

---

## 💻 Code Examples

### Example 1: Simple Chatbot

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
]

response = llm.invoke(messages)
print(response.content)
```

### Example 2: RAG Pipeline

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Setup vector store
vectorstore = Chroma.from_texts(
    ["Paris is the capital of France", "Berlin is the capital of Germany"],
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# Create RAG chain
template = """Answer based on context: {context} Question: {question}"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o-mini")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke("What is the capital of France?"))
```

### Example 3: Simple Agent

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny, 25°C in {city}"

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_react_agent(llm, [get_weather])

result = agent.invoke({"messages": [("user", "Weather in Tokyo?")]})
print(result["messages"][-1].content)
```

---

## 📅 4-Week Learning Path

### Week 1: Foundations
- [ ] Set up Ollama and run local models
- [ ] Build first chatbot with LangChain
- [ ] Understand prompts and chains
- [ ] Complete: Simple Q&A bot

### Week 2: RAG & Vector DBs
- [ ] Learn embedding concepts
- [ ] Set up ChromaDB or Qdrant
- [ ] Build document Q&A system
- [ ] Complete: PDF reader with RAG

### Week 3: Agents & Tools
- [ ] Understand ReAct pattern
- [ ] Build agent with tool use
- [ ] Explore multi-agent frameworks
- [ ] Complete: Research assistant agent

### Week 4: Production
- [ ] Add evaluation with Ragas/DeepEval
- [ ] Implement observability (Langfuse/Phoenix)
- [ ] Deploy with Docker
- [ ] Complete: Production-ready chatbot

---

## 🔧 Common Issues & Solutions

### Issue: Ollama won't start
```bash
# Check if port is in use
lsof -i :11434

# Kill existing process
pkill ollama

# Restart
ollama serve
```

### Issue: ChromaDB import error
```bash
# Reinstall with dependencies
pip uninstall chromadb
pip install chromadb
```

### Issue: OpenAI rate limits
```python
# Use retries and backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_with_retry():
    return llm.invoke(messages)
```

### Issue: Memory issues with large documents
```python
# Use smaller chunks and batching
text_splitter = CharacterTextSplitter(
    chunk_size=500,  # Reduce from 1000
    chunk_overlap=50
)

# Process in batches
for i in range(0, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    vectorstore.add_documents(batch)
```

### Issue: Slow vector search
```python
# Use HNSW index for faster search
vectordb = Chroma.from_documents(
    docs,
    embedding,
    collection_metadata={"hnsw:space": "cosine"}
)
```

---

## 📚 Next Steps

1. Explore the [main README](README.md) for all available tools
2. Join our [community discussions](https://github.com/your-org/open-source-ai/discussions)
3. Check out the [examples](./examples) folder for more code samples

---

## Need Help?

- Open an issue on GitHub
- Check tool documentation (linked in README)
- Join Discord communities listed in README

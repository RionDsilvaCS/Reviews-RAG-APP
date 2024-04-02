from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

class ResponseChain():
    def __init__(self) -> None:
        
        self.embeddings = HuggingFaceEmbeddings()
        self.main_db = FAISS.load_local("../DB/main_db", self.embeddings, allow_dangerous_deserialization=True)
        self.retriever = self.main_db.as_retriever(search_kwargs={"k": 10})
        self.llm = Ollama(model="llama2", base_url="http://localhost:11434")
        self.template = """
            Your task is to analyze the reviews of books sold online.
            Get the book name and author name from the context provided. 
            Answer the question based only on the following context:
            {context}"

            Don't respond with duplicate data.
            Question: {question}
            """

        self.prompt = ChatPromptTemplate.from_template(self.template)

        self.chain = (
                {"context": self.retriever, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm.invoke
                | StrOutputParser()
            )
        
    def get_response(self, question):
        return self.chain.invoke(question)
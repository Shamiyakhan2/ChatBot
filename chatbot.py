from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from retrieval import build_vectorstore
from utils import load_rules


def get_chatbot():
    # Load HuggingFace model
    model_name = "google/flan-t5-small"
    pipe = pipeline("text2text-generation", model=model_name, max_length=512)
    llm = HuggingFacePipeline(pipeline=pipe)

    # Build vectorstore
    vectordb = build_vectorstore()

    # If no vector database found, fallback mode
    if vectordb is None:
        def simple_qa(question):
            return "I couldn't access my knowledge base, but generally speaking, nutrition is important for health."
        return simple_qa

    # Create retriever
    retriever = vectordb.as_retriever()

    # Prompt for answering
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a nutrition expert.\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer:"
        )
    )

    # Build modern Runnable retrieval chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain




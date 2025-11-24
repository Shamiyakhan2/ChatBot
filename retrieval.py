from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_vectorstore():
    try:
        # ✅ Simple embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # ✅ Dummy text to avoid empty index error
        texts = ["Nutrition is important for good health."]
        vectordb = FAISS.from_texts(texts, embedding=embeddings)

        return vectordb

    except Exception as e:
        print("⚠ Error in build_vectorstore:", e)
        return None   # return safe None
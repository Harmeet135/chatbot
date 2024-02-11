from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework import generics, status
from rest_framework.response import Response
from .models import PdfDocument, UserSession
from .serializers import PdfDocumentSerializer
import fitz  # PyMuPDF
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import UserSession
from django.shortcuts import get_object_or_404
import json

load_dotenv()


class Document:
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata if metadata is not None else {}

def get_vectorstore_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_text(text)

    documents = [Document(chunk) for chunk in document_chunks]

    vector_store = Chroma.from_documents(documents, OpenAIEmbeddings())
    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()
    
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
      ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
    return retriever_chain
    
def get_conversational_rag_chain(retriever_chain): 
    
    llm = ChatOpenAI()
    
    prompt = ChatPromptTemplate.from_messages([
      ("system", "Answer the user's questions based on the below context:\n\n{context}"),
      MessagesPlaceholder(variable_name="chat_history"),
      ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

class PdfDocumentView(generics.ListCreateAPIView):
    queryset = PdfDocument.objects.all()
    serializer_class = PdfDocumentSerializer
    
    def create(self, request, *args, **kwargs):
        if 'pdf' in request.FILES:
            pdf_file = request.FILES['pdf']

            try:
                # Create PdfDocument object with the serialized data
                vector_store = get_vectorstore_from_pdf(pdf_file)
                pdf_obj = PdfDocument.objects.create(pdf=pdf_file, conversational_rag_chain=vector_store)

                # Return success response
                return Response({'message': 'PDF uploaded and processed successfully'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No PDF file uploaded'}, status=status.HTTP_400_BAD_REQUEST)


def recreate_vector_store(stored_data):
    data = json.loads(stored_data)
    print(data)
    # Placeholder: Convert stored_data back into a list of Document objects
    # This step depends on how you've decided to store the necessary data
    documents = []
    for data in stored_data:
        document = Document(text=data['text'], metadata=data.get('metadata'))
        documents.append(document)
    
    # Assuming OpenAIEmbeddings or similar is used to compute embeddings
    embeddings_model = OpenAIEmbeddings()
    
    # Reconstruct the vector store with these documents
    vector_store = Chroma.from_documents(documents, embeddings_model)
    
    return vector_store

def get_response(pdf_id, user_input):
    try:
        pdf_document = PdfDocument.objects.get(id=pdf_id)
        vector_store = recreate_vector_store(pdf_document.conversational_rag_chain)
        print(type(vector_store)) 
        
        retriever_chain = get_context_retriever_chain(vector_store)
        conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
        
        response = conversation_rag_chain.invoke({"input": user_input})
        
        return response['answer']
    except PdfDocument.DoesNotExist:
        return 'PDF not found.'
    except Exception as e:
        return f'An error occurred 23: {str(e)}'

class UserQuestionView(APIView):
    def post(self, request, *args, **kwargs):
        pdf_id = request.data.get('pdf_id')  # Retrieve pdf_id from the request
        user_input = request.data.get('question')
        if not pdf_id or not user_input:
            return JsonResponse({'error': 'PDF ID and question are required.'}, status=400)

        try:
            # Ensure the PDF document exists
            pdf_document = PdfDocument.objects.get(id=pdf_id)
            # vector_store = pdf_document.conversational_rag_chain

            answer = get_response(pdf_id, user_input)

            return JsonResponse({'answer': answer})

        except PdfDocument.DoesNotExist:
            return JsonResponse({'error': 'PDF not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'}, status=500)

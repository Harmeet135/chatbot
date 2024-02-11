from django.db import models

class PdfDocument(models.Model):
    pdf = models.FileField(upload_to='pdfs/')
    # vector_store = models.JSONField(blank=True, null=True)  # Using Django's built-in JSONField
    conversational_rag_chain = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"PDF Document - {self.id}"

class UserSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    conversational_rag_chain = models.JSONField(blank=True, null=True)
    chat_history = models.JSONField(default=list)

    def __str__(self):
        return self.session_id

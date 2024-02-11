from rest_framework import serializers
from .models import PdfDocument  # Updated import

class PdfDocumentSerializer(serializers.ModelSerializer):  # Renamed class

    class Meta:
        model = PdfDocument  # Updated model reference
        fields = ('id', 'pdf', 'conversational_rag_chain')  # Updated fields

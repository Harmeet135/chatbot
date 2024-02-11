from django.contrib import admin
from images.models import PdfDocument  # Updated import

admin.site.register(PdfDocument)  # Updated model reference

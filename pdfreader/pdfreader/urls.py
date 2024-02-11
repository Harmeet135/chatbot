from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from images.views import PdfDocumentView , UserQuestionView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PdfDocumentView.as_view(), name='pdf_document_upload'),  
    path('ask/', UserQuestionView.as_view(), name='ask-question'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

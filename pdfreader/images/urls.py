from django.urls import path
from .views import PdfDocumentView, UserQuestionView 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('pdfs/', PdfDocumentView.as_view(), name='pdf-upload'),
    path('ask/', UserQuestionView.as_view(), name='ask-question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

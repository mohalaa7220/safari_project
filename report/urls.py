from django.urls import path
from .views import AddReport, DetailsReport, ExportExcel, report_download


urlpatterns = [
    path('', AddReport.as_view(), name='report'),
    path('<int:pk>', DetailsReport.as_view(), name='report_details'),
    path('<int:pk>/export/', ExportExcel.as_view()),

    # other URL patterns
    path('report_download/', report_download, name='report_download'),
    path('report_download/<int:report_id>',
         report_download, name='report_download'),
]

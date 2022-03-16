from django.urls    import path

from insight.views import TotalReportView

urlpatterns = [
    path("",TotalReportView.as_view()),
]
from django.urls    import path

from insight.views import SearchView

urlpatterns = [
    # path("",TotalReportView.as_view()),
    path('',SearchView.as_view()),
]
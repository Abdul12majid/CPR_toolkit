from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("task_app.urls")),
    path('api/', include("inv_api.urls")),
    path('rely/', include("rely_invoice.urls")),
    path('payment/', include("payment.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

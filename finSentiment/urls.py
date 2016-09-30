from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import finSentiment.views

#admin.autodiscover()
urlpatterns = [url(r'^$', finSentiment.views.home, name='home'),url(r'^admin/', include(admin.site.urls)),
               url(r'^twitterSentiment/', include('twitterSentiment.urls'))] + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

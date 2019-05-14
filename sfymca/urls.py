from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import sfymca.feed.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(sfymca.feed.urls)),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))

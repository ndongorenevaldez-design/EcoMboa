"""
EcoMboa — Root URL Configuration
----------------------------------
All URL namespaces are registered here.
Public pages are accessible without authentication.
Role-specific dashboards redirect via /accounts/redirect/.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Django Admin ──────────────────────────────────────────────────────────
    path('django-admin/', admin.site.urls),

    # ── Authentication (allauth) ──────────────────────────────────────────────
    path('accounts/', include('allauth.urls')),

    # ── Public Pages ──────────────────────────────────────────────────────────
    path('', include('apps.collection_points.public_urls', namespace='public')),

    # ── Citizen Space ─────────────────────────────────────────────────────────
    path('citizen/', include('apps.reports.urls', namespace='reports')),

    # ── Independent Seller Space ──────────────────────────────────────────────
    path('seller/', include('apps.suppliers.urls', namespace='suppliers')),

    # ── Collector Space ───────────────────────────────────────────────────────
    path('collector/', include('apps.missions.urls', namespace='missions')),

    # ── Sorting Center Space ──────────────────────────────────────────────────
    path('center/', include('apps.sorting_center.urls', namespace='sorting_center')),

    # ── Industrial Buyer Space ────────────────────────────────────────────────
    path('buyer/', include('apps.buyers.urls', namespace='buyers')),

    # ── Partner Company Space ─────────────────────────────────────────────────
    path('partner/', include('apps.partners.urls', namespace='partners')),

    # ── EcoMboa Admin Space ───────────────────────────────────────────────────
    path('admin-eco/', include('apps.dashboard.urls', namespace='dashboard')),
    path('admin-eco/finances/', include('apps.finances.urls', namespace='finances')),
    path('admin-eco/collection-points/', include('apps.collection_points.urls', namespace='collection_points')),
    path('admin-eco/reports/', include('apps.reports.admin_urls', namespace='reports_admin')),

    # ── Accounts (profile, redirect) ──────────────────────────────────────────
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),

    # ── REST API ──────────────────────────────────────────────────────────────
    path('api/', include('apps.api.urls', namespace='api')),

    # ── Notifications (HTMX polling endpoint) ─────────────────────────────────
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
]

# ── Media files in development ────────────────────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

# ── Custom error handlers ─────────────────────────────────────────────────────
handler403 = 'apps.accounts.views.error_403'
handler404 = 'apps.accounts.views.error_404'
handler500 = 'apps.accounts.views.error_500'

# Django admin customization
admin.site.site_header = 'EcoMboa Administration'
admin.site.site_title = 'EcoMboa Admin'
admin.site.index_title = 'Platform Management'

from django.http import HttpResponse


def role_redirect(request):
    return HttpResponse("Role redirect placeholder.")


def profile_view(request):
    return HttpResponse("Profile placeholder.")


def error_403(request, exception=None):
    return HttpResponse("Forbidden (403)", status=403)


def error_404(request, exception=None):
    return HttpResponse("Not Found (404)", status=404)


def error_500(request):
    return HttpResponse("Server Error (500)", status=500)


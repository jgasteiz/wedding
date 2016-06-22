from django.core.checks import Error
from django.conf import settings


def check_session_csrf_enabled(app_configs, **kwargs):
    errors = []
    if "session_csrf.CsrfMiddleware" not in settings.MIDDLEWARE_CLASSES:
        errors.append(Error(
            "SESSION_CSRF_DISABLED",
            hint="Please add 'session_csrf.CsrfMiddleware' to MIDDLEWARE_CLASSES",
        ))
    return errors


def check_csp_is_not_report_only(app_configs, **kwargs):
    errors = []
    if getattr(settings, "CSP_REPORT_ONLY", False):
        errors.append(Error(
            "CSP_REPORT_ONLY_ENABLED",
            hint="Please set 'CSP_REPORT_ONLY' to False",
        ))
    return errors


CSP_SOURCE_NAMES = [
    'CSP_DEFAULT_SRC',
    'CSP_SCRIPT_SRC',
    'CSP_IMG_SRC',
    'CSP_OBJECT_SRC',
    'CSP_MEDIA_SRC',
    'CSP_FRAME_SRC',
    'CSP_FONT_SRC',
    'CSP_STYLE_SRC',
    'CSP_CONNECT_SRC',
]

def check_csp_sources_not_unsafe(app_configs, **kwargs):
    errors = []
    for csp_src_name in CSP_SOURCE_NAMES:
        csp_src_values = getattr(settings, csp_src_name, [])
        if "'unsafe-inline'" in csp_src_values or "'unsafe-eval'" in csp_src_values:
            errors.append(Error(
                csp_src_name + "_UNSAFE",
                hint="Please remove 'unsafe-inline'/'unsafe-eval' from your CSP policies",
            ))
    return errors

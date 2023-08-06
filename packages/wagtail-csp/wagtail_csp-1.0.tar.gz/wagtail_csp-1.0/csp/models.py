from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.db import models


@register_setting
class ContentSecurityPolicySettings(BaseSetting):
    class Meta:
        app_label = 'csp'
        managed = True

    CSP_DEFAULT_SRC = models.TextField(
        default="'self'",
        help_text="Fallback for child-src, manifest-src, prefetch-src, worker-src",
    )
    CSP_SCRIPT_SRC = models.TextField(
        default="'self'",
        help_text="Specifies valid sources for javascript. It would be a security win to disallow unsafe-inline in the future by using a nonce-source/hash-source for any inline scripts.",
    )
    CSP_STYLE_SRC = models.TextField(
        default="'self'",
        help_text="Specifies valid sources for stylesheets. It would be a security win to disallow unsafe-inline in the future by using a nonce-source/hash-source for any inline styles.",
    )
    CSP_OBJECT_SRC = models.TextField(
        default="'self'",
        help_text="Specifies valid sources for <object>, <embed>, and <applet> elements.",
    )
    CSP_IMG_SRC = models.TextField(
        default="'self'", help_text="Specifies valid sources for images and favicons."
    )
    CSP_MEDIA_SRC = models.TextField(
        default="'self'",
        help_text="Specifies valid sources for <audio> and <video> elements.",
    )
    CSP_FRAME_SRC = models.TextField(
        default="'self'",
        help_text="Specifies valid sources for <frame> and <iframe> elements.",
    )
    CSP_FONT_SRC = models.TextField(
        default="'self'",
        help_text="Specifies valid sources for fonts loaded using @font-face.",
    )
    CSP_CONNECT_SRC = models.TextField(
        default="'self'",
        help_text="Restricts the URLs which can be loaded using script interfaces. Restricted APIs: <a>, ping, fetch, XMLHttprequest, WebSocket, EventSource, Navigator.sendBeacon.",
    )
    CSP_FRAME_ANCESTORS = models.TextField(
        default="'self'",
        help_text="Specifies valid websites that may embed a page from the website.",
    )

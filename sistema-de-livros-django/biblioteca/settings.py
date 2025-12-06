INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Meus aplicativos
    "livros",
    # Aplicativos de terceiros
    "crispy_forms",
    "crispy_bootstrap5",
]


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "livro_list"
LOGOUT_REDIRECT_URL = "login"

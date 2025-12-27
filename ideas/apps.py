from django.apps import AppConfig

class IdeasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ideas'

    def ready(self):
        # Импорт сигналов для идей
        import ideas.signals  # noqa: F401
        # Регистрация сигналов: обновление счетчиков идей, комментариев и голосов

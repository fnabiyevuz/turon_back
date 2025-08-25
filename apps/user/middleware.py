import datetime
from datetime import timedelta
from django.utils.timezone import now
from apps.user.models import UserActivity


class TrackUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_time = now()
            last_activity = request.session.get("last_activity")

            if last_activity:
                try:
                    last_activity = datetime.datetime.fromisoformat(last_activity)
                    delta = current_time - last_activity

                    # 30 minutdan oshmagan bo‘lsa aktiv vaqt deb hisoblaymiz
                    if delta.total_seconds() < 1800:
                        activity, _ = UserActivity.objects.get_or_create(
                            user=request.user,
                            date=current_time.date(),
                            defaults={"active_time": timedelta(seconds=0)}
                        )
                        activity.active_time += delta
                        activity.save(update_fields=["active_time"])
                except Exception:
                    pass  # session format xatosi bo‘lsa e’tiborsiz qoldiramiz

            # keyingi request uchun saqlab qo‘yish
            request.session["last_activity"] = current_time.isoformat()

        return response

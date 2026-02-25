from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from django.db.models import QuerySet

from automationapp import settings
from src.core.management.commands.base_command import BaseCommand
from src.media.models import PostContent
from src.tiktok.services.post.tiktok_poster_service import TikTokPostService


class Command(BaseCommand):
    def handle(self, *args, **options):
        tiktok = TikTokPostService()
        content: QuerySet[PostContent] = (
            PostContent.objects
            .exclude(status=PostContent.STATUS_UPLOADED)
            .filter(site='all')
        )
        now_utc = datetime.now(timezone.utc)

        for single_content in content:
            local_time = now_utc.astimezone(ZoneInfo(single_content.timezone))
            scheduled_local = single_content.scheduled_at.astimezone(ZoneInfo(single_content.timezone))

            if settings.APP_ENV == 'production' and not (local_time >= scheduled_local):
                continue

            if single_content.is_tiktok():
                tiktok.post_content(single_content)
            elif single_content.is_facebook():
                pass
            else:
                continue

            single_content.status = PostContent.STATUS_UPLOADED
            single_content.save()

            if single_content.group:
                posts = PostContent.objects.filter(group=single_content.group).order_by('id')
                for post in posts:
                    post.status = PostContent.STATUS_UPLOADED
                    post.save()

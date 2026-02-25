import random
from datetime import datetime, time, timezone

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile

from src.media.models import PostContent, SocialAccount
from src.user.models import User


class UploadFileService():
    def upload_file(self, user: User, file: UploadedFile, data: dict):
        fs = FileSystemStorage()
        path = f'{user.id}/{file.name}'
        file_name = fs.save(path, file)
        mime_type = file.content_type
        main_type = mime_type.split("/")[0]

        PostContent.objects.create(
            user=user,
            content_type=main_type,
            site=data.get("site"),
            social_account=SocialAccount.objects.get(id=data.get("social_account_id")),
            title=data.get("title"),
            content=data.get("content"),
            file_name=file_name,
            timezone=data.get("timezone"),
            status=PostContent.STATUS_NONE,
            group=data.get("group") or None,
            scheduled_at=self.generate_random_utc()
        )

    def generate_random_utc(self):
        now_utc = datetime.now(timezone.utc)
        today = now_utc.date()

        hour = random.randint(19, 20)  # 19:00–20:59
        minute = random.randint(0, 59)
        second = random.randint(0, 0)

        return datetime.combine(
            today,
            time(hour, minute, second),
            tzinfo=timezone.utc
        )

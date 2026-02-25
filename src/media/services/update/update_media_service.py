import os

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import get_object_or_404

from src.media.models import PostContent, SocialAccount
from src.user.models import User


class UpdateMediaService():
    def update_media(
            self,
            post_id: int,
            user: User,
            data: dict,
            file: None | UploadedFile
    ):
        post = get_object_or_404(PostContent, id=post_id, user=user)
        if data.get("delete_file"):
            if post.file_name:
                path = post.get_file_path()
                if os.path.exists(path):
                    os.remove(path)
            post.delete()
        else:
            post.site = data.get("site")
            post.social_account = SocialAccount.objects.get(id=data.get("social_account_id"))
            post.title = data.get("title")
            post.content = data.get("content")
            post.timezone = data.get("timezone")

            if file:
                fs = FileSystemStorage()
                path = f'{user.id}/{file.name}'
                file_name = fs.save(path, file)
                mime_type = file.content_type
                main_type = mime_type.split("/")[0]
                post.file_name = file_name
                post.content_type = main_type

            post.save()

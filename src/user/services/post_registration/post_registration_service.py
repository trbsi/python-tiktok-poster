from src.user.models import UserProfile, User


class PostRegistrationService():
    def post_register(self, user: User):
        UserProfile.objects.create(user=user)

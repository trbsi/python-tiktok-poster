import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from automationapp import settings
from src.core.utils import full_url_for_route, save_to_cache


# from django.core.cache import cache


@require_GET
def auth_redirect_to_tiktok(request: HttpRequest):
    """
    https://developers.tiktok.com/doc/login-kit-manage-user-access-tokens?enter_method=left_navigation
    """
    redirect_uri = _redirect_url(request.GET.get('tiktok_username'))
    url = f'https://www.tiktok.com/v2/auth/authorize/?client_key={settings.TIKTOK_CLIENT_KEY}&response_type=code&scope=user.info.basic&redirect_uri={redirect_uri}'

    return redirect(url)


@require_GET
@login_required
def auth_redirect_from_tiktok(request: HttpRequest):
    """
    https://developers.tiktok.com/doc/oauth-user-access-token-management?enter_method=left_navigation
    {
        "access_token": "act.example12345Example12345Example",
        "expires_in": 86400,
        "open_id": "afd97af1-b87b-48b9-ac98-410aghda5344",
        "refresh_expires_in": 31536000,
        "refresh_token": "rft.example12345Example12345Example",
        "scope": "user.info.basic,video.list",
        "token_type": "Bearer"
    }
    """
    user = request.user
    authorization_code = request.GET.get('code')
    tiktok_username = request.GET.get('tiktok_username')

    payload = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "client_secret": settings.TIKTOK_CLIENT_SECRET,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": _redirect_url(tiktok_username),
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    response = requests.post(
        'https://open.tiktokapis.com/v2/oauth/token/', data=payload, headers=headers
    )
    result = response.json()

    save_to_cache(result, tiktok_username)


def _redirect_url(tiktok_username: str):
    return full_url_for_route(
        'tiktok.auth_redirect_from_tiktok',
        query_params={'tiktok_username': tiktok_username}
    )

from django.utils.cache import add_never_cache_headers

class SocialLoginDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # 如果是登入相關路徑，強制告訴瀏覽器「不准快取」
        if 'accounts/google/login' in request.path or 'accounts/login' in request.path:
            add_never_cache_headers(response)
            
        return response

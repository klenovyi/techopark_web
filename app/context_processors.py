from app.models import *


def info(request):
    '''
    tags = Tag.objects.best_tags()
    profiles = Profile.objects.best_members()
    '''
    
    profiles = ["username 226", "username 484", "username 1624", "username 1634",
                "username 1915", "username 2106", "username 2225", "username 5388",
                "username 8160", "username 8292"]
    tags = ["tags 671",
            "tags 1772",
            "tags 2282",
            "tags 2871",
            "tags 3538",
            "tags 3881",
            "tags 6159",
            "tags 6914",
            "tags 8280",
            "tags 8460"]
    context = {'tags': tags,
               'members': profiles}
    return context

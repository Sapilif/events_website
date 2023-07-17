from django.contrib import admin


from .models import Event
from .models import Ticket
from .models import Friendship
from .models import FriendRequest
from .models import AppUser
# Register your models here.


admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
admin.site.register(AppUser)


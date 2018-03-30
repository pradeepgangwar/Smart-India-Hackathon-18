from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(DeptProfile)
admin.site.register(vacancy)
admin.site.register(applications)
admin.site.register(query)
admin.site.register(notifications)
admin.site.register(activation)

from django.contrib import admin
from .models import Contest, ContestProblem, Announcement

admin.site.register(Contest)
admin.site.register(ContestProblem)
admin.site.register(Announcement)

# Removes a user from a contest scoreboard by removing their registration
# Doesn't affect their submissions, though.

import django
from django.conf import settings
import os
import sys

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semicolon_src.settings')
django.setup()

from django.contrib.auth.models import User
from contests.models import Contest, Registration

user_id = int(input("Enter user id: "))
contest_id = int(input("Enter contest id: "))

user = User.objects.get(id=user_id)
contest = Contest.objects.get(id=contest_id)

check = input(f"Remove user {user.username} from contest {contest.name} "
               "Are you sure? Type 'YES' (without the quotes)")

if(check != "YES"):
    quit()

Registration.objects.filter(user_id=user_id, contest_id=contest_id).delete()

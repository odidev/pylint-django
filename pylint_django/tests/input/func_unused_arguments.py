"""
Checks that Pylint still complains about unused-arguments if a function/method
contains an argument named `request`.
"""
# pylint: disable=missing-docstring

from django.http import JsonResponse
from django.views import View


def user_detail(request, user_id):  # [unused-argument]
    # nothing is done with user_id
    return JsonResponse({'username': 'steve'})


class UserView(View):
    def get(self, request, user_id):  # [unused-argument]
        # nothing is done with user_id
        return JsonResponse({'username': 'steve'})

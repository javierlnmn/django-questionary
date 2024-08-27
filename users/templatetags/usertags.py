from django import template
from users.models import CustomUser

register = template.Library()

@register.simple_tag
def get_users_list():
    users = CustomUser.objects.all()
    return users

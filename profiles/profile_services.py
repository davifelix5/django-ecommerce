from . import models


def get_addresses(user):
    return models.Address.objects.filter(user=user.userprofile)

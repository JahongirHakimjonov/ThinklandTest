from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Home Page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Users & Groups"),
        "items": [
            {
                "title": _("Groups"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Users"),
                "icon": "person_add",
                "link": reverse_lazy("admin:users_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("SMS"),
                "icon": "sms",
                "link": reverse_lazy("admin:users_smsconfirm_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Shop"),
        "items": [
            {
                "title": _("Products"),
                "icon": "inventory_2",
                "link": reverse_lazy("admin:shop_product_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_product"
                ),
            },
            {
                "title": _("Categories"),
                "icon": "category",
                "link": reverse_lazy("admin:shop_productcategory_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_productcategory"
                ),
            },
        ],
    },
]

TABS = [
    {
        "models": [
            "auth.user",
            "auth.group",
        ],
        "items": [
            {
                "title": _("Users"),
                "link": reverse_lazy("admin:auth_user_changelist"),
            },
            {
                "title": _("Groups"),
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
        ],
    },
]

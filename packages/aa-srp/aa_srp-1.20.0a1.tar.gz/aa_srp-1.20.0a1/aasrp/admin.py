"""
Django admin declarations
"""

# Django
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

# AA SRP
from aasrp.models import FleetType, RequestComment, SrpLink, SrpRequest


def custom_filter(title):
    """
    Custom filter for model properties
    :param title:
    :return:
    """

    class Wrapper(admin.FieldListFilter):
        """
        Custom_filter :: wrapper
        """

        def expected_parameters(self):
            """
            Expected parameters
            :return:
            :rtype:
            """

            pass

        def choices(self, changelist):
            """
            Choices
            :param changelist:
            :type changelist:
            :return:
            :rtype:
            """

            pass

        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title

            return instance

    return Wrapper


@admin.register(SrpLink)
class SrpLinkAdmin(admin.ModelAdmin):
    """
    SrpLinkAdmin
    """

    list_display = (
        "srp_code",
        "fleet_time",
        "_creator",
        "srp_name",
        "srp_status",
        "fleet_doctrine",
    )
    ordering = ("fleet_time",)

    list_filter = ("creator", "srp_status", "fleet_doctrine")

    search_fields = ("srp_code", "fleet_doctrine", "srp_name")

    @classmethod
    @admin.display(description=_("Creator"), ordering="creator")
    def _creator(cls, obj):
        creator_name = obj.creator

        if obj.creator.profile.main_character:
            creator_name = obj.creator.profile.main_character.character_name

        return creator_name


@admin.register(SrpRequest)
class SrpRequestAdmin(admin.ModelAdmin):
    """
    SrpRequestAdmin
    """

    list_display = (
        "request_code",
        "_creator",
        "character",
        "srp_link",
        "post_time",
        "ship",
        "loss_amount",
        "payout_amount",
        "killboard_link",
        "request_status",
    )
    ordering = ("post_time",)

    list_filter = ("creator", "character", "request_status")

    search_fields = (
        "request_code",
        "character__character_name",
        "ship__name",
        "srp_link__srp_code",
    )

    @classmethod
    @admin.display(description=_("Requestor"), ordering="creator")
    def _creator(cls, obj):
        creator_name = obj.creator

        if obj.creator.profile.main_character:
            creator_name = obj.creator.profile.main_character.character_name

        return creator_name


@admin.register(RequestComment)
class RequestCommentAdmin(admin.ModelAdmin):
    """
    RequestCommentAdmin
    """

    list_display = ("srp_request", "comment_type", "creator")
    ordering = ("srp_request",)
    list_filter = ("comment_type",)


@admin.register(FleetType)
class FleetTypeAdmin(admin.ModelAdmin):
    """
    FleetTypeAdmin
    """

    list_display = ("id", "_name", "_is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)

    @admin.display(description=_("Fleet Type"), ordering="name")
    def _name(self, obj):
        """
        Rewrite name
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.name

    @admin.display(description=_("Is Enabled"), boolean=True, ordering="is_enabled")
    def _is_enabled(self, obj):
        """
        Rewrite is_enabled
        :param obj:
        :type obj:
        :return:
        :rtype:
        """

        return obj.is_enabled

    actions = ("activate", "deactivate")

    @admin.action(description=_("Activate selected fleet types"))
    def activate(self, request, queryset):
        """
        Mark fleet type as active
        :param request:
        :type request:
        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        notifications_count = 0
        failed = 0

        for obj in queryset:
            try:
                obj.is_enabled = True
                obj.save()

                notifications_count += 1
            except Exception:
                failed += 1

        if failed:
            messages.error(
                request,
                ngettext(
                    "Failed to activate {failed} fleet type",
                    "Failed to activate {failed} fleet types",
                    failed,
                ).format(failed=failed),
            )

        if queryset.count() - failed > 0:
            messages.success(
                request,
                ngettext(
                    "Activated {notifications_count} fleet type",
                    "Activated {notifications_count} fleet types",
                    notifications_count,
                ).format(notifications_count=notifications_count),
            )

    @admin.action(description=_("Deactivate selected fleet types"))
    def deactivate(self, request, queryset):
        """
        Mark fleet type as inactive
        :param request:
        :type request:
        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        notifications_count = 0
        failed = 0

        for obj in queryset:
            try:
                obj.is_enabled = False
                obj.save()

                notifications_count += 1
            except Exception:
                failed += 1

        if failed:
            messages.error(
                request,
                ngettext(
                    "Failed to deactivate {failed} fleet type",
                    "Failed to deactivate {failed} fleet types",
                    failed,
                ).format(failed=failed),
            )

        if queryset.count() - failed > 0:
            messages.success(
                request,
                ngettext(
                    "Deactivated {notifications_count} fleet type",
                    "Deactivated {notifications_count} fleet types",
                    notifications_count,
                ).format(notifications_count=notifications_count),
            )

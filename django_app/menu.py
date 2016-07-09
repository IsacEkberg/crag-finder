"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'crag-finder.menu.CustomMenu'
"""
import re
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu
from django_api.models import RockFace, Area


class CustomMenu(Menu):
    """
    Custom Menu for crag-finder admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        superuser = context['request'].user.is_superuser
        resolver_match = context['request'].resolver_match
        view_name = resolver_match.view_name
        match = re.match(r'^admin:django_api_(rockface|area)_change$', view_name)

        if match:
            pk = resolver_match.args[0]
            if match.group(1) == 'rockface':
                rockface = RockFace.objects.get(pk=pk)
                area = rockface.area
            else:  # Its an area.
                area = Area.objects.get(pk=pk)

            rockfaces = []
            for r in area.rockfaces.all():
                rockfaces.append(items.MenuItem(r.name, reverse('admin:django_api_rockface_change', args=(r.pk,))))

            self.children += [
                items.MenuItem(
                    'Områdesöversikt',
                    children=[
                        items.MenuItem('Område: ' + area.name, reverse('admin:django_api_area_change', args=(area.pk,))),
                    ] + rockfaces
                )
            ]
        else:
            self.children += [
                items.MenuItem('Lägg till/Ändra område',
                               children=[
                                   items.MenuItem('Lägg till område', reverse('admin:django_api_area_add')),
                                   items.MenuItem('Ändra ett område', reverse('admin:django_api_area_changelist')),
                               ])
                ]
        if superuser:
            self.children += [items.AppList(
                _('Administration'),
                models=()
            )]




        return super(CustomMenu, self).init_with_context(context)

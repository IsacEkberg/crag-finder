"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'crag-finder.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for crag-finder admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.MenuItem('Lägg till/Ändra område',
                           children=[
                               items.MenuItem('Lägg till område', reverse('admin:django_api_area_add')),
                               items.MenuItem('Ändra ett område', reverse('admin:django_api_area_changelist')),
                           ]),
        ]
            #items.Bookmarks(),
            #items.AppList(
            #    _('Applications'),
            #    exclude=('django.contrib.*',)
            #),

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        superuser = context['request'].user.is_superuser
        print(superuser)
        #if superuser:
        #    self.children += items.AppList(
        #        _('Administration'),
        #        models=()
        #    )
        return super(CustomMenu, self).init_with_context(context)

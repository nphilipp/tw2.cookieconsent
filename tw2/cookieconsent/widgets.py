# -*- coding: utf-8 -*-
#
# tw2.cookieconsent.widgets
#
# Copyright © 2016 Nils Philippsen <nils@tiptoe.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from speaklater import is_lazy_string

from tw2.core import Param, Widget, js_function, js_symbol
from tw2.core.core import request_local
from tw2.core.i18n import _

from .resources import inject_resources

__all__ = ('CookieConsentWidget',)


class CookieConsentWidget(Widget):

    template = ""

    default_options = {
        'header': _("Cookies used on the website!"),
        'message': _("This website uses cookies to ensure you get the"
                     " best experience on our website."),
        'dismiss': _("Got it!"),
        'allow': _("Allow cookies"),
        'deny': _("Decline"),
        'link': _("Learn more"),
    }

    options = Param(
        "The options passed to the plugin", default={})

    def prepare(self):
        super(CookieConsentWidget, self).prepare()

        if self.options:
            cfg = self.options
        else:
            cfg = self.default_options

        # always use full URLs for themes
        theme = cfg.get('theme', 'light-floating')
        rl = request_local()
        cfg['theme'] = (
            rl['middleware'].config.res_prefix + 'tw2.cookieconsent/static/'
            + theme + ".css")

        # evaluate any lazy strings
        for key, value in cfg.items():
            if is_lazy_string(value):
                cfg[key] = str(value)

        self.add_call(js_function(
            "(function(window,cfg){window.cookieconsent_options=cfg;})"
        )(js_symbol("window"), cfg), location='head')
        inject_resources()

    def generate_output(self, displays_on):
        return u""

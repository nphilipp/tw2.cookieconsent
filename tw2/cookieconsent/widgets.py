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

from tw2.core import Widget, Param, js_function, js_symbol
from tw2.core.core import request_local
from tw2.core.i18n import _
from speaklater import is_lazy_string

from .resources import inject_resources

__all__ = ('CookieConsentWidget',)


class CookieConsentWidget(Widget):

    template = ""

    message = Param(
        "The message shown by the plugin.", default=_(
            "This website uses cookies to ensure you get the best "
            "experience on our website"))

    dismiss = Param(
        "The text used on the dismiss button.", default=_("Got it!"))

    learnMore = Param(
        "The text shown on the link to the cookie policy (requires the link "
        "option to also be set).", default=_("More info"))

    link = Param(
        "The url of your cookie policy. If it isn't set, the link is hidden.",
        default=None)

    container = Param(
        "The element you want the Cookie Consent notification to be "
        "appended to. If None, the Cookie Consent plugin is appended to "
        "the body.\n\nNote: the majority of our built in themes are "
        "designed around the plugin being a child of the body.", default=None)

    theme = Param("The theme you wish to use.", default='light-floating')

    path = Param(
        "The path for the consent cookie that Cookie Consent uses, to "
        "remember that users have consented to cookies. Use to limit "
        "consent to a specific path within your website.", default="/")

    domain = Param(
        "The domain for the consent cookie that Cookie Consent uses, "
        "to remember that users have consented to cookies. Useful if "
        "your website uses multiple subdomains, e.g. if your script is "
        "hosted at www.example.com you might override this to example.com, "
        "thereby allowing the same consent cookie to be read by subdomains "
        "like foo.example.com.", default=None)

    expiryDays = Param(
        "The number of days Cookie Consent should store the user’s consent "
        "information for.", default=365)

    target = Param(
        "The target of the link to your cookie policy. Use to open a link "
        "in a new window, or specific frame, if you wish.", default='_self')

    def prepare(self):
        super(CookieConsentWidget, self).prepare()

        cfg = {}

        for parm in (
                'message', 'dismiss', 'learnMore', 'link', 'container',
                'theme', 'path', 'domain', 'expiryDays', 'target'):
            val = getattr(self, parm)
            if val is not None:
                if parm != "theme":
                    cfg[parm] = str(val) if is_lazy_string(val) else val
                else:
                    rl = request_local()
                    cfg[parm] = (
                        rl['middleware'].config.res_prefix +
                        'tw2.cookieconsent/static/' + val + ".css")

        self.add_call(js_function("(function(window,cfg){window.cookieconsent_options=cfg;})")(js_symbol("window"), cfg), location='head')
        inject_resources()

    def generate_output(self, displays_on):
        return u""

# -*- coding: utf-8 -*-
#
# tw2.cookieconsent.resources
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

from tw2.core import JSLink, DirLink
from tw2.core.middleware import register_resource

__all__ = ('cookieconsent_js', 'cookieconsent_static_resources')


class CookieConsentResourceMixin(object):

    modname = 'tw2.cookieconsent'


class CookieConsentJSLink(CookieConsentResourceMixin, JSLink):

    filename = "static/cookieconsent.min.js"


class CookieConsentDirLink(CookieConsentResourceMixin, DirLink):

    filename = "static"
    whole_dir = True


cookieconsent_js = CookieConsentJSLink()
cookieconsent_static_resources = CookieConsentDirLink()

cookieconsent_resources = [cookieconsent_js, cookieconsent_static_resources]

def register_resources():
    for res in cookieconsent_resources:
        res_req = res.req()
        register_resource(
                res_req.modname, res_req.filename, isinstance(res, DirLink))

def inject_resources():
    for res in cookieconsent_resources:
        res.inject()

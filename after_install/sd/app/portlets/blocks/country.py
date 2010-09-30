# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.formlib.form import Fields
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from sd import _
from base import *
from interfaces import ICountryBlock


class Country(AssignmentWithImage):
    """A portlet representing a country.
    """
    implements(ICountryBlock)

    def __init__(self, name, local_names=[], caption=u"", image=None):
        super(Country, self).__init__(name, caption, image)
        self.local_names = local_names


class AddForm(AddFormWithImage):
    """Country block add form
    """
    form_fields = Fields(ICountryBlock)

    def create(self, data):
        country = Country(**data)
        return country


class EditForm(EditFormWithImage):
    """Country block edit form
    """
    label = _(u"Edit Country block")
    description = _(u"This form allow you to edit your country block.")
    form_fields = Fields(ICountryBlock)


class Renderer(ImagePortletRenderer):
    """Browser view to render a country block
    """
    render = ViewPageTemplateFile('templates/country.pt')
    
    def names(self):
        return self.data.local_names

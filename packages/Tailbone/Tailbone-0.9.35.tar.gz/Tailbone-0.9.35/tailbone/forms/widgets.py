# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Form Widgets
"""

import json
import datetime
import decimal

import colander
from deform import widget as dfwidget
from webhelpers2.html import tags, HTML

from tailbone.db import Session
from tailbone.forms.types import ProductQuantity


class ReadonlyWidget(dfwidget.HiddenWidget):

    readonly = True

    def serialize(self, field, cstruct, **kw):
        if cstruct in (colander.null, None):
            cstruct = ''
        # TODO: is this hacky?
        text = kw.get('text')
        if not text:
            text = field.parent.tailbone_form.render_field_value(field.name)
        return HTML.tag('span', text) + tags.hidden(field.name, value=cstruct, id=field.oid)


class NumberInputWidget(dfwidget.TextInputWidget):
    template = 'numberinput'
    autocomplete = 'off'


class NumericInputWidget(NumberInputWidget):
    """
    This widget only supports Buefy themes for now.  It uses a
    ``<numeric-input>`` component, which will leverage the ``numeric.js``
    functions to ensure user doesn't enter any non-numeric values.  Note that
    this still uses a normal "text" input on the HTML side, as opposed to a
    "number" input, since the latter is a bit ugly IMHO.
    """
    template = 'numericinput'
    allow_enter = True


class PercentInputWidget(dfwidget.TextInputWidget):
    """
    Custom text input widget, used for "percent" type fields.  This widget
    assumes that the underlying storage for the value is a "traditional"
    percent value, e.g. ``0.36135`` - but the UI should represent this as a
    "human-friendly" value, e.g. ``36.135 %``.
    """
    template = 'percentinput'
    autocomplete = 'off'

    def serialize(self, field, cstruct, **kw):
        if cstruct not in (colander.null, None):
            # convert "traditional" value to "human-friendly"
            value = decimal.Decimal(cstruct) * 100
            value = value.quantize(decimal.Decimal('0.001'))
            cstruct = str(value)
        return super(PercentInputWidget, self).serialize(field, cstruct, **kw)

    def deserialize(self, field, pstruct):
        pstruct = super(PercentInputWidget, self).deserialize(field, pstruct)
        if pstruct is colander.null:
            return colander.null
        # convert "human-friendly" value to "traditional"
        try:
            value = decimal.Decimal(pstruct)
        except decimal.InvalidOperation:
            raise colander.Invalid(field.schema, "Invalid decimal string: {}".format(pstruct))
        value = value.quantize(decimal.Decimal('0.00001'))
        value /= 100
        return str(value)


class CasesUnitsWidget(dfwidget.Widget):
    """
    Widget for collecting case and/or unit quantities.  Most useful when you
    need to ensure user provides cases *or* units but not both.
    """
    template = 'cases_units'
    amount_required = False
    one_amount_only = False

    def serialize(self, field, cstruct, **kw):
        if cstruct in (colander.null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        kw['cases'] = cstruct['cases'] or ''
        kw['units'] = cstruct['units'] or ''
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        return field.renderer(template, **values)

    def deserialize(self, field, pstruct):
        if pstruct is colander.null:
            return colander.null

        schema = ProductQuantity()
        try:
            validated = schema.deserialize(pstruct)
        except colander.Invalid as exc:
            raise colander.Invalid(field.schema, "Invalid pstruct: %s" % exc)

        if self.amount_required and not (validated['cases'] or validated['units']):
            raise colander.Invalid(field.schema, "Must provide case or unit amount",
                                   value=validated)

        if self.amount_required and self.one_amount_only and validated['cases'] and validated['units']:
            raise colander.Invalid(field.schema, "Must provide case *or* unit amount, "
                                   "but *not* both", value=validated)

        return validated


class DynamicCheckboxWidget(dfwidget.CheckboxWidget):
    """
    This checkbox widget can be "dynamic" in the sense that form logic can
    control its value and state.
    """
    template = 'checkbox_dynamic'


class PlainSelectWidget(dfwidget.SelectWidget):
    template = 'select_plain'


class CustomSelectWidget(dfwidget.SelectWidget):
    """
    This widget is mostly for convenience.  You can set extra kwargs for the
    :meth:`serialize()` method, e.g.::

       widget.set_template_values(foo='bar')
    """

    def set_template_values(self, **kw):
        if not hasattr(self, 'extra_template_values'):
            self.extra_template_values = {}
        self.extra_template_values.update(kw)

    def get_template_values(self, field, cstruct, kw):
        values = super(CustomSelectWidget, self).get_template_values(field, cstruct, kw)
        if hasattr(self, 'extra_template_values'):
            values.update(self.extra_template_values)
        return values


class DynamicSelectWidget(CustomSelectWidget):
    """
    This is a "normal" select widget, but instead of (or in addition to) its
    values being set when constructed, they must be assigned dynamically in
    real-time, e.g. based on other user selections.

    Really all this widget "does" is render some Vue.js-compatible HTML, but
    the page which contains the widget is ultimately responsible for wiring up
    the logic for things to work right.
    """
    template = 'select_dynamic'


class JQuerySelectWidget(dfwidget.SelectWidget):
    template = 'select_jquery'


class PlainDateWidget(dfwidget.DateInputWidget):
    template = 'date_plain'


class JQueryDateWidget(dfwidget.DateInputWidget):
    """
    Uses the jQuery datepicker UI widget, instead of whatever it is deform uses
    by default.
    """
    template = 'date_jquery'
    type_name = 'text'
    requirements = None

    default_options = (
        ('changeMonth', True),
        ('changeYear', True),
        ('dateFormat', 'yy-mm-dd'),
    )

    def serialize(self, field, cstruct, **kw):
        if cstruct in (colander.null, None):
            cstruct = ''
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        options = dict(
            kw.get('options') or self.options or self.default_options
        )
        options.update(kw.get('extra_options', {}))
        kw.setdefault('options_json', json.dumps(options))
        kw.setdefault('selected_callback', None)
        values = self.get_template_values(field, cstruct, kw)
        return field.renderer(template, **values)


class JQueryTimeWidget(dfwidget.TimeInputWidget):
    """
    Uses the jQuery datepicker UI widget, instead of whatever it is deform uses
    by default.
    """
    template = 'time_jquery'
    type_name = 'text'
    requirements = None
    default_options = (
        ('showPeriod', True),
    )


class JQueryAutocompleteWidget(dfwidget.AutocompleteInputWidget):
    """ 
    Uses the jQuery autocomplete plugin, instead of whatever it is deform uses
    by default.
    """
    template = 'autocomplete_jquery'
    requirements = None
    field_display = ""
    assigned_label = None
    service_url = None
    cleared_callback = None
    selected_callback = None
    input_callback = None
    new_label_callback = None
    ref = None

    default_options = (
        ('autoFocus', True),
    )
    options = None

    def serialize(self, field, cstruct, **kw):
        if 'delay' in kw or getattr(self, 'delay', None):
            raise ValueError(
                'AutocompleteWidget does not support *delay* parameter '
                'any longer.'
            )
        if cstruct in (colander.null, None):
            cstruct = ''
        self.values = self.values or []
        readonly = kw.get('readonly', self.readonly)

        options = dict(
            kw.get('options') or self.options or self.default_options
        )
        options['source'] = self.service_url

        kw['options'] = json.dumps(options)
        kw['field_display'] = self.field_display
        kw['cleared_callback'] = self.cleared_callback
        kw['assigned_label'] = self.assigned_label
        kw['input_callback'] = self.input_callback
        kw['new_label_callback'] = self.new_label_callback
        kw['ref'] = self.ref
        kw.setdefault('selected_callback', self.selected_callback)
        tmpl_values = self.get_template_values(field, cstruct, kw)
        template = readonly and self.readonly_template or self.template
        return field.renderer(template, **tmpl_values)


class MultiFileUploadWidget(dfwidget.FileUploadWidget):
    """
    Widget to handle multiple (arbitrary number) of file uploads.
    """
    template = 'multi_file_upload'
    requirements = ()

    def deserialize(self, field, pstruct):
        if pstruct is colander.null:
            return colander.null

        # TODO: why is this a thing?  pstruct == [b'']
        if len(pstruct) == 1 and pstruct[0] == b'':
            return colander.null

        files_data = []
        for upload in pstruct:

            data = self.deserialize_upload(upload)
            if data:
                files_data.append(data)

        if not files_data:
            return colander.null

        return files_data

    def deserialize_upload(self, upload):
        # nb. this logic was copied from parent class and adapted
        # to allow for multiple files.  needs some more love.

        uid = None              # TODO?

        if hasattr(upload, "file"):
            # the upload control had a file selected
            data = dfwidget.filedict()
            data["fp"] = upload.file
            filename = upload.filename
            # sanitize IE whole-path filenames
            filename = filename[filename.rfind("\\") + 1 :].strip()
            data["filename"] = filename
            data["mimetype"] = upload.type
            data["size"] = upload.length
            if uid is None:
                # no previous file exists
                while 1:
                    uid = self.random_id()
                    if self.tmpstore.get(uid) is None:
                        data["uid"] = uid
                        self.tmpstore[uid] = data
                        preview_url = self.tmpstore.preview_url(uid)
                        self.tmpstore[uid]["preview_url"] = preview_url
                        break
            else:
                # a previous file exists
                data["uid"] = uid
                self.tmpstore[uid] = data
                preview_url = self.tmpstore.preview_url(uid)
                self.tmpstore[uid]["preview_url"] = preview_url
        else:
            # the upload control had no file selected
            if uid is None:
                # no previous file exists
                return colander.null
            else:
                # a previous file should exist
                data = self.tmpstore.get(uid)
                # but if it doesn't, don't blow up
                if data is None:
                    return colander.null
        return data


def make_customer_widget(request, **kwargs):
    """
    Make a customer widget; will be either autocomplete or dropdown
    depending on config.
    """
    # use autocomplete widget by default
    factory = CustomerAutocompleteWidget

    # caller may request dropdown widget
    if kwargs.pop('dropdown', False):
        factory = CustomerDropdownWidget

    else: # or, config may say to use dropdown
        if request.rattail_config.getbool(
                'rattail', 'customers.choice_uses_dropdown',
                default=False):
            factory = CustomerDropdownWidget

    # instantiate whichever
    return factory(request, **kwargs)


class CustomerAutocompleteWidget(JQueryAutocompleteWidget):
    """
    Autocomplete widget for a Customer reference field.
    """

    def __init__(self, request, *args, **kwargs):
        super(CustomerAutocompleteWidget, self).__init__(*args, **kwargs)
        self.request = request
        model = self.request.rattail_config.get_model()

        # must figure out URL providing autocomplete service
        if 'service_url' not in kwargs:

            # caller can just pass 'url' instead of 'service_url'
            if 'url' in kwargs:
                self.service_url = kwargs['url']

            else: # use default url
                self.service_url = self.request.route_url('customers.autocomplete')

        # TODO
        if 'input_callback' not in kwargs:
            if 'input_handler' in kwargs:
                self.input_callback = input_handler

    def serialize(self, field, cstruct, **kw):

        # fetch customer to provide button label, if we have a value
        if cstruct:
            model = self.request.rattail_config.get_model()
            customer = Session.get(model.Customer, cstruct)
            if customer:
                self.field_display = str(customer)

        return super(CustomerAutocompleteWidget, self).serialize(
            field, cstruct, **kw)


class CustomerDropdownWidget(dfwidget.SelectWidget):
    """
    Dropdown widget for a Customer reference field.
    """

    def __init__(self, request, *args, **kwargs):
        super(CustomerDropdownWidget, self).__init__(*args, **kwargs)
        self.request = request

        # must figure out dropdown values, if they weren't given
        if 'values' not in kwargs:

            # use what caller gave us, if they did
            if 'customers' in kwargs:
                customers = kwargs['customers']
                if callable(customers):
                    customers = customers()

            else: # default customer list
                model = self.request.rattail_config.get_model()
                customers = Session.query(model.Customer)\
                                   .order_by(model.Customer.name)\
                                   .all()

            # convert customer list to option values
            self.values = [(c.uuid, c.name)
                           for c in customers]


class DepartmentWidget(dfwidget.SelectWidget):
    """
    Custom select widget for a Department reference field.

    Constructor accepts the normal ``values`` kwarg but if not
    provided then the widget will fetch department list from Rattail
    DB.

    Constructor also accepts ``required`` kwarg, which defaults to
    true unless specified.
    """

    def __init__(self, request, **kwargs):

        if 'values' not in kwargs:
            model = request.rattail_config.get_model()
            departments = Session.query(model.Department)\
                                 .order_by(model.Department.number)
            values = [(dept.uuid, str(dept))
                      for dept in departments]
            if not kwargs.pop('required', True):
                values.insert(0, ('', "(none)"))
            kwargs['values'] = values

        super(DepartmentWidget, self).__init__(**kwargs)


def make_vendor_widget(request, **kwargs):
    """
    Make a vendor widget; will be either autocomplete or dropdown
    depending on config.
    """
    # use autocomplete widget by default
    factory = VendorAutocompleteWidget

    # caller may request dropdown widget
    if kwargs.pop('dropdown', False):
        factory = VendorDropdownWidget

    else: # or, config may say to use dropdown
        app = request.rattail_config.get_app()
        vendor_handler = app.get_vendor_handler()
        if vendor_handler.choice_uses_dropdown():
            factory = VendorDropdownWidget

    # instantiate whichever
    return factory(request, **kwargs)


class VendorAutocompleteWidget(JQueryAutocompleteWidget):
    """
    Autocomplete widget for a Vendor reference field.
    """

    def __init__(self, request, *args, **kwargs):
        super(VendorAutocompleteWidget, self).__init__(*args, **kwargs)
        self.request = request
        model = self.request.rattail_config.get_model()

        # must figure out URL providing autocomplete service
        if 'service_url' not in kwargs:

            # caller can just pass 'url' instead of 'service_url'
            if 'url' in kwargs:
                self.service_url = kwargs['url']

            else: # use default url
                self.service_url = self.request.route_url('vendors.autocomplete')

        # # TODO
        # if 'input_callback' not in kwargs:
        #     if 'input_handler' in kwargs:
        #         self.input_callback = input_handler

    def serialize(self, field, cstruct, **kw):

        # fetch vendor to provide button label, if we have a value
        if cstruct:
            model = self.request.rattail_config.get_model()
            vendor = Session.get(model.Vendor, cstruct)
            if vendor:
                self.field_display = str(vendor)

        return super(VendorAutocompleteWidget, self).serialize(
            field, cstruct, **kw)


class VendorDropdownWidget(dfwidget.SelectWidget):
    """
    Dropdown widget for a Vendor reference field.
    """

    def __init__(self, request, *args, **kwargs):
        super(VendorDropdownWidget, self).__init__(*args, **kwargs)
        self.request = request

        # must figure out dropdown values, if they weren't given
        if 'values' not in kwargs:

            # use what caller gave us, if they did
            if 'vendors' in kwargs:
                vendors = kwargs['vendors']
                if callable(vendors):
                    vendors = vendors()

            else: # default vendor list
                model = self.request.rattail_config.get_model()
                vendors = Session.query(model.Vendor)\
                                   .order_by(model.Vendor.name)\
                                   .all()

            # convert vendor list to option values
            self.values = [(c.uuid, c.name)
                           for c in vendors]

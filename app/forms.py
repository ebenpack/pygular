from flask.ext.wtf import Form, TextField, TextAreaField, SelectMultipleField, widgets
from flask.ext.wtf import Required


OPTIONS = [('L', 'Locale'), ('m', 'Multiline'), ('s', 'Dot all'), ('u', 'Unicode'), ('i', 'Ignore case'), ('x', 'Verbose')]


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RegExForm(Form):
    regex = TextField('regex', validators = [Required()])
    test = TextAreaField('test', validators = [Required()])
    options = MultiCheckboxField('options',choices=OPTIONS)

    #TODO: Handle warnings (e.g. 'Expression not valid') with form validation
# coding: utf-8
from copy import copy


class ComponentHtml(object):
    """
    <TAG></TAG>
    """
    def __init__(self, tag_name, innerHtml='', **kwargs):
        self.tag_name = tag_name
        self.innerHtml = innerHtml
        self.kwargs = kwargs

        # Every component may have associated scripts.
        self.css_libraries = []
        self.javascript_libraries = []
        self._script = ''
        self.jquery_init_code = ''

        self.propagate_scripts(innerHtml)

    def __str__(self):
        return self.as_html()

    def as_html(self):
        return ComponentHtml.tag(self.tag_name, self.innerHtml, **self.kwargs)

    def add_component(self, component):
        """
        @component must be a ComponentHtml or a unicode string.
        """
        self.innerHtml += unicode(component)
        self.propagate_scripts(component)

    def propagate_scripts(self, component):
        if isinstance(component, ComponentHtml):
            # avoid replicated libraries ('set' function does not preserve order)
            for css_lib in component.css_libraries:
                self.css_libraries.append(css_lib)
            for js_lib in component.javascript_libraries:
                self.javascript_libraries.append(js_lib)
            self.add_javascript_code(component._script)
            self.add_jquery_init_code(component.jquery_init_code)

    def get(self, attr):
        try:
            return self.kwargs[attr]
        except KeyError:
            return None

    def set(self, attr, value):
        self.kwargs[attr] = value

    def clone(self):
        return copy(self)

    # Scripts Methods

    def add_css_library(self, href):
        self.css_libraries.append(href)

    def add_javascript_library(self, src):
        self.javascript_libraries.append(src)

    def add_javascript_code(self, src):
        self._script += src

    def add_jquery_init_code(self, src):
        self.jquery_init_code += src

    # Global methods

    @classmethod
    def attribute_conversion(cls, name):
        if name == 'clazz': return u'class'
        if name == 'xml_lang': return u'xml:lang'
        if name == 'http_equiv': return u'http-equiv'
        return name

    @classmethod
    def tag(cls, tag_name, innerHtml, **kwargs):
        attr_function = lambda key, value: u' %s="%s"' % (cls.attribute_conversion(key), value) if value else u''
        attributes_string = u''.join(attr_function(key, value) for key, value in kwargs.iteritems()) if kwargs else u''
        return u'<%s%s>%s</%s>' % (tag_name, attributes_string, innerHtml, tag_name)

    @classmethod
    def simple_tag(cls, tag_name, **kwargs):
        attr_function = lambda key, value: u' %s="%s"' % (cls.attribute_conversion(key), value) if value else u''
        attributes_string = u''.join(attr_function(key, value) for key, value in kwargs.iteritems()) if kwargs else u''
        return u'<%s%s/>' % (tag_name, attributes_string)


class SimpleComponentHtml(ComponentHtml):
    """
    <TAG/>
    """
    def as_html(self):
        return ComponentHtml.simple_tag(self.tag_name, **self.kwargs)


class Image(SimpleComponentHtml):
    """
    <img>
    """
    def __init__(self, src, **kwargs):
        super(Image, self).__init__(u'img', src=src, **kwargs)


class Link(ComponentHtml):
    """
    <a>
    """
    def __init__(self, href, innerHtml, target=None, **kwargs):
        super(Link, self).__init__(u'a', href=href, innerHtml=innerHtml, target=target, **kwargs)


class Paragraph(ComponentHtml):
    """
    <p>
    """
    def __init__(self, innerHtml, **kwargs):
        super(Paragraph, self).__init__(u'p', innerHtml=innerHtml, **kwargs)


class UnorderedList(ComponentHtml):
    """
    <ul>
    """
    def __init__(self, **kwargs):
        super(UnorderedList, self).__init__(u'ul', **kwargs)

    #override
    def add_component(self, component):
        if isinstance(component, (str, unicode)):
            super(UnorderedList, self).add_component(ComponentHtml.tag(u'li', component))
        else:
            if component.tag_name == 'li':
                super(UnorderedList, self).add_component(component)
            else:
                super(UnorderedList, self).add_component(ComponentHtml.tag(u'li', component))


class OrderedList(ComponentHtml):
    """
    <ol>
    """
    def __init__(self, **kwargs):
        super(OrderedList, self).__init__(u'ol', **kwargs)

    #override
    def add_component(self, component):
        if isinstance(component, (str, unicode)):
            super(OrderedList, self).add_component(ComponentHtml.tag(u'li', component))
        else:
            if component.tag_name == 'li':
                super(UnorderedList, self).add_component(component)
            else:
                super(UnorderedList, self).add_component(ComponentHtml.tag(u'li', component))


class Chunk(ComponentHtml):
    """
    <span>
    """
    def __init__(self, innerHtml=u'', **kwargs):
        super(Chunk, self).__init__(u'span', innerHtml=innerHtml, **kwargs)


class Panel(ComponentHtml):
    """
    <div>
    """
    def __init__(self, innerHtml=u'', **kwargs):
        super(Panel, self).__init__(u'div', innerHtml=innerHtml, **kwargs)


class InformationPanel(Panel):
    """
    <div><span class="label"><span><span class="value"><span></div>
    """
    def __init__(self, innerHtml=u'', label_class='', value_class='value', **kwargs):
        super(Panel, self).__init__(u'div', innerHtml=innerHtml, **kwargs)
        self.label_class = label_class
        self.value_class = value_class
        
    def add_info(self, label, value):
        self.add_component(Chunk(label, clazz=self.label_class))
        self.add_component(Chunk(value, clazz=self.value_class))
        self.add_component('<br/>')
    

class Table(ComponentHtml):
    """
    <table>
    """
    LINE_CLASSES = (u'odd', u'even')

    def __init__(self, **kwargs):
        super(Table, self).__init__(u'table', **kwargs)
        self._header = ComponentHtml(u'thead', u'')
        self._header_line = None
        self._body = ComponentHtml(u'tbody', u'')
        self._body_line = None
        self._line_index = 0

    def start_header_line(self):
        if self._header_line is not None:
            self._header.add_component(self._header_line)
        self._header_line = ComponentHtml(u'tr', u'')

    def add_cell_on_header(self, content, **kwargs):
        # FIXME: it must propagate libraries
        self.propagate_scripts(content)
        if self._header_line is None:
            self.start_header_line()
        if isinstance(content, (str, unicode)):
            content = ComponentHtml(u'th', content, **kwargs)
        self._header_line.add_component(content)

    def start_line(self):
        if self._body_line is not None:
            self._body.add_component(self._body_line)
        self._body_line = ComponentHtml(u'tr', '', clazz=Table.LINE_CLASSES[self._line_index % 2])
        self._line_index += 1

    def add_cell(self, content, **kwargs):
        # FIXME: it must propagate libraries
        self.propagate_scripts(content)
        if self._body_line is None:
            self.start_line()
        content = ComponentHtml(u'td', content, **kwargs)
        self._body_line.add_component(content)

    #override
    def as_html(self):
        self.start_header_line()
        self.start_line()
        self.innerHtml = self._header.as_html()
        self.innerHtml += self._body.as_html()
        return super(Table, self).as_html()


class Form(ComponentHtml):
    """
    <form>
    """
    def __init__(self, action, method=u'post', **kwargs):
        super(Form, self).__init__(u'form', action=action, method=method, **kwargs)

    def add_component_with_label(self, label, component):
        panel = ComponentHtml(u'div', '', clazz=u'form-label-field')
        panel.add_component(ComponentHtml.tag(u'div', ComponentHtml.tag(u'span', label), clazz=u'form-label'))
        panel.add_component(ComponentHtml.tag(u'div', component, clazz=u'form-field'))
        self.add_component(panel)

    def include_file_upload(self):
        self.set('enctype', 'multipart/form-data')


class TextBox(SimpleComponentHtml):
    """
    <input type="text">
    """
    def __init__(self, name, value, maxlength=100, **kwargs):
        super(TextBox, self).__init__(u'input', type=u'text', name=name, value=value, maxlength=maxlength, **kwargs)


class TextArea(ComponentHtml):
    """
    <textarea>
    """
    def __init__(self, name, value, maxlength=500, **kwargs):
        super(TextArea, self).__init__(u'textarea', name=name, value=value, maxlength=maxlength, **kwargs)


class CheckBox(SimpleComponentHtml):
    """
    <input type="checkbox">
    """
    def __init__(self, name, **kwargs):
        super(CheckBox, self).__init__(u'input', type=u'checkbox', name=name, **kwargs)

    #override
    def set(self, attr, value):
        "Checkbox should have value attribute too. We need a trustable and solid standard"

        if attr == u'value':
            if value in [True, 'True', 'true', 'on']:
                super(CheckBox, self).set(u'checked', u'checked')
            else:
                super(CheckBox, self).set(u'checked', u'')
        else:
            super(CheckBox, self).set(attr, value)

    def get(self, attr):
        if attr == 'value':
            return True if super(CheckBox, self).get(u'checked') else False
        else:
            return super(CheckBox, self).get(attr)


class UploadBox(SimpleComponentHtml):
    """
    <input type="file">
    """
    def __init__(self, name, value, **kwargs):
        super(UploadBox, self).__init__(u'input', type=u'file', name=name, value=value, **kwargs)


class Select(ComponentHtml):
    """
    <select>
    """
    def __init__(self, name, multiple=False, **kwargs):
        if multiple:
            multiple = u'multiple'
        else:
            multiple = u''
        super(Select, self).__init__(u'select', name=name, multiple=multiple, **kwargs)
        self.options = []

    def add_option(self, label, value, selected=False):
        if selected:
            option = ComponentHtml(u'option', innerHtml=label, value=value, selected=u'selected')
        else:
            option = ComponentHtml(u'option', innerHtml=label, value=value)
        self.options.append(option)

    def set(self, attr, value):
        "Select should have value attribute too. We need a trustable and solid standard"
        if attr == u'value':
            if isinstance(value, list):
                for v in value:
                    for option in self.options:
                        if unicode(option.get(u'value')) == v:
                            option.set(u'selected', u'selected')
                            break
            else: # only one value
                for option in self.options:
                    if option.get(u'value') == value:
                        option.set(u'selected', u'selected')
        else:
            super(Select, self).set(attr, value)

    def get(self, attr):
        if attr == u'value':
            if self.get(u'multiple') == u'multiple':
                values = []
                for option in self.options:
                    if option.get(u'selected') == u'selected':
                        values.append(option.get(u'value'))
                return values
            else:
                for option in self.options:
                    if option.get(u'selected') == u'selected':
                        return option.get(u'value')
                return None
        else:
            return super(Select, self).get(attr)

    #override
    def as_html(self):
        self.innerHtml = ''.join([option.as_html() for option in self.options])
        return super(Select, self).as_html()


class SubmitButton(SimpleComponentHtml):
    """
    <input type="submit">
    """
    def __init__(self, id, value, **kwargs):
        super(SubmitButton, self).__init__(u'input', type=u'submit', id=id, value=value, **kwargs)


class HiddenField(SimpleComponentHtml):
    """
    <input type="submit">
    """
    def __init__(self, id, value, **kwargs):
        super(HiddenField, self).__init__(u'input', type=u'hidden', id=id, value=value, **kwargs)


class Button(ComponentHtml):
    """
    <button>
    """
    def __init__(self, id, **kwargs):
        super(Button, self).__init__(u'button', id=id, **kwargs)


class Head(ComponentHtml):
    """
    <head>
    """
    def __init__(self, title, description, keywords, favicon, **kwargs):
        super(Head, self).__init__(u'head', **kwargs)
        self.title = title
        self.description = description
        self.keywords = keywords
        self.favicon = favicon

    #override
    def as_html(self):
        self.innerHtml = ComponentHtml.tag(u'title', self.title)
        self.innerHtml += ComponentHtml.simple_tag(u'meta', name=u'description', content=self.description)
        self.innerHtml += ComponentHtml.simple_tag(u'meta', name=u'keywords', content=self.keywords)
        self.innerHtml += ComponentHtml.simple_tag(u'meta', http_equiv=u'Content-Type', content=u'text/html;charset=UTF-8')
        if self.favicon:
            self.innerHtml += ComponentHtml.simple_tag(u'link', rel=u'shortcut', href=self.favicon)
        for href in self.css_libraries:
            self.innerHtml += ComponentHtml.simple_tag(u'link', type=u'text/css', rel=u'stylesheet', href=href)
        for src in self.javascript_libraries:
            self.innerHtml += ComponentHtml.tag(u'script', '', type=u'text/javascript', src=src)
        script = ComponentHtml(u'script', '', type=u'text/javascript')
        if self.jquery_init_code:
            script.add_component(u'$(document).ready(function() { %s });' % self.jquery_init_code);
        self.innerHtml += script.as_html()
        return super(Head, self).as_html()


class Body(ComponentHtml):
    """
    <body>
    """
    def __init__(self, **kwargs):
        super(Body, self).__init__(u'body', **kwargs)


class Page(ComponentHtml):
    """
    <html>
    """
    TRANSITIONAL_401 = u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n'
    STRICT_401 = u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n'
    HTML5_DOCTYPE = u'<!DOCTYPE html>\n'

    def __init__(self, title, description, keywords, favicon=None, doc_type=TRANSITIONAL_401, lang=u'en'):
        super(Page, self).__init__(u'html', xmlns=u'http://www.w3.org/1999/xhtml', xml_lang=lang, lang=lang)
        self.doc_type = doc_type
        self.head = Head(title, description, keywords, favicon)
        self.body = Body()

    #override
    def as_html(self):
        self.head.propagate_scripts(self)
        self.head.propagate_scripts(self.body)
        self.innerHtml = self.head.as_html()
        self.innerHtml += self.body.as_html()
        return self.doc_type + super(Page, self).as_html()

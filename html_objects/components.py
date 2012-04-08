# coding: utf-8

from copy import copy


class ComponentHtml(object):

    def __init__(self, tag_name, innerHtml='', **kwargs):
        self.tag_name = tag_name
        self.innerHtml = innerHtml
        self.kwargs = kwargs

    def __str__(self):
        return self.as_html()
    
    def as_html(self):
        return ComponentHtml.tag(self.tag_name, self.innerHtml, **self.kwargs)

    def add_component(self, component):
        self.innerHtml += str(component)
        
    def get(self, attr):
        try:
            return self.kwargs[attr]
        except KeyError:
            return None
    
    def set(self, attr, value):
        self.kwargs[attr] = value
        
    def clone(self):
        return copy(self)

    @classmethod
    def attribute_conversion(cls, name):
        if name == 'clazz': return 'class'
        if name == 'xml_lang': return 'xml:lang'
        if name == 'http_equiv': return 'http-equiv'
        return name

    @classmethod
    def tag(cls, tag_name, innerHtml, **kwargs):
        attr_function = lambda key, value: ' %s="%s"' % (cls.attribute_conversion(key), value) if value else ''
        attributes_string = ''.join(attr_function(key, value) for key, value in kwargs.iteritems()) if kwargs else ''
        return '<%s%s>%s</%s>' % (tag_name, attributes_string, innerHtml, tag_name)
    
    @classmethod
    def simple_tag(cls, tag_name, **kwargs):
        attr_function = lambda key, value: ' %s="%s"' % (cls.attribute_conversion(key), value) if value else ''
        attributes_string = ''.join(attr_function(key, value) for key, value in kwargs.iteritems()) if kwargs else ''
        return '<%s%s/>' % (tag_name, attributes_string)


class SimpleComponentHtml(ComponentHtml):

    def as_html(self):
        return ComponentHtml.simple_tag(self.tag_name, **self.kwargs)


class Image(SimpleComponentHtml):

    def __init__(self, src, **kwargs):
        super(Image, self).__init__('img', src=src, **kwargs)


class Link(ComponentHtml):

    def __init__(self, href, innerHtml, target=None, **kwargs):
        super(Link, self).__init__('a', href=href, innerHtml=innerHtml, target=target, **kwargs)


class Paragraph(ComponentHtml):

    def __init__(self, innerHtml, **kwargs):
        super(Paragraph, self).__init__('p', innerHtml=innerHtml, **kwargs)
        

class UnorderedList(ComponentHtml):

    def __init__(self, **kwargs):
        super(UnorderedList, self).__init__('ul', **kwargs)

    #override
    def add_component(self, component):
        if isinstance(component, str):
            super(UnorderedList, self).add_component(ComponentHtml.tag('li', component))
        else:
            super(UnorderedList, self).add_component(component)
            
            
class OrderedList(ComponentHtml):

    def __init__(self, **kwargs):
        super(OrderedList, self).__init__('ol', **kwargs)

    #override
    def add_component(self, component):
        if isinstance(component, str):
            super(OrderedList, self).add_component(ComponentHtml.tag('li', component))
        else:
            super(OrderedList, self).add_component(component)


class Panel(ComponentHtml):

    def __init__(self, innerHtml='', **kwargs):
        super(Panel, self).__init__('div', innerHtml=innerHtml, **kwargs)


class Table(ComponentHtml):
    LINE_CLASSES = ('odd', 'even')

    def __init__(self, **kwargs):
        super(Table, self).__init__('table', **kwargs)
        self._header = ComponentHtml('thead', '')
        self._header_line = None
        self._body = ComponentHtml('tbody', '')
        self._body_line = None
        self._line_index = 0

    def start_header_line(self):
        if self._header_line is not None:
            self._header.add_component(self._header_line)
        self._header_line = ComponentHtml('tr', '')

    def add_cell_on_header(self, content, **kwargs):
        if self._header_line is None:
            self.start_header_line()
        if isinstance(content, str):
            content = ComponentHtml('th', content, **kwargs)
        self._header_line.add_component(content)
        
    def start_line(self):
        if self._body_line is not None:
            self._body.add_component(self._body_line)
        self._body_line = ComponentHtml('tr', '', clazz=Table.LINE_CLASSES[self._line_index % 2])
        self._line_index += 1

    def add_cell(self, content, **kwargs):
        if self._body_line is None:
            self.start_line()
        content = ComponentHtml('td', content, **kwargs)
        self._body_line.add_component(content)

    #override
    def as_html(self):
        self.start_header_line()
        self.start_line()
        self.innerHtml = self._header.as_html()
        self.innerHtml += self._body.as_html()
        return super(Table, self).as_html()


class Form(ComponentHtml):
    def __init__(self, action, method='post', **kwargs):
        super(Form, self).__init__('form', action=action, method=method, **kwargs)
        
    def add_component_with_label(self, label, component):
        panel = ComponentHtml('div', '', clazz='form-label-field')
        panel.add_component(ComponentHtml.tag('div', ComponentHtml.tag('span', label), clazz='form-label'))
        panel.add_component(ComponentHtml.tag('div', component, clazz='form-field'))
        self.add_component(panel)
        
        
class TextBox(SimpleComponentHtml):
    def __init__(self, name, value, maxlength=100, **kwargs):
        super(TextBox, self).__init__('input', type='text', name=name, value=value, maxlength=maxlength, **kwargs)
        

class TextArea(ComponentHtml):
    def __init__(self, name, value, maxlength=500, **kwargs):
        super(TextArea, self).__init__('textarea', name=name, value=value, maxlength=maxlength, **kwargs)


class CheckBox(SimpleComponentHtml):
    def __init__(self, name, **kwargs):
        super(CheckBox, self).__init__('input', type='checkbox', name=name, **kwargs)
        
    #override
    def set(self, attr, value):
        "Checkbox should have value attribute too. We need a trustable and solid standard"
        
        if attr == 'value':
            if value in [True, 'True', 'true', 'on']:
                super(CheckBox, self).set('checked', 'checked')
            else:
                super(CheckBox, self).set('checked', '')
        else:
            super(CheckBox, self).set(attr, value)
            
    def get(self, attr):
        if attr == 'value':
            return True if super(CheckBox, self).get('checked') else False
        else:
            return super(CheckBox, self).get(attr)
        
        
class UploadBox(SimpleComponentHtml):
    def __init__(self, name, value, **kwargs):
        super(UploadBox, self).__init__('input', type='file', name=name, value=value, **kwargs)
        
        
class Select(ComponentHtml):
    def __init__(self, name, multiple=False, **kwargs):
        if multiple:
            multiple = 'multiple'
        else:
            multiple = ''
        super(Select, self).__init__('select', name=name, multiple=multiple, **kwargs)
        self.options = []

    def add_option(self, label, value, selected=False):
        if selected:
            option = ComponentHtml('option', innerHtml=label, value=value, selected='selected')
        else:
            option = ComponentHtml('option', innerHtml=label, value=value)
        self.options.append(option)
        
    def set(self, attr, value):
        "Select should have value attribute too. We need a trustable and solid standard"
        if attr == 'value':
            if isinstance(value, list):
                for v in value:
                    for option in self.options:
                        if str(option.get('value')) == v:
                            option.set('selected', 'selected')
                            break
            else: # only one value
                for option in self.options:
                    if option.get('value') == value:
                        option.set('selected', 'selected')
        else:
            super(Select, self).set(attr, value)
            
    def get(self, attr):
        if attr == 'value':
            if self.get('multiple') == 'multiple':
                values = []
                for option in self.options:
                    if option.get('selected') == 'selected':
                        values.append(option.get('value'))
                return values
            else:
                for option in self.options:
                    if option.get('selected') == 'selected':
                        return option.get('value')
                return None
        else:
            return super(Select, self).get(attr)
            
    #override
    def as_html(self):
        self.innerHtml = ''.join([option.as_html() for option in self.options])
        return super(Select, self).as_html()
        

class SubmitButton(SimpleComponentHtml):
    def __init__(self, id, value, **kwargs):
        super(SubmitButton, self).__init__('input', type='submit', id=id, value=value, **kwargs)
        
        
class Button(ComponentHtml):
    def __init__(self, id, **kwargs):
        super(Button, self).__init__('button', id=id, **kwargs)        
        
        
class Head(ComponentHtml):
    
    def __init__(self, title, description, keywords, favicon, **kwargs):
        super(Head, self).__init__('head', **kwargs)
        self.title = title
        self.description = description
        self.keywords = keywords
        self.favicon = favicon
        self.css_libraries = []
        self.javascript_libraries = []
        self._script = ComponentHtml('script', '', type="text/javascript")
        self.jquery_init_code = ''

    def add_css_library(self, href):
        self.css_libraries.append(href)
    
    def add_javascript_library(self, src):
        self.javascript_libraries.append(src)
        
    def add_javascript_code(self, src):
        self._script += src
        
    def add_jquery_init_code(self, src):
        self.jquery_init_code += src
        
    #override
    def as_html(self):
        self.innerHtml = ComponentHtml.tag('title', self.title)
        self.innerHtml += ComponentHtml.simple_tag('meta', name='description', content=self.description)
        self.innerHtml += ComponentHtml.simple_tag('meta', name='keywords', content=self.keywords)
        self.innerHtml += ComponentHtml.simple_tag('meta', http_equiv='Content-Type', content='text/html;charset=UTF-8')
        if self.favicon:
            self.innerHtml += ComponentHtml.simple_tag('link', rel='shortcut', href=self.favicon)
        for href in self.css_libraries:
            self.innerHtml += ComponentHtml.simple_tag('link', type="text/css", rel="stylesheet", href=href)
        for src in self.javascript_libraries:
            self.innerHtml += ComponentHtml.tag('script', '', type="text/javascript", src=src)
        script = self._script.clone()
        if self.jquery_init_code:
            script.add_component('$(document).ready(function() { %s });' % self.jquery_init_code);
        self.innerHtml += script.as_html()
        return super(Head, self).as_html()
    

class Body(ComponentHtml):
    
    def __init__(self, **kwargs):
        super(Body, self).__init__('body', **kwargs)


class Page(ComponentHtml):
    TRANSITIONAL_401 = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'
    STRICT_401 = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'

    def __init__(self, title, description, keywords, favicon=None, doc_type=TRANSITIONAL_401, lang='en'):
        super(Page, self).__init__('html', xmlns='http://www.w3.org/1999/xhtml', xml_lang=lang, lang=lang)
        self.doc_type = doc_type
        self.head = Head(title, description, keywords, favicon)
        self.body = Body()
        
    #override
    def as_html(self):
        self.innerHtml = self.head.as_html()
        self.innerHtml += self.body.as_html()
        return self.doc_type + super(Page, self).as_html()


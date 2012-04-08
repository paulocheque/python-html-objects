from unittest import TestCase

from html_objects.components import ComponentHtml, Table, Link, Image,\
    UnorderedList, Panel, OrderedList, Form, TextBox, TextArea, SubmitButton,\
    CheckBox, Select

class ComponentHtmlClassTests(TestCase):
    
    def test_create_tag_without_content_and_without_attributes(self):
        self.assertEquals('<x></x>', ComponentHtml.tag('x', ''))
    
    def test_create_tag_with_content_and_without_attributes(self):
        self.assertEquals('<x>y</x>', ComponentHtml.tag('x', 'y'))
    
    def test_create_tag_without_content_and_with_attributes(self):
        self.assertEquals('<x a="b"></x>', ComponentHtml.tag('x', '', a='b'))
        self.assertEquals('<x a="b" c="d"></x>', ComponentHtml.tag('x', '', a='b', c='d'))
    
    def test_create_tag_with_content_and_with_attributes(self):
        self.assertEquals('<x a="b">y</x>', ComponentHtml.tag('x', 'y', a='b'))
        self.assertEquals('<x a="b" c="d">y</x>', ComponentHtml.tag('x', 'y', a='b', c='d'))
        
    def test_clazz_attribute_is_converted_to_class_attribute(self):
        self.assertEquals('<x class="b">y</x>', ComponentHtml.tag('x', 'y', clazz='b'))

    def test_creation_ignore_null_attributes(self):
        self.assertEquals('<x></x>', ComponentHtml.tag('x', '', a=None))


class ComponentHtmlInstanceTests(TestCase):
    
    def test_create_tag_without_content_and_without_attributes(self):
        self.component = ComponentHtml('x')
        self.assertEquals('<x></x>', self.component.as_html())
    
    def test_create_tag_with_content_and_without_attributes(self):
        self.component = ComponentHtml('x', 'y')
        self.assertEquals('<x>y</x>', self.component.as_html())
    
    def test_create_tag_without_content_and_with_attributes(self):
        self.component = ComponentHtml('x', '', a='b')
        self.assertEquals('<x a="b"></x>', self.component.as_html())
        self.component = ComponentHtml('x', '', a='b', c='d')
        self.assertEquals('<x a="b" c="d"></x>', self.component.as_html())
    
    def test_create_tag_with_content_and_with_attributes(self):
        self.component = ComponentHtml('x', 'y', a='b')
        self.assertEquals('<x a="b">y</x>', self.component.as_html())
        self.component = ComponentHtml('x', 'y', a='b', c='d')
        self.assertEquals('<x a="b" c="d">y</x>', self.component.as_html())
        
    def test_get_return_value_of_the_attribute(self):
        self.component = ComponentHtml('x', 'y', a='b')
        self.assertEquals('b', self.component.get('a'))
        
    def test_get_return_value_of_a_inexistent_attribute_must_return_None(self):
        self.component = ComponentHtml('x', 'y')
        self.assertEquals(None, self.component.get('a'))
        
    def test_set_value_of_the_attribute(self):
        self.component = ComponentHtml('x', 'y', a='b')
        self.component.set('a', 'c')
        self.assertEquals('c', self.component.get('a'))
        

class ImageTests(TestCase):
    
    def test_src_attribute_is_mandatory(self):
        image = Image('/x.jpg')
        self.assertEquals('<img src="/x.jpg"/>', image.as_html())
    
    
class LinkTests(TestCase):
    
    def test_href_and_content_attributes_are_mandatory(self):
        link = Link('/y', 'x')
        self.assertEquals('<a href="/y">x</a>', link.as_html())
    
    def test_content_can_be_a_html_component(self):
        link = Link('/y', Image('/x.jpg'))
        self.assertEquals('<a href="/y"><img src="/x.jpg"/></a>', link.as_html())


class UnorderedListTests(TestCase):
    
    def test_create_an_empty_list(self):
        ul = UnorderedList()
        self.assertEquals('<ul></ul>', ul.as_html())
        
    def test_create_a_list_with_one_item(self):
        ul = UnorderedList()
        ul.add_component('x')
        self.assertEquals('<ul><li>x</li></ul>', ul.as_html())
        
    def test_create_a_list_with_two_items(self):
        ul = UnorderedList()
        ul.add_component('x')
        ul.add_component('y')
        self.assertEquals('<ul><li>x</li><li>y</li></ul>', ul.as_html())
        
    def test_items_can_be_components_too(self):
        ul = UnorderedList()
        ul.add_component(ComponentHtml('li', 'x'))
        ul.add_component(ComponentHtml('li', 'y'))
        self.assertEquals('<ul><li>x</li><li>y</li></ul>', ul.as_html())
        
    def test_items_can_have_strings_and_components_in_the_same_list(self):
        ul = UnorderedList()
        ul.add_component(ComponentHtml('li', 'x'))
        ul.add_component('y')
        self.assertEquals('<ul><li>x</li><li>y</li></ul>', ul.as_html())


class OrderedListTests(TestCase):
    
    def test_create_an_empty_list(self):
        ol = OrderedList()
        self.assertEquals('<ol></ol>', ol.as_html())
        
    def test_create_a_list_with_one_item(self):
        ol = OrderedList()
        ol.add_component('x')
        self.assertEquals('<ol><li>x</li></ol>', ol.as_html())
        
    def test_create_a_list_with_two_items(self):
        ol = OrderedList()
        ol.add_component('x')
        ol.add_component('y')
        self.assertEquals('<ol><li>x</li><li>y</li></ol>', ol.as_html())
        
    def test_items_can_be_components_too(self):
        ol = OrderedList()
        ol.add_component(ComponentHtml('li', 'x'))
        ol.add_component(ComponentHtml('li', 'y'))
        self.assertEquals('<ol><li>x</li><li>y</li></ol>', ol.as_html())
        
    def test_items_can_have_strings_and_components_in_the_same_list(self):
        ol = OrderedList()
        ol.add_component(ComponentHtml('li', 'x'))
        ol.add_component('y')
        self.assertEquals('<ol><li>x</li><li>y</li></ol>', ol.as_html())
        

class PanelTests(TestCase):

    def test_create_an_empty_panel(self):
        panel = Panel()
        self.assertEquals('<div></div>', panel.as_html())
        
    def test_panel_can_have_initial_content(self):
        panel = Panel('x')
        self.assertEquals('<div>x</div>', panel.as_html())
        
    def test_panel_can_have_initial_content_as_a_component(self):
        panel = Panel(Image('y'))
        self.assertEquals('<div><img src="y"/></div>', panel.as_html())
        
    def test_panel_can_receive_strings(self):
        panel = Panel()
        panel.add_component('x')
        self.assertEquals('<div>x</div>', panel.as_html())
        
    def test_panel_can_receive_components(self):
        panel = Panel()
        panel.add_component(Image('y'))
        self.assertEquals('<div><img src="y"/></div>', panel.as_html())
        
    def test_panel_can_receive_strings_and_components(self):
        panel = Panel()
        panel.add_component('x')
        panel.add_component(Image('y'))
        self.assertEquals('<div>x<img src="y"/></div>', panel.as_html())


class TableTests(TestCase):
    
    def test_empty_table_has_empty_header_and_empty_body(self):
        table = Table()
        self.assertEquals('<table><thead></thead><tbody></tbody></table>', table.as_html())
        
    def test_it_is_possible_to_add_cells_on_header_in_a_line_that_was_created(self):
        table = Table()
        table.start_header_line()
        table.add_cell_on_header('x')
        self.assertEquals('<table><thead><tr><th>x</th></tr></thead><tbody></tbody></table>', table.as_html())
        
    def test_it_is_possible_to_add_cells_on_header_without_starting_a_new_line(self):
        table = Table()
        table.add_cell_on_header('x')
        self.assertEquals('<table><thead><tr><th>x</th></tr></thead><tbody></tbody></table>', table.as_html())
        
    def test_it_is_possible_to_add_many_lines_on_header(self):
        table = Table()
        table.add_cell_on_header('x')
        table.add_cell_on_header('y')
        table.start_header_line()
        table.add_cell_on_header('z')
        self.assertEquals('<table><thead><tr><th>x</th><th>y</th></tr><tr><th>z</th></tr></thead><tbody></tbody></table>', table.as_html())
        
    def test_it_is_possible_to_add_cells_on_a_body_line_that_was_started_and_the_line_will_have_default_class_style(self):
        table = Table()
        table.start_line()
        table.add_cell('x')
        self.assertEquals('<table><thead></thead><tbody><tr class="odd"><td>x</td></tr></tbody></table>', table.as_html())

    def test_it_is_possible_to_add_cells_on_body_without_start_a_new_line(self):
        table = Table()
        table.add_cell('x')
        self.assertEquals('<table><thead></thead><tbody><tr class="odd"><td>x</td></tr></tbody></table>', table.as_html())
        
    def test_it_is_possible_to_add_many_lines_on_body_and_lines_has_default_class_styles(self):
        table = Table()
        table.add_cell('x')
        table.add_cell('y')
        table.start_line()
        table.add_cell('z')
        self.assertEquals('<table><thead></thead><tbody><tr class="odd"><td>x</td><td>y</td></tr><tr class="even"><td>z</td></tr></tbody></table>', table.as_html())


class FormTests(TestCase):
    
    def test_action_is_mandatory_and_default_method_is_post(self):
        form = Form('x')
        self.assertEquals('<form action="x" method="post"></form>', form.as_html())
        
    def test_method_can_be_get(self):
        form = Form('x', method='get')
        self.assertEquals('<form action="x" method="get"></form>', form.as_html())
        
        
class TextBoxTests(TestCase):
    
    def test_name_and_value_are_mandatory_and_id_will_be_the_same_as_the_name(self):
        text_box = TextBox('x', 'y')
        self.assertEquals('<input type="text" name="x" value="y" maxlength="100"/>', text_box.as_html())

        
class TextAreaTests(TestCase):
    
    def test_name_and_value_are_mandatory_and_id_will_be_the_same_as_the_name(self):
        text_area = TextArea('x', 'y')
        self.assertEquals('<textarea name="x" value="y" maxlength="500"></textarea>', text_area.as_html())
        

class SubmitButtonTests(TestCase):
    
    def test_id_and_value_are_mandatory(self):
        button = SubmitButton('x', 'y')
        self.assertEquals('<input type="submit" id="x" value="y"/>', button.as_html())


class CheckBoxTests(TestCase):
    
    def test_name_is_mandatory(self):
        component = CheckBox('x')
        self.assertEquals('<input type="checkbox" name="x"/>', component.as_html())
        
    def test_set_value_is_the_same_check_the_checkbox(self):
        component = CheckBox('x')
        component.set('value', True)
        self.assertEquals('<input type="checkbox" checked="checked" name="x"/>', component.as_html())
        
    def test_get_value(self):
        component = CheckBox('x')
        self.assertEquals(False, component.get('value'))
        component.set('value', True)
        self.assertEquals(True, component.get('value'))
        

class SelectTests(TestCase):
    
    def test_name_is_mandatory(self):
        component = Select('x')
        self.assertEquals('<select name="x"></select>', component.as_html())
        
    def test_multiple_select(self):
        component = Select('x', multiple=True)
        self.assertEquals('<select multiple="multiple" name="x"></select>', component.as_html())
        
    def test_can_add_options(self):
        component = Select('x')
        component.add_option('a', 'b')
        self.assertEquals('<select name="x"><option value="b">a</option></select>', component.as_html())
        
    def test_can_add_selected_options(self):
        component = Select('x')
        component.add_option('a', 'b', selected=True)
        self.assertEquals('<select name="x"><option selected="selected" value="b">a</option></select>', component.as_html())
        
    def test_set_value_select_options_with_the_value(self):
        component = Select('x')
        component.add_option('a', 'b')
        component.set('value', 'b')
        self.assertEquals('<select name="x"><option selected="selected" value="b">a</option></select>', component.as_html())
        
    def test_set_value_accept_multiple_values(self):
        component = Select('x')
        component.add_option('a', 'b')
        component.set('value', ['b'])
        self.assertEquals('<select name="x"><option selected="selected" value="b">a</option></select>', component.as_html())
        
    def test_get_value_return_value_if_multiple_selection_is_false(self):
        component = Select('x', multiple=False)
        component.add_option('a', 'b')
        self.assertEquals(None, component.get('value'))
        component.set('value', 'b')
        self.assertEquals('b', component.get('value'))
    
    def test_get_value_return_list_of_values_if_multiple_selection_is_true(self):
        component = Select('x', multiple=True)
        component.add_option('a', 'b')
        self.assertEquals([], component.get('value'))
        component.set('value', ['b'])
        self.assertEquals(['b'], component.get('value'))
        
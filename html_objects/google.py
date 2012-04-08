# coding: utf-8

from html_objects.components import Panel, Link, Image


class GoogleAdSenseComponent(Panel):

    def __init__(self, client, slot, width, height, **kwargs):
        super(GoogleAdSenseComponent, self).__init__(**kwargs)
        adsense_code = """<script type="text/javascript"><!--
google_ad_client = "%s";
google_ad_slot = "%s";
google_ad_width = %s;
google_ad_height = %s;
//-->
</script>
<script type="text/javascript"
src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
</script>""" % (client, slot, width, height)
        self.add_component(adsense_code)


class GoogleAnalyticsComponent(Panel):
    
    def __init__(self, id, **kwargs):
        super(GoogleAnalyticsComponent, self).__init__(clazz='google-analytics', **kwargs)
        ga_code = r"""
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '%s']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
""" % id
        self.add_component(ga_code)


class GoogleMapsComponent(Panel):
    
    def __init__(self, address, size='200x200', zoom='16', **kwargs):
        super(GoogleMapsComponent, self).__init__(clazz='google-maps', **kwargs)
        href = 'http://maps.google.com/maps/api/staticmap?center=%s&zoom=%s&size=%s&sensor=true&markers=color:blue%s' % (address, zoom, size, address)
        self.add_component(Link(href, address, target='_blank'))
        self.add_component(self.tag('br', ''))
        self.add_component(Link(href, Image(href), target='_blank'))
    
from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.core.urlresolvers import reverse
from django.forms.widgets import flatatt
from django.utils.html import escape
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode



class impressao(forms.Textarea):
    """
    Aqui eu crio um widget com um botão que será usado para ligar acionar o Hamster II e pegar a digital.
    """
    def render(self,name,value,attrs=None):
        if value is None: value=''
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs,name=name)

        if value:
            saidabtn = mark_safe(u'<input type=hidden %s value=%s /><input type=button name="btnfinger" value="Recapturar Digitais" onclick="document.getElementById(%s).value=registradigital();">' % (flatatt(final_attrs), value, "'id_Impressao'"))
        else:
            saidabtn = mark_safe(u'<input type=hidden %s value=%s /><input type=button name="btnfinger" value="Capturar Digitais" onclick="document.getElementById(%s).value=registradigital();">' % (flatatt(final_attrs), value, "'id_Impressao'"))            

        return saidabtn

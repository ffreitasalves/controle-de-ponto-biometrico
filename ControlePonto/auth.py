# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings
from string import lower
import ldap
###TESTE
from django.http import HttpResponseRedirect

class ActiveDirectoryBackend:


  def is_valid (self,username=None,password=None):
    ## Disallowing null or blank string as password
    ## as per comment: http://www.djangosnippets.org/snippets/501/#c868
    binddn = "%s@%s" % (username,settings.AD_NT4_DOMAIN)
    if password == None or password == '':
      return False
    try:
      l = ldap.initialize(settings.AD_LDAP_URL)
      l.simple_bind_s(binddn,password)
      l.unbind_s()
      return True
    except ldap.LDAPError:
      return False

  def have_permission(self, username,password):
    SEARCH_LEVEL = {
        'BASE': ldap.SCOPE_BASE,
        'ONELEVEL': ldap.SCOPE_ONELEVEL,
        'SUBTREE': ldap.SCOPE_SUBTREE
      }
    AD_LEVEL = SEARCH_LEVEL[settings.SEARCH_LEVEL]
    binddn = "%s@%s" % (username,settings.AD_NT4_DOMAIN)
    result = False
    for search_dn in settings.AD_SEARCH_DN:
      l = ldap.initialize(settings.AD_LDAP_URL)
      l.simple_bind_s(binddn,password)
      if result == False:
        try:
          result = l.search_ext_s(search_dn,AD_LEVEL, "sAMAccountName=%s" % username,settings.AD_SEARCH_FIELDS)[0][1]
        except:
          result = False
      l.unbind_s()
      

    flag = False
    if result:
      for group in settings.AD_GROUP_DN:
        if group.lower() in map(lower,result['memberOf']):
          flag = "simples"     
      for group in settings.AD_ADMGROUP_DN:
        if group.lower() in map(lower,result['memberOf']):
          flag = "adm"     

    return flag


  def authenticate(self,username=None,password=None):
    if not self.is_valid(username,password):
      return None
    
    perm = self.have_permission(username, password)

    try:
      user = User.objects.get(username=username.lower())
    except User.DoesNotExist:
      user = User(username=username.lower(), first_name=username, email='%s@%s' % (username,settings.AD_NT4_DOMAIN))

    if perm == "adm":      
      user.is_staff = True
      user.is_superuser = True
      user.set_password(password)
      user.save()
    elif perm=="simples":
      user.is_staff = False
      user.is_superuser = False
      user.set_password(password)
      user.save()
    else:
      return None
      
    return user

  def get_user(self,user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None

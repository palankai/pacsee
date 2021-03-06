from django.db import models
from xadrpy.models.inheritable import Inheritable
from xadrpy.models.fields.json_field import JSONField
from django.utils.translation import ugettext_lazy as _
from xadrpy.utils.signals import autodiscover_signal
from django.dispatch.dispatcher import receiver
import conf
from xadrpy.utils.imports import get_class
from django.db.models import Q
import logging
from django.template.loader import find_template
from django.template import loader
from django.template.base import TemplateDoesNotExist
from django.contrib.staticfiles import finders
from xadrpy.models.fields.dict_field import DictField

logger = logging.getLogger("xadrpy.contrib.themes.models")

class ThemeAdjuster(models.Model):
    
    class Meta:
        abstract = True
    
    def setup_theme(self, theme, request, view, args, kwargs):
        pass

class DefaultDict(dict):
    def set_default(self, default):
        self.default = default
        return self

    def __unicode__(self):
        return self[self.default]

    def __getattr__(self, name):
        return self[name]

class AttrCaller(object):
    def __init__(self, method, default):
        self.method = method
        self.default = default
    
    def __getitem__(self, name):
        return DefaultDict(self.method(name)).set_default(self.default)

    def __getattr__(self, name):
        return DefaultDict(self.method(name)).set_default(self.default)

#    def __call__(self):
#        return self.__unicode__()
#    
#    def __str__(self):
#        return self.__unicode__()
#    
#    def __unicode__(self):
#        return self.method(self.default)

class Theme(Inheritable):
    name = models.CharField(max_length=255, unique=True)
    meta = JSONField()
    utime = models.DateTimeField(blank=True, null=True)
    files = DictField()
    
    class Meta:
        verbose_name=_("Theme")
        verbose_name_plural=_("Themes")
        db_table = "xadrpy_themes_theme"

    def get_base_path(self):
        if hasattr(self, "_base_path"):
            return self._base_path
        self._base_path = "themes/%s/" % (self.meta['name'])
        if self.meta['type']:
            self._base_path = "%s/%s" % (self.meta['type'], self._base_path)
        return self._base_path

    def get_middle_path(self):
        return "x-theme/"

    def get_top_path(self):
        return "x-theme/themes/%s/" % self.name


    def get_base_html(self):
        return self.get_base_path() + self.meta['layouts'][0]['name']
    
    def get_styles(self):
        for style in self.meta['styles']:
            yield self.get_base_path() + style
    
    def get_scripts(self):
        for script in self.meta['scripts']:
            yield self.get_base_path() + script
        
    def get_libraries(self):
        libs = self.meta['libs']+conf.DEFAULT_LIBRARIES
        return Library.objects.filter(Q(autoload=True)|Q(name__in=libs))

    def template(self, name=None):
        if not name: return AttrCaller(self.template, "file")
        return self.get_files("html", self.meta['templates'][name]['source'])

    def style(self, name=None):
        if not name: return AttrCaller(self.style, "file")
        return self.get_files("html", self.meta['templates'][name]['source'])

    def media(self, name=None):
        if not name: return AttrCaller(self.media, "file")
        return self.get_files("media", self.meta['media'][name]['source'])

    def script(self, name=None):
        if not name: return AttrCaller(self.script, "file")
        return self.get_files("html", self.meta['templates'][name]['source'])

    
    def get_files(self, file_type, name):
        return self.files[file_type][name]
    
    def collect_files(self):
        logger.info("Collecting files of %s theme.", self.name)
        try:
            self._files = {}
            base_files = self.meta['files']
            self._collect_files(base_files)
            self.files = self._files
            self.save() 
        except Exception, e:
            logger.exception(unicode(e))
            raise e
    
    def _collect_files(self, base_files):
        for file_type in self._get_file_types():
            self._files[file_type] = self._collect_type(file_type, base_files[file_type])
    
    def _collect_type(self, file_type, base_files):
        files = []
        for base_file in base_files:
            if file_type in self._get_static_file_types():
                files_tripple = self._collect_static_file(file_type, base_file) 

            if file_type in self._get_template_file_types():
                files_tripple = self._collect_template_file(file_type, base_file)

            file_list = [file_name for file_name in files_tripple if file_name]
            if base_file['required']:
                assert file_list, "File '%s' not found for %s theme" % (base_file['file_name'], self.name)
            files.append((base_file['name'], dict(base_file, 
                                                  files_tripple=files_tripple, 
                                                  files=file_list,
                                                  base_file=file_list and file_list[0] or None,
                                                  top_file=file_list and file_list[-1] or None,
                                                  file=file_list and file_list[-1] or None,
                                                  middle_file=file_list and file_list[:2][-1] or None)))
        return dict(files)
    
    def _collect_static_file(self, file_type, base_file):
        a,b,c = self._get_prefix_triple()

        file_list = base_file['file_name']
        if not isinstance(file_list, (list, tuple)):
            file_list=[file_list]
        
        for f in file_list:
            ra,rb,rc = (finders.find(a+f) and a+f, 
                    finders.find(b+f) and b+f, 
                    finders.find(c+f) and c+f)
            if ra or rb or rc: break
        return ra,rb,rc
    
    def _collect_template_file(self, file_type, base_file):
        a,b,c = self._get_prefix_triple()

        file_list = base_file['file_name']
        if not isinstance(file_list, (list, tuple)):
            file_list=[file_list]
            
        for f in file_list:
            ra,rb,rc =  (self._find_template(a+f) and a+f,
                         self._find_template(b+f) and b+f,
                         self._find_template(c+f))
            if ra or rb or rc: break
        return ra,rb,rc

    def _find_template(self, path):
        for template_loader in loader.template_source_loaders:
            try: 
                template_loader.load_template_source(path)
                return path
            except TemplateDoesNotExist: pass
        return None

    def _get_file_types(self):
        return self._get_static_file_types()+self._get_template_file_types()

    def _get_static_file_types(self):
        return ['style', 'script', 'media']

    def _get_template_file_types(self):
        return ['html']

    def _get_prefix_triple(self):
        return (self.get_base_path(), self.get_middle_path(), self.get_top_path())

class Library(Inheritable):
    name = models.CharField(max_length=255, unique=True)
    autoload = models.BooleanField(default=False, db_index=True)
    meta = JSONField()
    utime = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name=_("Library")
        verbose_name_plural=_("Libraries")
        db_table = "xadrpy_themes_library"

    def get_styles(self):
        for style in self.meta['styles']:
            yield self.get_base_path() + style

    def get_scripts(self):
        for script in self.meta['scripts']:
            yield self.get_base_path() + script

    def get_base_path(self):
        if hasattr(self, "_base_path"):
            return self._base_path
        self._base_path = "libs/"
        if self.meta['type']:
            self._base_path = "%s/%s" % (self.meta['type'], self._base_path)
        return self._base_path


@receiver(autodiscover_signal)
def init_theme_loaders(**kwargs):
    import loaders
    find_template("xadrpy/themes/base.html") #Hack: init template loaders
    for loader_name in conf.THEME_LOADERS:
        theme_loader_cls = get_class(loader_name, loaders.ThemeLoader)
        theme_loader = theme_loader_cls()
        theme_loader.load()

import json
from aioweb.db.model_codecs import json_dumps
import pystache


class HtmlRenderer(object):
    template_dirs = ['./html']

    def __init__(self, template_dirs=None):
        self.template_dirs = template_dirs + self.template_dirs

    def render_scripts(self, scripts):
        def _render_scripts(scripts):
            _rscripts = []
            for script in scripts:
                rscript = "<script src='%(src)s' " % script
                if 'media' in script:
                    rscript += "media='%(media)s" % script
                rscript +=  "></script>"
                _rscripts.append(rscript)
            return "\n".join(_rscripts)

        def add_scripts(text):
            try:
                tscripts = json.loads(text)
            except Exception as e:
                tscripts = []
            if isinstance(tscripts, list):
                tscripts.extend(scripts)
            return _render_scripts(tscripts)
        return add_scripts

    def render(self, template_name, *args, **kwargs):
        kwargs['scripts'] = self.render_scripts(kwargs.get('scripts', []))
        renderer = pystache.Renderer(search_dirs=self.template_dirs)
        return renderer.render_name(template_name, *args, **kwargs).encode()


class JsonRenderer():
    def render(self, *args, **kwargs):
        if args:
            return json_dumps(args[0]).encode()
        return json_dumps(kwargs).encode()
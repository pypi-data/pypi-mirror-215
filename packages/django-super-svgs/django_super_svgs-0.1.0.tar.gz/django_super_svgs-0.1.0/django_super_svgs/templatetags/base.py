import importlib
import os
import re
import sys

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template import Node, TemplateSyntaxError
from django.utils.regex_helper import _lazy_re_compile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class BaseTemplateTag(Node):
    kwargs_re = _lazy_re_compile(r"(\w+:)?([a-zA-Z-_]+)=(.+)")
    SVGS_BASE = ["hero_solid", "hero_outline", "dripicons"]
    SVG_CONTAINER_CLASS = "svg-container"
    ERROR_MSG = _(
        'The svg tag requires a svg filename followed by svg name and optionally followed by a list of attributes and values like attr="value"'
    )

    def __init__(self, parser, token):
        self.parser = parser
        self.token = token
        self.tag_name, *self.bits = token.split_contents()
        self.kwargs, self.dot_kwargs = self.token_kwargs(
            self.bits, self.parser
        )
        self.args = list(filter(lambda x: not x.__contains__("="), self.bits))
        self.container_classes = getattr(
            settings,
            "SUPER_SVGS_CONTAINER_CLASSES",
            self.SVG_CONTAINER_CLASS,
        )

    def token_kwargs(self, bits, parser):
        kwargs = {}
        dot_kwargs = {}

        for bit in bits:
            match = self.kwargs_re.match(bit)
            if match:
                mg = match.groups()
                if mg:
                    if mg[0]:
                        key = mg[0].strip(":")
                        value = {mg[1]: parser.compile_filter(mg[2])}
                        if key in dot_kwargs.keys():
                            dot_kwargs.get(key).append(value)
                        else:
                            dot_kwargs[key] = [value]

                        continue
                    kwargs[mg[1]] = parser.compile_filter(mg[2])
            continue
        return kwargs, dot_kwargs


class RenderSvg(BaseTemplateTag):
    def __init__(self, parser, token):
        super().__init__(parser, token)

    def _parse_kwargs(self):
        for k, v in self.kwargs.items():
            if v.var.startswith("{{"):
                var_from_token = re.sub(r"[}{\s]", "", v.var)
                self.tags += f'{k}="{self.context.get(var_from_token, "")}"'
            else:
                self.tags += f'{k}="{v.var}" '

        if "class" in self.kwargs.keys():
            self.classes = self.kwargs.get("class").var

    def _parse_dot_kwargs(self):
        if "svg" in self.dot_kwargs.keys():
            self.svg_tags = self.dot_kwargs.get("svg")

        if "path" in self.dot_kwargs.keys():
            self.path_tags = self.dot_kwargs.get("path")

    def _parse_args(self):
        self.svg_name = self.args[0]
        self.svg_file = None
        if len(self.args) > 1:
            self.svg_name = self.args[1]
            self.svg_file = self.args[0]

    def _render(self):
        apps_finder = finders.AppDirectoriesFinder()
        apps_list = list(
            filter(
                lambda x: x[0].__contains__(f"svgs/{self.svg_file}.py"),
                apps_finder.list(ignore_patterns=["admin", "__pycache__"]),
            )
        )
        self.svg_path = ""
        if apps_list:
            self.svg_path = os.path.join(
                apps_list[0][1].location, apps_list[0][0]
            )
        module_name = self.svg_file

        if self.svg_file not in self.SVGS_BASE:
            if self.svg_path:
                if os.path.dirname(self.svg_path) not in sys.path:
                    sys.path.append(os.path.dirname(self.svg_path))
                importlib.import_module(self.svg_file)
        else:
            module_name = (
                f"django_super_svgs.templatetags.svgs.{self.svg_file}"
            )

        self.html = f"""
            <div class="{self.container_classes} {self.classes}" {self.tags}>
                {getattr(sys.modules.get(module_name), self.svg_name, "")}
            </div>
        """

        for tag in self.svg_tags:
            for k, v in tag.items():
                pattern = rf"{k}=\"[#A-Za-z0-9]+\""
                sub = re.findall(r"<svg.*>", self.html)[0]
                new_sub = re.findall(pattern, sub)
                if not new_sub:
                    ns = re.sub(r"<svg\s", f'<svg {k}="{v.var}"', sub)
                    self.html = self.html.replace(sub, ns)
                for n in new_sub:
                    self.html = self.html.replace(n, f'{k}="{v.var}"')

        for p in self.path_tags:
            for k, v in p.items():
                pattern = rf"{k}=\"[#A-Za-z0-9]+\""
                sub = re.findall(r"<path.*>", self.html)
                for s in sub:
                    new_sub = re.findall(pattern, s)
                    if not new_sub:
                        ns = re.sub(r"<path\s", f'<path {k}="{v.var}"', s)
                        self.html = self.html.replace(s, ns)
                    for n in new_sub:
                        self.html = self.html.replace(n, f'{k}="{v.var}"')

        return mark_safe(self.html)

    def render(self, context):
        self.path_tags = {}
        self.svg_tags = {}
        self.classes = ""
        self.tags = ""
        self.context = context

        if len(self.args) < 2:
            raise TemplateSyntaxError(self.ERROR_MSG)

        self._parse_args()

        self._parse_kwargs()

        self._parse_dot_kwargs()

        return self._render()

#!/usr/bin/python3
# coding: utf-8

import sys
import os
import json
import jinja2


path    = "./build"
jnj_tex = jinja2.Environment(
    loader                = jinja2.FileSystemLoader(os.path.abspath('.')),
    block_start_string    = "%<",
    block_end_string      = ">%",
    variable_start_string = "< print",
    variable_end_string   = ">",
    comment_start_string  = "%<#",
    comment_end_string    = ">%",
    line_statement_prefix = "%py",
    line_comment_prefix   = "%#py",
    trim_blocks           = True,
    autoescape            = False,
)


class AttrDict (dict):
    def __init__ (self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load_json (path):
    with open(path, 'r') as json_file:
        return AttrDict(json.load(json_file))


def main ():
    data = load_json("pt-br.json")
    tex  = jnj_tex.get_template("content.tex").render(
        detail      = data.detail,
        experiences = data.experiences,
        educations  = data.educations,
        skills      = data.skills,
    )
    
    if not os.path.isdir(path):
        os.mkdir(path)

    file_name = os.path.join(path, "output.tex")
    with open(file_name, 'w') as tex_file:
        tex_file.write(tex)


if __name__ == "__main__": main()

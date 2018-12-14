import sys
import os
import json
import re

# {{{
def main (args):
    check_parameters_amount(args)
    check_file_exist(args[1])
    check_file_exist(args[2])
    check_directory_exist(args[3])

    dictionary  = load_json_file(args[1])
    template    = load_template_file(args[2])
    path_output = "%s/output.tex" % args[3]

    output = parser(template, dictionary)

    #save_output_file(path_output, output) # TODO DESCOMENTAR ESSA LINHA
    sys.exit(0)

# }}}
def parser (template, dictionary):
    import pdb
    stack = list()

    index = 0
    size = len(template)
    while index < size:
        char = template[index]

        if char == '<':
            stack.append(index)

        elif char == '>':
            start = stack.pop(-1)
            end   = index+1

            value = get_value(template[start:end], dictionary)

            first_part = template[:start]
            last_part = template[end:]
            template = first_part + value + last_part

            size = len(template)
            index = start + len(value)

        index += 1

    return template

def get_value (s, d):

    result = re.search(r'^< ([A-z0-9-]*[A-z0-9\.-]*) >$', s)

    if result:
        keys = result.group(1).split('.')
        c = d
        for key in keys:
            if key in c.keys():
                c = c[key]
            else:
                return s

        return c
    else:
        return s


# {{{
def save_output_file (path_output, output):
    try:
        output_file = open(path_output, "w")
        output_file.write(output)
        output_file.close()
    except:
        error_msg("Falha inesperada no salvamento do arquivo '%s'" % path_output, 7)


def load_template_file (path_file):
    template = None
    try:
        with open(path_file, "r", encoding='utf-8') as template_file:
            template = template_file.read()
            template_file.close()
    except:
        error_msg("Falha inesperada durante carregamento do arquivo template", 5)

    return template


def load_json_file (path_file):
    dictionary = dict()
    try:
        with open(path_file, "r") as json_file:
            dictionary = json.load(json_file)
            json_file.close()

    except json.JSONDecodeError:
        error_msg("Arquivo json '%s' contem erros" % path_file, 3)

    except:
        error_msg("Falha inesperada durante carregamento do arquivo json", 4)

    return dictionary
# }}}
# {{{
def check_parameters_amount (args):
    if (len(args)) < 4:
        error_msg("Quantidade de parametros invalida.", 1)


def check_directory_exist (d):
    return True # TODO REMOVER ESSA LINHA
    if not os.path.isdir(d):
        warning_msg("Diretorio '%s' nao existe." % d)
        try:
            os.mkdir(d)
        except:
            error_msg("Falha ao criar diretorio '%s'" % d, 6)


def check_file_exist (f):
    if not os.path.exists(f):
        error_msg("Arquivo '%s' nao existe" % f, 2)
# }}}
# {{{
def sucess_msg (msg):
    print("\33[32m%s\033[0m" % msg)


def warning_msg (msg):
    print("\n\33[5;33mWARNING: %s\033[0m\n" % msg.upper())


def error_msg (msg, exit_code):
    print("\n\33[41mERROR: %s\033[0m\n" % msg)
    sys.exit(exit_code)
# }}}

if __name__ == "__main__": main(sys.argv)

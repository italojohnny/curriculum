import time
import sys
import os
import json
import re

variable  = r'[A-z_][\w_-]*'
variables = r'(%s)(\.%s)*' % (variable, variable)
t_print   = re.compile(r'< print (%s) >' % variables)
t_for     = re.compile(r'< for (%s) in (%s) >(.*?)< endfor >' % (variable, variables), re.M | re.S)
t_if      = re.compile(r'< if (%s) >(.*?)< endif >' % variables, re.M | re.S)


# {{{
def main (args):
    check_parameters_amount(args)
    check_file_exist(args[1])
    check_file_exist(args[2])
    check_directory_exist(args[3])

    dictionary  = load_json_file(args[1])
    template    = load_template_file(args[2])
    path_output = "%s/output.tex" % args[3]

    output = compiler(template, dictionary)
    save_output_file(path_output, output)
    #sys.exit(0)


def get_value (string, dictionary):
    value = dictionary
    keys = string.split('.')
    for key in keys:
        if key in value.keys():
            value = value[key]
        else:
            return string
    return value
# }}}
# {{{
def save_output_file (path_output, output):
    try:
        output_file = open(path_output, "w")
        output_file.write(output)
        output_file.close()
    except Exception as e:
        error_msg("Falha inesperada no salvamento do arquivo '%s'\n%s" % (path_output, e), 7)


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

def compiler (template, dictionary):
    index = 0
    size = len(template)
    stack = list()

    while index < size:
        char = template[index]

        if char == '<':
            stack.append(index)

        if char == '>' and len(stack) > 0:
            start = stack.pop(-1)
            end   = index +1
            tag   = template[start:end]

            if tag.startswith('< print'):
                result = t_print.search(template)
                value = get_value(result.group(1), dictionary)
                template = t_print.sub(value, template, 1)
                index = 0
                size = len(template)

            elif tag.startswith('< for'):
                result = t_for.search(template)
                values = get_value(result.group(2), dictionary)
                iterator = result.group(1)
                last_element = len(result.groups())

                sub_template = result.group(last_element)
                sub_dictionary = dictionary
                new_template = ""
                for i, value in enumerate(values):
                    sub_dictionary[iterator] = values[i]
                    new_template += compiler(sub_template, sub_dictionary)
                template =  template[:result.span()[0]] + \
                        new_template + \
                        template[result.span()[1]:]
                index = 0
                size = len(template)

        index += 1
    return template


if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv)
    print("%s seconds" % (time.time() - start_time))
    sys.exit(0)

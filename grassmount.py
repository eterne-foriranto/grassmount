#!/usr/bin/python
from os import path
from sys import path as syp
from subprocess import Popen
syp.append(path.expanduser('~/lib'))

from stmod import remove_comment as rc
from stmod import readfile
from argparse import ArgumentParser

default = path.expanduser('~') + '/.config/grassmount.cs'
#default = path.expanduser('~') + '/.config/grassmount'
parser = ArgumentParser()
parser.add_argument('-r', dest = 'flag', default = ['normal'], action = 'store_const', const = ['repair', 'normal'])
parser.add_argument('-u', dest = 'flag', default = ['normal'], action = 'store_const', const = ['repair'])
parser.add_argument('config', default = default, nargs = '?')
namespace = parser.parse_args()
config = namespace.config

lines = readfile(config)

def loop(mode):
    prefices = {'normal':'sshfs ', 'repair':'fusermount -u -z '}
    for line in lines:
        line = rc(line, '#')
        if '@' in line:
            keys = [i.replace('\n', '') for i in line.split()]
            options = ''
            if len(keys) == 3:
                options = '-o ' + keys[2].replace('\n', '')
            cmds = {
                    'normal':prefices[mode] + options + ' ' + keys[0] + ' ' + keys[1],
                    'repair':prefices[mode] + keys[1]
                    }
            #print(kline['counter'])
            print(cmds[mode])
            p = Popen(cmds[mode], shell = True)
            p.wait()
for mode in namespace.flag:
    loop(mode)

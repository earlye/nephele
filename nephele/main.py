#!/usr/bin/env python3

import argparse
import atexit
import boto3
import cmd

import json
import os
import readline
import shlex
import subprocess
import sys
import traceback
import yaml

from nephele import Config
from nephele.AwsProcessor import AwsProcessor
from nephele.AwsProcessorFactoryImpl import AwsProcessorFactoryImpl
from nephele.CommandArgumentParser import CommandArgumentParser

from botocore.exceptions import ClientError
from fnmatch import fnmatch
from pprint import pprint
from stdplus import *

# DELETEME: mappedKeys = { 'SecretAccessKey' : 'AWS_SECRET_ACCESS_KEY', 'SessionToken': 'AWS_SECURITY_TOKEN', 'AccessKeyId' : 'AWS_ACCESS_KEY_ID' }

from nephele.SilentException import SilentException
from nephele.SlashException import SlashException

from nephele.AwsAutoScalingGroup import AwsAutoScalingGroup
from nephele.AwsStack import AwsStack
from nephele.AwsRoot import AwsRoot


histfile = os.path.join(os.path.expanduser("~"), ".nephele_hist")

def main():
    try:
        argv = sys.argv

        Config.loadConfig()

        parser = CommandArgumentParser(argv[0])
        parser.add_argument('-p','--profile',dest='profile',default=defaultifyDict(Config.config,'profile','default'),help='select nephele profile')
        parser.add_argument('-m','--mfa',dest='mfa',help='provide mfa code')
        parser.add_argument('-c','--continue',dest='continue',action='store_true',default=False,help='continue after executing `command`')
        parser.add_argument(dest='command',nargs=argparse.REMAINDER)
        args = vars(parser.parse_args(argv[1:]))

        command = args['command']
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except IOError:
            pass
        atexit.register(readline.write_history_file, histfile)
        atexit.register(AwsProcessor.killBackgroundTasks)

        AwsProcessor.processorFactory = AwsProcessorFactoryImpl()

        awsConfigFilename = os.path.expanduser("~/.aws/credentials")
        if not os.path.exists(awsConfigFilename):
            print( "ERROR: aws cli has not been configured." )
            pid = fexecvp(['aws','configure'])
            os.waitpid(pid,0)

        command_prompt = AwsRoot()
        command_prompt.onecmd("profile -v {}".format(args['profile']))
        if None != args['mfa']:
            command_prompt.onecmd("mfa {}".format(args['mfa']))

        cmdloop = True
        if command:
            command_prompt.onecmd(" ".join(command))
            cmdloop = args['continue']
        else:
            command_prompt.onecmd("stacks --summary")

        if cmdloop:
            command_prompt.cmdloop()

    except SystemExit as systemExit:
        print("exiting...")
        pass
    except SilentException as ignore:
        pass

if __name__== "__main__":
    main()

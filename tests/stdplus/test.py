from __future__ import print_function
import sys

from nose.core import run
from nose.core import unittest

from pprint import pprint

from stdplus._readSshConfig import parseSshConfig
from stdplus import *

def test_parseSshConfig():
    result = parseSshConfig("Host 192.168.*\n"
                            + "     # User earlye\n"
                            + "     User ec2-user\n"
                            + "     IdentityFile /Users/earlye/.ssh/aws/keen-test/cassandra.private.pem\n"
                            + "     #ProxyCommand ssh -i /Users/earlye/.ssh/id_rsa.pub -W %h:%p cassandra@bastion.us-west-2.keen-test.aws.keen.io\n"
                            + "     ProxyCommand ssh -q -i /Users/earlye/.ssh/id_rsa.pub -W %h:%p earlye@bastion.us-west-2.keen-test.aws.keen.io\n")
    assert( '192.168.*' in result.hosts )
    assert( 'ProxyCommand' in result.hosts['192.168.*'].settings)
    assert( 1 == len(result.hosts['192.168.*'].settings['ProxyCommand']) )
    assert( result.hosts['192.168.*'].settings['ProxyCommand'][0].value == 'ssh -q -i /Users/earlye/.ssh/id_rsa.pub -W %h:%p earlye@bastion.us-west-2.keen-test.aws.keen.io' )

def test_readSshConfig():
    result = readSshConfig()

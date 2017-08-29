from AwsProcessor import AwsProcessor
from stdplusAwsHelpers.AwsConnectionFactory import AwsConnectionFactory

from pprint import pprint

class AwsInstance(AwsProcessor):
    def __init__(self,instanceId,parent):
        """
        Construct an AwsInstance command processor
        """
        AwsProcessor.__init__(self,parent.raw_prompt + "/instance:" + instanceId,parent)
        self.instanceId = instanceId
        self.do_refresh('')

    def do_refresh(self,args):
        """
        Refresh the view of the instance
        """
        client = AwsConnectionFactory.getEc2Client()
        response = client.describe_instances(InstanceIds=[self.instanceId])
        self.instance = response["Reservations"][0]["Instances"][0]

    def do_pprint(self,args):
        """
        Print the instance model object.
        """
        pprint(self.instance)

    def do_tags(self,args):
        for entry in self.instance['Tags']:
            print("'{}': '{}'".format(entry['Key'],entry['Value']))

    def do_ssh(self,args):
        parser = CommandArgumentParser("ssh")
        parser.add_argument('-a','--interface-number',dest='interface-number',default='0',help='instance id of the instance to ssh to')
        parser.add_argument('-ii','--ignore-host-key',dest='ignore-host-key',default=False,action='store_true',help='Ignore host key')
        parser.add_argument('-i','--identity',dest='identity',default=None,help='Identity file to use')
        parser.add_argument('-ne','--no-echo',dest='no-echo',default=False,action='store_true',help='Do not echo command')
        parser.add_argument('-L',dest='forwarding',nargs='*',help="port forwarding string: {localport}:{host-visible-to-instance}:{remoteport} or {port}")
        parser.add_argument('-R','--replace-key',dest='replaceKey',default=False,action='store_true',help="Replace the host's key. This is useful when AWS recycles an IP address you've seen before.")
        parser.add_argument('-Y','--keyscan',dest='keyscan',default=False,action='store_true',help="Perform a keyscan to avoid having to say 'yes' for a new host. Implies -R.")
        parser.add_argument('-B','--background',dest='background',default=False,action='store_true',help="Run in the background. (e.g., forward an ssh session and then do other stuff in aws-shell).")
        parser.add_argument('-v',dest='verbosity',default=0,action=VAction,nargs='?',help='Verbosity. The more instances, the more verbose');
        parser.add_argument('-m',dest='macro',default=False,action='store_true',help='{command} is a series of macros to execute, not the actual command to run on the host');
        parser.add_argument(dest='id',default=self.instanceId,help='identifier of the instance to ssh to [aws instance-id or ip address]')
        parser.add_argument(dest='command',nargs='*',help="Command to run") 
        args = vars(parser.parse_args(args))
        self.ssh(args)

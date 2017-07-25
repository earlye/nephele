Nephele: a shell for aws.
```````````````````````````

Overview
========

I wasn't happy with the AWS web console, because the UI felt
disjointed and was slow to navigate. So I slapped this together:
a very simple interactive cli shell in python.

I'm actively using it for work, so it supports the things that
I'm doing, rather than being an exhaustive system. I invite
pull requests for missing features, bugfixes, etc.

WARNINGS
========

This tool is incredibly immature. It WILL be changing considerably as
long as I'm using it, because I will be viewing the things it does (or
doesn't do), and the manner in which it does (or doesn't do) them as
impediments to my workflow.

It is not even "alpha" level code yet, so expect things to be broken
or buggy. Also expect syntax to be in a fairly constant state of flux.

Installation
============

.. code-block::

    pip install nephele

Usage
=====

.. code-block:: bash

    $ nephele
    (aws)/: help

Configuration
=============

Nephele reads `~/.nephele.yaml` during startup. Its format looks like this:

.. code-block::

   profile: {profile-name}

   profiles:
     {profile-name}:
       awsProfile: {aws profile name}
       ssh-jump-host: {jump host name or ip}
       ssh-jump-user: {jump host username}
     {profile-name-2}:
       awsProfile: {aws profile name}
       ssh-jump-host: {jump host name or ip}
       ssh-jump-user: {jump host username}

   ssh-macros:
     {macro-name}: {remote command}


SSH support
===========

If you've set up your `~/.nephele.yaml` with a correct
`profiles.{profile}.ssh-bastion` entry, then this is probably the best
part of `nephele`.

nephele can ssh to an instance without you having to figure out its
ip, modify /etc/host, or know anything other than its aws instance id:

.. code:: bash
  (aws)/: ssh {instance-id}
  /usr/bin/ssh {first private ip}
  Last login: {sometime} from {somewhere}
  
         __|  __|_  )
         _|  (     /   Amazon Linux AMI
        ___|\___|___|

  https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/

If you've navigated to an autoscaling group, you don't even need to
know the instance id. You can ssh by the instance's index in the
autoscaling group's list of instances:

.. code-block:: bash

    (aws)/stack:{stack}/stack:{substack}/: asg 0
    loading auto scaling group 0
    loading stack resource arn:{arn}
    AutoScaling Group:{name}
    === Instances ===
     0 Healthy az-2a {instance-id}
     1 Healthy az-2b {instance-id}
     2 Healthy az-2c {instance-id}
    (aws)/stack:{stack}/stack:{substack}/asg:{asg}/: ssh 2
    /usr/bin/ssh {first private ip}
    Last login: {sometime} from {somewhere}
  
         __|  __|_  )
         _|  (     /   Amazon Linux AMI
        ___|\___|___|
  
    https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/

It also supports port forwarding!

.. code-block:: bash

    (aws)/stack:{stack}/stack:{substack}/asg:{asg}/: ssh 2 -L 8888:localhost:8888
    /usr/bin/ssh {first private ip}  
    Last login: {sometime} from {somewhere}

         __|  __|_  )
         _|  (     /   Amazon Linux AMI
        ___|\___|___|

    https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
    $ exit
    (aws)/stack:{stack}/stack:{substack}/asg:{asg}/: ssh 2 -L 8888 # <-- useful shorthand!

So how do you set up your `~/.nephele.yaml` for this? It helps if your
AWS admins have set things up so that using ssh from a command line is
fairly straightforward. If you need a `-J` option to ssh to connect to
a host, specify the jump host user and password using
`profiles.{profile}.ssh-jump-host` and
`profiles.{profile}.ssh-jump-user`, respectively.

Command Reference
=================

We use the excellent argparse module to specify how commands are
used. This reference contains descriptions only; for details on
syntax, use any command's `-h` option.

Globally Available Commands
---------------------------

config
^^^^^^

Deal with configuration. Available subcommands:

* config print - print the current configuration
* config reload - reload the current configuration from disk
* config set - change a setting in the configuration
* config save - save the configuration to disk

mfa
^^^

Enter a 6-digit MFA token. Nephele will execute the
appropriate `aws` command line to authenticate that token.

profile
^^^^^^^

Select nephele profile

quit
^^^^

Exit nephele

ssh
^^^

SSH to an instance. 

Note: This command is extended in more specific contexts, for example
inside Autoscaling Groups.

slash
^^^^^

Navigate back to the root level.

For example, if you are in `(aws)/stack:.../asg:.../`, executing
`slash` will place you in `(aws)/`.

up
^^^

Navigate up by one level.

For example, if you are in `(aws)/stack:.../asg:.../`, executing `up`
will place you in `(aws)/stack:.../`.


New Features
============

_Most Recent Last._

Doesn't include bug fixes, or any features I forgot to list. Maybe
that last bit was obvious :-D

Yes, you could figure this all out by looking at commit logs. Why would
I make you go through that?

* You can now input an MFA token by running `mfa {token}`. It's
  rudimentary support at this point, and likely broken if you've never
  used [aws-mfa](https://github.com/lonelyplanet/aws-mfa) before.

* You can now ssh with shorthanded port forwarding. Basically, if you
  want to forward a port on the remote server via the same local port,
  you no longer have to use the `-L {port}:localhost:{port}`
  syntax. Instead, just say `-L {port}`. You can still use the server
  as a tunnel to yet another server, or choose different local/remote
  port numbers with the old syntax though.

* When launching, nephele automatically runs "stacks" for you.

* --profile (short: -p) selects a specific AWS profile. This is
  helpful when other processes require that your default profile be
  one other than the one you would like nephele to use.

* nephele now knows how to get your aws device info. I also tried to
  make it file-compatible with aws-mfa, so you should in theory not
  need the separate aws-mfa tool any longer - just use nephele to
  manage your .aws/{mfa-related-files}, and you should be good to
  go. Of course, my wife always says she wants to move to Theory,
  because everything works... in Theory.

* --mfa (short: -m) provide your mfa command at launch. If you *know*
  your cached mfa credentials are expired, this saves the step of
  waiting for nephele to get access denied.

* there is now a `profile` command to change profiles after you've
  started nephele.

* `stacks` now adds `-e` and `-i` parameters so you can exclude or
  include new stack states in the filter.

* `~/.nephele.yaml` is the new config file. It has one setting for now,
  `profile`. Example:

.. code-block:: config

    ---
    profile: {aws profile name}

* `ssh` commands now have a `-R`/`--replace-key` option. It is quite
  possible in AWS for IP addresses to get recycled, especially if you
  are creating/tearing-down cloudformation stacks while iterating on
  their templates. When this happens, you don't want to have to go
  hack on `~/.ssh/known_hosts` in order to ssh in to the host. This
  option will run the appropriate command (`ssh-keygen -R {host}`) to
  remove the entry before running ssh.

* auto-scaling groups now support the `terminateInstance` command.

* AwsStack now prints stack events and outputs as if they were normal
  stack resources.

* Added ability to glob when listing stacks. E.g., `stacks *cass*`
  will list all stacks with "cass" as a substring.

* Renamed from aws-shell to nephele (after the mythological cloud
  nymph), and got the tool to be installable via pip.

* You can now run a command across the instances in an auto scaling
  group. Navigate to the group and use the `run` command.

* Cloudwatch logging support has commenced. It's very rudimentary
  so far - you can see log groups inside stacks, select them
  using the `logGroup` command, and see that there are streams present.
  The output is not beautified yet, and you can't actually see
  the content of those streams yet. Soon.

* IAM role support has commenced, too. It's also very rudimentary so
  far. You can see roles inside cloudformation stacks, down to the
  policy document level using the `role`. The output is not beautified yet
  and it's purely read-only. I don't anticipate beautifying it, because
  pprint() is good enough for me, but I certainly welcome patches if
  it matters to you.

* Cloudwatch logging support continues with the addition of the
  `logStream` command, which is available from inside a `logGroup`.
  Right now you can tail the logs, and they aren't beautified.
  As I get more comfortable with the log-scanning API, I plan to add
  some cross-stream log viewing at the `logGroup` level, probably
  in the form of a grep-like capability. No promises, of course,
  just logging where my head's at.

* In an autoscaling group, the `printInstances` command has two new
  options: `-t` to print the list of tags, and `-d` to print all the
  node's details.

* In a stack, the `copy` command now knows how to copy an asg's id
  to the clipboard.

* ASG's now support the `printActivities` and `printActivity` commands
  to assist in debugging changes initiated by autoscaling.

* ASG's now support showing scaling policies via the `printPolicy`
  command.

* ASG `run` command supports `-s` option to skip _n_ hosts

* Stacks now display their parameters. These are escaped and "elipsified"
  in order to fit. Will be adding a command to print a full parameter
  value at some point.

* stdplus.elipsifyMiddle is now a thing.

* ssh commands no longer depend on ~/.ssh/config working, instead
  supporting ~/.nephele.yaml

* ssh now supports the fantastic -J option (you'll need a recent ssh
  client for this to work)

* ssh has a very limited macro capability. Specifically, you can
  do something like this:

.. code-block:: config

    ssh-macros:
      cassandrapid: pgrep -f CassandraDaemon

    (aws)/stack:.../asg:.../: ssh -m 0 cassandrapid
    /usr/bin/ssh 192.168.1.1 -q -J jump-host.us-west-2.generic.domain pgrep -f CassandraDaemon
    3285
    (aws)/stack:.../asg:.../:

  It does not yet have a way to do variable substitution.

* You can now reload your config using the `configReload` command.

* Started adding a command reference to this doc.

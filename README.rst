#####
OpenShift
#####

A openshift cluster manager based on the Python docker API

.. image:: https://travis-ci.org/FNNDSC/openshiftmgr.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/openshiftmgr

PREREQS:

- You will need a running OpenShift cluster with a valid .kube/config for openshiftmgr.py to access
- If you are mounting directories for openshiftmgr to access within OpenShift, you'll need to allow OpenShift to access hostDirs: https://docs.openshift.org/latest/admin_guide/manage_scc.html#use-the-hostpath-volume-plugin


The docker image can be run from a openshift manager to schedule a job:

.. code-block:: bash

  docker run --rm -v /root/.kube/config:/root/.kube/config fnndsc/openshiftmgr openshiftmgr.py -s test -p myproject -i alpine -c "echo test"

This will schedule the ``test`` job that runs command:

.. code-block:: bash

  echo test

using the ``Alpine`` image


The same thing can be accomplished from ``Python`` code:

.. code-block:: python

  client = docker.from_env()
  # 'remove' option automatically remove container when finished
  byte_str = client.containers.run('fnndsc/openshiftmgr',  'openshiftmgr.py -s test -p myproject -i alpine -c "echo test"',
                                   volumes={'/root/.kube/config': {'bind': '/root/.kube/config', 'mode': 'rw'}},
                                   remove=True)


To remove the ``test`` job:

.. code-block:: bash

  docker run --rm -v /root/.kube/config:/root/.kube/config fnndsc/openshiftmgr openshiftmgr.py --remove test -p myproject

or from ``Python``:

.. code-block:: python

  byte_str = client.containers.run('fnndsc/openshiftmgr',  'openshiftmgr.py --remove test -p myproject',
                                   volumes={'/root/.kube/config': {'bind': '/root/.kube/config', 'mode': 'rw'}},
                                   remove=True)


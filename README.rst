#####
OpenShift
#####

A openshift cluster manager based on the Python docker API

.. image:: https://travis-ci.org/FNNDSC/openshift.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/openshift

The docker image can be run from a openshift manager to schedule a service:

.. code-block:: bash

  docker run --rm -v /root/.kube/config:/root/.kube/config fnndsc/openshift pman_openshift.py -s test -p myproject -i alpine -c "echo test"

This will schedule the ``test`` service that runs command:

.. code-block:: bash

  echo test

using the ``Alpine`` image


The same thing can be accomplished from ``Python`` code:

.. code-block:: python

  client = docker.from_env()
  # 'remove' option automatically remove container when finished
  byte_str = client.containers.run('fnndsc/pman-openshift',  'pman_openshift.py -s test -p myproject -i alpine -c "echo test"',
                                   volumes={'/root/.kube/config': {'bind': '/root/.kube/config', 'mode': 'rw'}},
                                   remove=True)


To remove the ``test`` service:

.. code-block:: bash

  docker run --rm -v /root/.kube/config:/root/.kube/config fnndsc/pman-openshift pman_openshift.py --remove test -p myproject

or from ``Python``:

.. code-block:: python

  byte_str = client.containers.run('fnndsc/pman-openshift',  'pman_openshift.py --remove test -p myproject',
                                   volumes={'/root/.kube/config': {'bind': '/root/.kube/config', 'mode': 'rw'}},
                                   remove=True)


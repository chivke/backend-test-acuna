
Welcome to Backend's test documentation!
========================================



Use
====

.. code-block::

  docker-compose -f local.yml build
  docker-compose up


Testing
=======

.. code-block::

  docker-compose -f local.yml run --rm django pytest

.. code-block::

  docker-compose -f local.yml run --rm django coverage run -m pytest
  docker-compose -f local.yml run --rm django coverage report

Tests
=====

Application has automatic tests to ensure everything is working correctly.

To run tests:

.. code-block::

    python -m pytest tests


Logic tests
-----------

Logic of application is completely tested. It uses flexmock for faking logger interface,
which is not subject of these tests.


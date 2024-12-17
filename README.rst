=====================
TestLitePytest
=====================

.. image:: https://img.shields.io/pypi/v/TestLitePytest.svg
    :target: https://pypi.org/project/TestLitePytest
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/TestLitePytest.svg
    :target: https://pypi.org/project/TestLitePytest
    :alt: Python versions


Pytest adaptor for TestLite TMS system

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.



Installation
------------

You can install "pytest-TestLitePytest" via `pip`_ from `PyPI`_::

    $ pip install TestLitePytest


Initial setup
-------------

To use, create a config file: “TestLiteConfig.ini” (be sure to use this
name, otherwise you will not find the configuration file)

::

   [TestLiteConfig]
   TESTLITEURL=http://TestLite.test (The address where your TestLite is located)
   DELETEREPORTSDIR=True/False (Save folder with reports) (Default: True)
   REPORTSDIRNAME=TestLiteReports (Тame of the folder with reports)
   REPORTSSAVETYPE=BINARY/TXT (In what format to save reports) (Default: BINARY) (TXT doesn't work))

Use in your tests
-----------------

::

    import  testlite

    class  TestWithTestLite:

        @testlite.test_key('PROJECT-TC-1')
        def  test_1(self):
            pass
               
        @testlite.test_key('PROJECT-TC-2')
        def  test_2(self):
        pass

Where “PROJECT-TC-1” its test case key in TestLite

::

        @testlite.test_key('PROJECT-TC-1')
            #TestLiteStep
            ..step1
            #TestLiteStep
            ..step2
               

#TestLiteStep - This is a pointer to the start of the step. The next #TestLiteStep indicates that the step has ended and a new one has begun. If an error is caused between these comments, the report will show that the step was broken

::

    get_parameters_from_TestLite('PROJECT-TC-1')
  
Returns parameters that are specified in test cases in TestLite

What it should look like
------------------------
::

        import testlite
        import pytest

        params = get_parameters_from_TestLite('PROJECT-TC-1')

        class Test:

            @pytest.fixture
            def fixture(self):
                return 'fixture value'

            @testlite.test_key('PROJECT-TC-1')
            @pytest.mark.parametrize('data', params)
            def test_1(self, fixture, data):
                #TestLiteStep
                ..step1
                #TestLiteStep
                ..step2


Command Line Arguments
----------------------

1. --testsuite=PROJECT-TS-1 (TestSuite key in TestLite)
2. --savejson=json_report.json (If so, save the file with the report.)
3. --collectfromtestlite (If specified, it will try to collect test cases using the keys specified in the test functions that correspond to the test suite in TestLite)

If you specify testsuite then TestLitePytest will try to send a report
to your TestLite that you specified

License
-------

Distributed under the terms of the `MIT`_ license, "TestLitePytest" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: https://opensource.org/licenses/MIT
.. _`BSD-3`: https://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: https://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: https://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/DmitrySkryabin/pytest-TestLitePytest/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project

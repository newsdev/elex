************
Installation
************

Quick install
#############

Install the Python library:

.. code:: bash

    pip install elex

Set your AP API key:

.. code:: bash

    export AP_API_KEY=<MY_AP_API_KEY>

Optional requirements
=====================

-  MongoDB (for recording raw results during tests and elections)

Install walkthrough with virtualenv
###################################

If you've set up and run Python projects before, you may have your own process, and the `Quick Install`_ instructions can get you going. But if you're fairly new to Python development, or if you're not familiar with the benefits of using a virtual environment, these tips are for you.

Set up some base tools
======================

The NPR Visuals Team's `guide to setting up a development environment <http://blog.apps.npr.org/2013/06/06/how-to-setup-a-developers-environment.html>`_ is wonderful. Walking through the entire guide is highly recommended; your machine will be much happier for it, and you'll feel prepared for a lot of things beyond just Elex.

For now, though, the most important piece is "Chapter 2: Install Virtualenv." At the very least, step through that section and install ``virtualenv`` and ``virtualenvwrapper``, two tools that help you use virtual environments for your Python projects.

.. note:: Virtual environments let you compartmentalize projects and the Python tools you install to work on them. You can create as many virtual environments as you like. When you "activate" one of them, you can feel comfortable installing new libraries, because if things break, no problem. Delete that environment and start again; your global settings haven't been touched. When you have things working just right, you can "freeze" the environment to create a list of installed packages so someone else can replicate it. Learning to love virtual environments makes you more efficient _and_ less stressed.

Once you've installed ``virtualenv`` and ``virtualenvwrapper``, then added the appropriate trigger to your ``.bash_profile`` as described in the NPR Visuals guide, you're ready to set up a pristine Elex environment.

Install Elex
============

The ``virtualenvwrapper`` tool gives you access to several commands for creating and managing virtual environments. To create a fresh environment for Elex, run this from your command line:

.. code:: bash

    mkvirtualenv elex

Your new environment won't know about or have access to any Python tools you've installed elsewhere, which is exactly what you want. The ``mkvirtualenv`` command will automatically activate your new environment for you, and your command prompt should reflect it. You should see something like:

.. code:: bash

    (elex) username@host: ~/your/path $

For reference, to turn off an active environment, run the ``deactivate`` command:

.. code:: bash

    deactivate

And to enable an environment, run ``workon`` followed by the environment's name:

.. code:: bash

    workon elex

With your new "elex" environment activated, installing the Elex library itself is easy:

.. code:: bash

    pip install elex

That will download Elex and add it to your virtual environment, along with all the libraries it depends on. Just for fun, you can print to screen everything that was installed:

.. code:: bash

    pip freeze

Now the Elex code will be available to you any time you activate your "elex" environment. You'll still need a project API key to actually run commands, so with "elex" active, add the key you should have received from AP:

.. code:: bash

    export AP_API_KEY=your_api_key_string

And with that in place, Elex should work as expected. You can test with any of the `tutorial commands <http://elex.readthedocs.org/en/1.0.0/tutorial.html>`_, like:

.. code:: bash

    elex races 11-03-2015 -o json

Some extra tricks
=================

Automatically set your API key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you've followed the instructions above, you should already have your ``AP_API_KEY`` set. When you ``export`` a variable, however, it's only available until your session ends. It's tedious to set something like that manually every time you start a new project session, though. Thankfully ``virtualenvwrapper`` provides an easy way to automatically load variables each time you activate an environment.

Open a new tab in your terminal, and:

.. code:: bash

    workon elex
    cdvirtualenv
    open bin/postactivate

This will activate your "elex" environment, navigate to its internal directory on your machine, then use your text editor to open a file called ``postactivate``. Any code you put in this file will be run immediately after you activate that environment. So just add:

.. code:: bash

    export AP_API_KEY=your_api_key_string
    echo "AP_API_KEY set"

Then save and close. From now on, every time you activate a new session of your "elex" environment, your API key will automatically be available (and you'll get a little "AP_API_KEY set" reminder printed to screen).

Make human-readable JSON
^^^^^^^^^^^^^^^^^^^^^^^^

You might notice that generating JSON with an Elex command like ``elex races 11-03-2015 -o json`` will put all the results on one line. This is great for keeping file sizes smaller, and it's perfectly readable by other machines. But if you're trying to see what properties are available in the JSON generated by different Elex commands, it's not particularly human-friendly. Fortunately, Elex provides a shortcut to display human-formatted json, the ``--format-json`` flag.

.. code:: bash

    elex races 11-03-2015 -o json --format-json

Or to save to a flat file you can inspect later:

.. code:: bash

    elex races 11-03-2015 -o json --format-json > races.json

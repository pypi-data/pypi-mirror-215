Python BatchMailchimp
=====================

.. image:: https://img.shields.io/pypi/v/batch-mailchimp.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/batch-mailchimp/

.. image:: https://img.shields.io/pypi/l/batch-mailchimp.svg
    :alt: License
    :target: https://pypi.org/project/batch-mailchimp/

A light wrapper around `mailchimp-marketing <https://pypi.org/project/mailchimp-marketing/>`__ that makes it easier to use batch operations.

Getting Started
---------------

Installation
~~~~~~~~~~~~

::

   pip install batch-mailchimp

Usage
~~~~~

This can be used as a drop-in replacement for mailchimp-marketing –
just change the import at the top, and everything should work the same:

.. code:: python

   import batch_mailchimp as MailchimpMarketing

   client = MailchimpMarketing.Client({
       "api_key": "YOUR_API_KEY",
   })

The additional functionality comes when we initialise the client with ``batch=True``:

.. code:: python

   import batch_mailchimp as MailchimpMarketing

   client = MailchimpMarketing.Client({
       "api_key": "YOUR_API_KEY",
       "batch": True,
   })

If we do this, operations are stored up in the client, to be run later. For example:

.. code:: python

   # add John Doe with email john.doe@example.com to list matching id '123456'
   client.lists.members.create(
       '123456', {
           'email_address': 'john.doe@example.com',
           'status': 'subscribed',
           'merge_fields': {
               'FNAME': 'John',
               'LNAME': 'Doe',
           },
       },
   )

All new operations will be added to the batch. When we’re ready, we can run all the operations in the batch:

.. code:: python

   batch = batch_client.batches.run()

We can check the batch’s status using:

.. code:: python

   batch.status()

API Structure and Endpoints
---------------------------

The API structure and endpoints match that of `mailchimp3 <https://pypi.org/project/mailchimp3/>`__. You should refer to their documentation for usage.

Support
-------

If you are having issues, please `create an issue <https://github.com/FullFact/python-batchmailchimp/issues>`__.

License
-------

The project is licensed under the MIT License.

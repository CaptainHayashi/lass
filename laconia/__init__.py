"""
======================================================
`laconia` - Lightweight external exposure of LASS data
======================================================

The `laconia` module holds machine-readable views of information in
LASS models.  It's like an ad-hoc API.

Its name comes from the area from which the Spartans originated; it
often returns information in short, terse bursts in the Spartan
tradition.

Things that belong in `laconia`:

1) Application-specific formatted views of data
2) Temporary glue logic that will eventually be replaced with APIs
3) Anything that is intended to be embedded in a script but does not
   require a heavyweight retrieval mechanism

Much of `laconia` is temporary and anticipates the creation of proper
structured API exposure of data.  As such, only depend on `laconia`
runoffs if you're reasonably confident that they are either permanent
or will be easily replacable in your code in the future.

tests
-----

.. automodule:: laconia.tests
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

views
-----

.. automodule:: laconia.views
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

"""

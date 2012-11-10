"""
=====================================================
`grid` - basic framework for dynamic grids of widgets
=====================================================

The `grid` app contains plumbing for a very basic dynamic widget grid
system.

`grid` was originally designed for the URY front page, which is
composed of various rectangular sections that each display a separate
view.  It was intended to separate mechanism from policy by allowing
the website templates to contain no information about the specific
make-up of the front site grid and the exact positions of parts of
it.

At time of writing, `grid` is very feature-poor and inflexible, having
effectively been created as a quick method of making the
aforementioned home page dynamic.  However, it is hoped that it can be
generalised in the future to other types of widget grid.

Models
======

.. automodule:: grid.models
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

Template tags
=============

The implementation-level side of the `grid` framework is contained in a
template tag library, `grid_tags`.

.. automodule:: grid.templatetags.grid_tags
    :deprecated:
    :members:
    :undoc-members:
    :show-inheritance:

"""

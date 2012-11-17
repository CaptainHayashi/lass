"""
Views for the dynamic grid system.

"""

from grid.models import GridBlock


def block_raw(request, block_id):
    """
    Renders the view associated with the block with the given ID.

    The view will be rendered verbatim, and thus will *not*
    constitute well-formed HTML.  Use this to include the block in
    existing pages not able to embed the view itself, for example
    using AJAX.

    :param request: the HTTP request that retrieved this view
    :param block_id: the identifier of the block (usually its name)
    :type block_id: string, integer or `GridBlock`
    :rtype: the result of calling the block's view with this request
    """

    block = GridBlock.get_or_404(block_id)

    # Ugly code to load the required module and view dynamically.
    ascii_view_name = block.view_name.encode('ascii', 'ignore')
    module_name, view_name = ascii_view_name.rsplit('.', 1)
    module = __import__(module_name, fromlist=[view_name])
    view = getattr(module, view_name)

    return view(request, block_id=block_id)

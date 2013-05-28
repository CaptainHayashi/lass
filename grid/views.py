"""
Views for the dynamic grid system.

"""

from django.shortcuts import render

from grid.models import GridBlock


def template_of(block):
    """Returns the path to the template for the given block.

    Args:
        block: the block whose template should be found

    Returns:
        the template path (for example, 'grid/example.html').
    """
    return 'grid/{}.html'.format(block.name)


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

    return render(
        request,
        'grid/block_indirect.html',
        {
            'box': block,
            'template': template_of(block),
        }
    )

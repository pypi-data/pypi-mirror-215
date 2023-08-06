from halerium_utilities.file.io import read_board, write_board, get_board_notebook_and_text_filenames_in_tree

from copy import deepcopy


COLOR_MAP = {
    "#125059": "note-color-2",  # green
    "#51455b": "note-color-8",  # yellow
    "#513063": "note-color-6",  # red
    "#28337e": "note-color-4"  # blue
}


def update_card_colors_in_board(board, inplace=False):
    """Update the colors of nodes in a board.

    Parameters
    ----------
    board :
        The board for which to update the colors of the nodes.
    inplace :
        Whether to update the colors in place.

    Returns
    -------
    board :
        The board with the color of every node updated.

    """
    if not inplace:
        board = deepcopy(board)

    if 'nodes' not in board:
        raise Exception("Board does not contain key 'nodes'")

    try:
        for node in board['nodes']:
            if node['type'] == 'note':
                if node['color'] in COLOR_MAP:
                    node['color'] = COLOR_MAP[node['color']]
    except TypeError:
        raise Exception("Node in board['nodes'] is not iterable")
    except KeyError as e:
        print(e)
        raise Exception(
            "Node does not contain either 'type' or 'color' as its key")

    return board


def update_card_colors_in_board_file(board_file_name, new_board_file_name):
    """Update the colors of nodes in board file.

    Parameters
    ----------
    board_file_name :
        The file to read the board from.
    new_board_file_name :
        The file to write the board with updated nodes to.

    Returns
    -------

    """
    board = read_board(board_file_name)

    board = update_card_colors_in_board(board, inplace=True)

    write_board(board, new_board_file_name)


def update_card_colors_in_board_file_tree(path):
    """Update the colors of nodes in drectory tree.

    Update the colors of all cards in all board files in a directory tree.
    The nodes are updated in-place.

    Parameters
    ----------
    path :
        The root of the directory tree.

    Returns
    -------

    """
    try:
        board_paths = get_board_notebook_and_text_filenames_in_tree(path)[0]
    except Exception as e:
        print('Error retrieving board file names in path: {}\nError Message: {}'.format(
            path, e))
        return

    for board_path in board_paths:
        try:
            update_card_colors_in_board_file(board_path, board_path)
        except Exception as e:
            print('Error capitalizing card titles in board {}.\n'.format(board_path) +
                  'Error message: {}'.format(e))

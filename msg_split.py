from bs4 import BeautifulSoup
from typing import Iterable, Tuple, Generator

BLOCK_TAGS = ['p', 'b', 'strong', 'i', 'ul', 'ol', 'div', 'span']


def get_next_fragment(children: Iterable, current_fragment: str, max_len: int, additional_length: int = 0,
                      left_side: str = '', right_side: str = '') -> Tuple[str, str]:
    """Recursively collecting all elements of current and forming next fragment.

    :param children: Children of current element (tag).
    :param current_fragment: Curreent fragment, which we are forming right now.
    :param max_len: Maximum length of current fragment.
    :param additional_length: Additional length, we need it because on splitting of block tags we don't add
    closing tags to our current_fragment until we get our limit length.
    :param left_side: Left side (opening block tags), we need them for forming next fragment.
    :param right_side: Right side (closed block tags), we need them for forming next fragment.
    """
    is_next = False
    next_fragment = None

    for child in children:
        if is_next:
            next_fragment += str(child)
            continue
        full_length = len(current_fragment) + len(right_side) + additional_length
        if isinstance(child, str):
            if full_length + len(child) <= max_len:
                current_fragment += child
            else:
                next_fragment = f'{left_side}{child}'
                is_next = True
        elif child.name:
            child_string = str(child)
            if full_length + len(child_string) <= max_len:
                current_fragment += child_string
            elif child.name in BLOCK_TAGS:
                open_tag = f'<{child.name}>'
                close_tag = f'</{child.name}>'
                current_fragment, next_fragment = get_next_fragment(
                    children=child.children, current_fragment=f'{current_fragment}{open_tag}', max_len=max_len,
                    additional_length=additional_length + len(right_side), left_side=f'{left_side}{open_tag}',
                    right_side=close_tag
                )
                is_next = True
            else:
                next_fragment = f'{left_side}{child_string}'
                is_next = True

    return f'{current_fragment}{right_side}', f'{next_fragment}{right_side}'


def split_message(source: str, max_len: int) -> Generator:
    """Splits the original message (`source`) into fragments of the specified length (`max_len`)."""
    current_fragment = ""
    last_next_fragment = None
    children = BeautifulSoup(source, 'html.parser').children

    while True:
        current_fragment, next_fragment = get_next_fragment(children, current_fragment, max_len)
        if next_fragment == last_next_fragment:
            raise ValueError(f"Не могу разделить на данный фрагмент: {next_fragment}")
        last_next_fragment = next_fragment
        yield current_fragment
        current_fragment = next_fragment

        if len(current_fragment) <= max_len:
            if len(current_fragment) > 0:
                yield current_fragment
            break
        else:
            children = BeautifulSoup(current_fragment, 'html.parser').children
            current_fragment = ''

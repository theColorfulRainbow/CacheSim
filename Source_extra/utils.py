import logging as log

'''
File with useful functions to be used in project
'''

MESI = False                # MESI Protocol
FLOPS = False               # hops can go both directions

def get_bit_length(_int):
    """returns bith length of the integer bit representation

    Args:
        _int (int): integer who's bit length is needed

    Raises:
        ValueError: if integer is no a power of 2

    Returns:
        int: lenght of the bit representation of the integer 
    """
    if not is_valid_int(_int):
        raise ValueError("Argument is not a power of 2!")
    return _int.bit_length() - 1


def is_valid_int(_int):
    """Checks if the integer is a power of 2

    Args:
        _int (int): integer under question

    Returns:
        boolean: true if is power of 2; false otherwise
    """
    return (_int & (_int-1) == 0) and _int != 0


def extraxct_from_address(address,cache_lines,cache_line_size):
    """Extract tag, line_id and offset address

    Args:
        address (int): address given to cache
        cache_lines (int): bit representing nr. of cache lines
        cache_line_size (int): bit representing nr. words in a cache line

    Raises:
        ValueError: if address is <= 0

    Returns:
        [int,int,int]: tag, index, offset
    """
    mask_tag = cache_lines + cache_line_size                        # 11
    mask_idx = cache_line_size                                      # 2
    # Shift off the lowest 1 bits, and mask off the higher ones
    tag = (address >> 11) & 0x1FFFFF                                # mask_tag
    # Shift off the lowest 2 bits, and mask off the higher ones
    index = (address >> 2) & 0x1FF                                  # mask_idx
    # Shift off the lowest 0 bits, and mask off the higher ones
    offset = (address >> 0) & 0x3
    return tag, index, offset             
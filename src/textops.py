
LEFT=0
RIGHT=1
CENTER=2
LEFTRIGHT=3

#
# Add spaces on left side (for RIGHT justify)
#
def __padleft(words, width):
    s = ' '.join(words)
    n = len(s)
    need = width - n
    if need <= 0:
        return s
    return (' ' * need) + s

#
# Add spaces on right side (for LEFT justify)
#
def __padright(words, width):
    s = ' '.join(words)
    n = len(s)
    need = width - n
    if need <= 0:
        return s
    return s + (' ' * need)

#
# Add spaces on both sides (for CENTER justify)
#
def __padboth(words, width):
    s = ' '.join(words)
    n = len(s)
    need = width - n
    if need <= 0:
        return s
    lhs = need // 2
    rhs = need - lhs
    return (' ' * lhs) + s + (' ' * rhs)

#
# Add spaces internally (for LEFTRIGHT justify)
#
# Determine the fractional number of spaces that are needed
# and use that to determine when an extra space is needed beyond
# the integer number of spaces.
#
def __padinternal(words, width):
    s = ' '.join(words)
    n = len(s)
    need = width - n
    ngaps = len(words)-1
    if ngaps == 0:
        return ' '.join(words)
    add = need / ngaps
    s = ''
    x = int(add)
    swidth=x + 1
    add -= x
    extra = 0
    for ndx in range(len(words)):
        w = words[ndx]
        if ndx != len(words)-1:
            extra += add
            s += w + (' ' * swidth)
            if extra >= 0.5:
                #print(f"{swidth:1d},{x:.02f},{add:.02f}")
                s += ' '
                extra -= 1.0
        else:
            s += w
    return s

def justify(text, width=72, indent=0, how=LEFT):
    """
    Justify text into multiple lines such that lines are
    no longer than 'width' characters (except if a single
    word is longer than 'width').

    
    Parameters:

    text: Text string to justify.
    width: How wide each line of text should be. Default is 72.
    indent: How much to indent the first line, defaults to zero.
    how: How to justify.  Valid values are:
         LEFT:  Left justify the text with a ragged right side
         RIGHT: Right justify the text with a ragged left side
         CENTER: Center the text on each line, ragged on each side
         LEFTRIGHT: Insert spacing so neither left or right is ragged.

         Default is LEFT
    """

    if how not in [LEFT,RIGHT,CENTER,LEFTRIGHT]:
        raise ValueError("Expected either LEFT, RIGHT, CENTER, LEFTRIGHT for justify type")
    
    result = []
    curlength = indent
    curwords = []

    for word in text.split():
        wlen = len(word)
        if wlen + curlength > width:
            if how == RIGHT:
                s = __padleft(curwords, width)
            elif how == LEFT:
                s = __padright(curwords, width)
            elif how == CENTER:
                s = __padboth(curwords, width)
            elif how == LEFTRIGHT:
                s = __padinternal(curwords, width)

            result.append(s)
            curwords = []
            curlength = 0
        curlength += wlen + 1
        curwords.append(word)

    if len(curwords) != 0:
        if how == RIGHT:
            s = __padleft(curwords, width)
        elif how == LEFT:
            s = __padright(curwords, width)
        elif how == CENTER:
            s = __padboth(curwords, width)
        elif how == LEFTRIGHT:
            s = __padinternal(curwords, width)
        result.append(s)

    result[0] = (' ' * indent) + result[0]
    return "\n".join(result)

def center(text, width):
    """
    Convenience method to call justify() with how=CENTER
    """
    return justify(text, width, how=CENTER)

def justify_paragraphs(text, width=72, indent=0, how=LEFT):
    """
    Justify each newline separated text as a separate paragraph.

    Paramters are the same as for justify()
    """
    result = []
    for p in text.split('\n'):
        result.append(justify(p, width=width, indent=indent, how=how))
    return "\n".join(result)

if __name__ == '__main__':
    import sys
    
    text="This is to test whether this formatting code works properly by left justifying the text on multiple lines with white space at the end of each line to fill out the line.\nHopefully it works. We want some really long words in here just in case so lets make a suuuuuuupppppppppperrrrr long word."

    hownames=["LEFT", "RIGHT", "CENTER", "LEFTRIGHT"]

    s = justify_paragraphs(text, width=40, indent=5)
    print(s)

    for how in [LEFT, RIGHT, CENTER, LEFTRIGHT]:
        failcount = 0
        fails=[]
        for w in range(20,132):
            s = justify(text, w, how=how)
            for l in s.split('\n'):
                if len(l) != w:
                    nw = len(l.split())
                    #
                    # It isn't a failure if it is a single word to big
                    # to fit on a line.
                    #
                    if nw != 1:
                        failedcount += 1
                        fails.append(w)
        h = hownames[how]
        if failcount == 0:
            sys.stderr.write(f"All tests for {h} justify method passed.\n")
        else:
            ws = ", ".join(fails)
            sys.stderr.write(f"{h} justify  method failed {failcount} tests at widths:\n{ws}\n")

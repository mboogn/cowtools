#!/usr/local/bin/python
# coding: utf-8 -*-
from typing import Callable, Any
from itertools import cycle


__name__ = "StringStuff"


class OutputSummoner(Exception):
        """ Dummy Exception for summoning output window.  Specifically meant for use with the PyDroid3 android app."""
        def rais(self, header='\n\n', msg=None, traceback=None, cause=None, **printkwg):
            slf = self
            if msg is not None:
                slf = type(self)(msg)
            if traceback is not None:
                slf = slf.with_traceback(traceback)
            print(header, **printkwg)
            raise slf from cause


EndExc = OutputSummoner("    ...    End")

def endexc(exc=EndExc):
    """Raises an instance of OutputSummoner so that the graphical output is brought into the foreground.  Specifically meant for use with the PyDroid3 android app.."""
    exc.rais()


"printfuncs (0)"

nL = "\n"
nT = "\t"
nT2 = nT*2
nL2 = nL*2
#nT3
nLT = nL+nT
nL2T = nL2+nT
nLT2 = nL+nT2
_jo = ''.join
_jo_ = ' '.join
_jc_ = ', '.join
_jnT = nT.join
_jnL = nL.join
_jnLT = nLT.join
_jnL2 = nL2.join
_jnLT2 = nLT2.join

_jB = b"".join
_jB_ = b" ".join
_jBn = b"\\".join
_jBnx = b"\x00".join
_jBnL = b"\n".join


def join(st_: [str, bytes]):
    "Returns the bound join method of ‘st_’.  Exists mostly for the sake of symmetry with jo, jo_, jnL, etc."
    return st_.join

def joinst(jst_: [str, bytes, type(_jo), type(_jB)], strfunc=str):
    "Accepts an instance of--or the bound .join method of--an instance of str or bytes, "\
    "and returns a callable which accepts any iterable, converts its contents to str or repr form, "\
    "if ‘reprs’ == False or True, respectively, and applies said join method to the sequence."
    
    jst_ = getattr(jst_, 'join', jst_)
    try:
        jstr = jst_(['', ''])
    except TypeError:
        jstr = jst_([b'', b''])
        jst_ = jstr.join
        jstr = repr(jstr)
        
        rebt = lambda x: rpt(bytes(map(ord, repr(x))))
        def stbt(x):
            try: return bytes((x,))
            except TypeError: return bytes(map(ord, str(x)))
        
        def __j(seq, strf=strfunc):
            rbt = stbt if strfunc!=repr else rebt
            return jst_(map(rbt, seq))
    else:
        jst_ = jstr.join
        def __j(seq, strf=strfunc):
            return jst_(map(strf, seq))
    
    js = jstr if jstr.isidentifier() else "ξspecialζς"
    
    __j.__name__ = 'jst_' + js
    assert jst_.__name__ == 'join'
    return __j
    
jo, jo_, jc_ = joinst(_jo), joinst(_jo_), joinst(_jc_)
jnL, jnT, jnLT, jnL2, jnLT2  = joinst(_jnL), joinst(_jnT), joinst(_jnLT), joinst(_jnL2), joinst(nLT2)
jB, jB_, jBn, jBnx, jBnL = joinst(_jB), joinst(_jB_), joinst(_jBn), joinst(_jBnx), joinst(_jBnL)


strEscapeSeprs = [nL, nT, nL2, nT2, nLT, nL2T, nLT2]
strJoiners = [_jo_, _jc_, _jnL, _jnT, _jnLT, _jnL2, _jnLT2]
strJoinsters = [jo, jo_, jc_, jnL, jnT, jnLT, jnL2, jnLT2]
byteJoiners = [_jB, _jB_, _jBn, _jBnx]
byteJoinsters = [jB, jB_, jBn, jBnx]


def prinL2(*value, sep=' ', end='', **kwg):    print(nL, *value, nL, sep=sep, end=end, **kwg)
prinL2.__doc__ = "Same as print, but pads output with newline characters."


def pri_(*value, sep=' ', end='', **kwg):    print(*value, sep=sep, end="", **kwg)
pri_.__doc__ = "Same as print, except the default for ‘end’ is an empty string."


def printrows(*value, sep=', ', linestart='    ', newline=nL, end='\n', **kwg):
    "printrows('sep = ', ' (‘sep’ ', f' + ‘newline’ (={repr(nL)}) ', ' + ‘linestart’)', sep='\\\\', linestart='  . . . ') "\
    "\n    → \n"\
    ". . . sep = \\\n"". . .  (‘sep’ \\\n"". . .  + ‘newline’ ("+f"={repr(nL)}) "+"\\\n"". . .  + ‘linestart’)"
    print(*value, sep=f'{sep}{newline}{linestart}', end=end, **kwg)

def rpt(descr, *value, sep=' ', end='\n', **kwg):
    "print(descr, *value, sep=sep, end=end, **kwg) \n"\
    "If len(value) == 0: \n    return descr \nIf len(value) == 1: \n    return value[0] \n"\
    "    Otherwise return value as a tuple. \n"\
    "Real convenient for when you want to catch the value of something passed from here-to-there "\
    "without having to dismantle anything."
    print(descr, *value, sep=sep, end=end, **kwg)
    if not value: return descr
    if not value[1:]: return value[0]
    return value
def derpt(descr, *value, sep=' ', end='\n', **kwg):
    "Does 𝑵𝑶𝑻 print(descr, *value, sep=sep, end=end, **kwg) \n"\
    "If len(value) == 0: \n    return descr \nIf len(value) == 1: \n    return value[0] \n"\
    "    Otherwise return value as a tuple. \n"\
    "Use as temporary off-switch for .rpt when debugging different parts of a program or whathaveyou."
    (lambda *a, **k: None)(descr, *value, sep=sep, end=end, **kwg)
    if not value: return descr
    if not value[1:]: return value[0]
    return value
    

def _formst_kyvl(items: type({}.items()), joint=', '.join, constru_form=False):
    joint = getattr(joint, 'join', joint)
    if joint is not None: return joint(_formst_kyvl(items, joint=None, constru_form=constru_form))
    if constru_form: return ("{0}={1}".format(*it) for it in items)
    return ("{repr(ky)}={vl}" for ky,vl in items)

Formstrs__ = [_formst_kyvl]


_subtransltabl = {49: 8321, 50: 8322, 51: 8323, 52: 8324, 53: 8325, 54: 8326, 55: 8327, 56: 8328, 57: 8329, 48: 8320, 46: 46, 61: 8332, 43: 8330, 45: 8331, 60: 753, 62: 754, 40: 8333, 41: 8334, 104: 8341, 105: 7522, 106: 11388, 107: 8342, 108: 8343, 97: 8336, 946: 7526, 947: 7527, 961: 7528, 966: 7529, 967: 7530, 120: 8339, 117: 7524, 118: 7525, 101: 8337, 109: 8344, 110: 8345, 111: 8338, 112: 8346, 114: 7523, 115: 8347, 116: 8348, 601: 8340}

_de_subtransltabl = {8321: 49, 8322: 50, 8323: 51, 8324: 52, 8325: 53, 8326: 54, 8327: 55, 8328: 56, 8329: 57, 8320: 48, 46: 46, 8332: 61, 8330: 43, 8331: 45, 753: 60, 754: 62, 8333: 40, 8334: 41, 8341: 104, 7522: 105, 11388: 106, 8342: 107, 8343: 108, 8336: 97, 7526: 946, 7527: 947, 7528: 961, 7529: 966, 7530: 967, 8339: 120, 7524: 117, 7525: 118, 8337: 101, 8344: 109, 8345: 110, 8338: 111, 8346: 112, 7523: 114, 8347: 115, 8348: 116, 8340: 601}

_supertransltabl = {40: 8317, 41: 8318, 43: 8314, 45: 8315, 46: 5159, 48: 8304, 49: 185, 50: 178, 51: 179, 52: 8308, 53: 8309, 54: 8310, 55: 8311, 56: 8312, 57: 8313, 61: 8316, 65: 7468, 66: 7470, 67: 7580, 68: 7472, 69: 7473, 70: 7584, 71: 7475, 72: 7476, 73: 7477, 74: 7478, 75: 7479, 76: 7480, 77: 7481, 78: 7482, 79: 7484, 80: 7486, 81: 5456, 82: 7487, 83: 738, 84: 7488, 85: 7489, 86: 11389, 87: 7490, 88: 739, 89: 89, 90: 7611, 97: 7491, 98: 7495, 99: 7580, 100: 7496, 101: 7497, 102: 7584, 103: 7501, 104: 688, 105: 8305, 106: 690, 107: 7503, 108: 737, 109: 7504, 110: 8319, 111: 7506, 112: 7510, 113: 5456, 114: 691, 115: 738, 116: 7511, 117: 7512, 118: 7515, 119: 695, 120: 739, 121: 696, 122: 7611, 198: 7469, 199: 7580, 216: 7601, 231: 7580, 240: 7582, 248: 7601, 294: 43000, 295: 43000, 322: 43870, 330: 7505, 331: 7505, 338: 43001, 339: 43001, 354: 7605, 355: 7605, 385: 7470, 390: 7507, 391: 7580, 392: 7580, 393: 7582, 394: 7472, 398: 7474, 399: 7498, 400: 7499, 403: 7475, 404: 736, 406: 7590, 407: 7588, 408: 7479, 409: 7503, 411: 7511, 412: 7514, 413: 7598, 414: 7505, 415: 7601, 420: 7486, 421: 7510, 422: 7487, 425: 7604, 426: 7604, 428: 7488, 429: 7511, 430: 7605, 433: 7607, 434: 11389, 439: 7614, 442: 7614, 544: 7505, 545: 7496, 546: 7485, 547: 7485, 564: 7496, 565: 7599, 566: 7605, 568: 7495, 569: 7510, 578: 740, 580: 7606, 581: 7610, 586: 5456, 587: 5456, 592: 7492, 593: 7493, 594: 7579, 595: 7495, 596: 7507, 597: 7581, 598: 7496, 599: 7496, 600: 7498, 601: 7498, 602: 7498, 603: 7499, 604: 7500, 605: 693, 606: 7499, 607: 7585, 608: 7586, 609: 7586, 610: 7475, 611: 736, 612: 7609, 613: 7587, 614: 689, 615: 43868, 616: 7588, 618: 7590, 619: 43870, 620: 43870, 621: 7593, 622: 7614, 623: 7514, 624: 7597, 625: 7596, 626: 7598, 627: 7599, 628: 7600, 629: 7601, 630: 43001, 631: 7607, 632: 7602, 633: 692, 634: 692, 635: 693, 636: 691, 637: 691, 638: 691, 640: 7487, 641: 694, 642: 7603, 643: 7604, 644: 7585, 646: 7604, 647: 7511, 648: 7605, 649: 7606, 650: 7607, 651: 7515, 652: 7610, 653: 7610, 654: 43870, 655: 696, 656: 7612, 657: 7613, 658: 7614, 659: 7614, 660: 704, 661: 705, 662: 704, 663: 7580, 665: 7470, 667: 7475, 668: 7544, 669: 7592, 670: 7503, 671: 7595, 672: 5456, 673: 704, 674: 705, 675: 7611, 676: 7614, 677: 7613, 678: 738, 679: 7604, 680: 7581, 682: 7594, 683: 7611, 686: 7587, 687: 7587, 913: 7493, 914: 7470, 915: 7518, 916: 7472, 917: 7499, 918: 7613, 919: 43868, 920: 7615, 921: 7589, 922: 7479, 923: 7595, 924: 7481, 925: 7482, 926: 739, 927: 7484, 928: 7486, 929: 7487, 931: 738, 932: 7488, 933: 7609, 934: 7520, 935: 7521, 937: 7490, 945: 7493, 946: 7517, 947: 7518, 948: 7519, 949: 7499, 950: 7613, 951: 43868, 952: 7615, 953: 7589, 954: 7503, 955: 737, 956: 7504, 957: 8319, 958: 739, 959: 7506, 960: 7510, 961: 691, 962: 738, 963: 738, 964: 7511, 965: 7607, 966: 7602, 967: 7521, 969: 695, 984: 5456, 985: 5456, 7424: 7424, 7425: 7469, 7426: 7494, 7427: 7471, 7428: 7580, 7429: 7472, 7430: 7582, 7431: 7473, 7432: 7583, 7433: 7502, 7434: 7478, 7435: 7479, 7436: 43870, 7437: 7481, 7438: 7483, 7439: 7484, 7440: 7507, 7441: 7484, 7442: 7506, 7443: 7601, 7444: 43001, 7445: 7485, 7446: 7508, 7447: 7509, 7448: 7486, 7449: 694, 7450: 694, 7451: 7604, 7452: 7489, 7453: 7513, 7454: 7513, 7456: 7515, 7457: 695, 7458: 7611, 7459: 7614, 7460: 738, 7461: 7516, 7462: 7518, 7463: 43870, 7465: 691, 7547: 7591, 7550: 7606, 7557: 43870, 7567: 7491, 7568: 7493, 7569: 7496, 7570: 7497, 7571: 7499, 7572: 7583, 7573: 7498, 7575: 7507, 7577: 43871, 11362: 43870, 11364: 7487, 11373: 7493, 11374: 7596, 11375: 7492, 11376: 7579, 11377: 11389, 11387: 7474, 42800: 7584, 42801: 738, 42862: 42864, 42863: 42864, 42870: 7487, 42893: 7587, 42894: 7593, 42922: 689, 42923: 7500, 42924: 7586, 42925: 43870, 42928: 7479, 42929: 7488, 43002: 7481, 43831: 43869, 43832: 43870, 43833: 43870, 43846: 7487, 43858: 43871, 43859: 7521, 43877: 7607}

_de_supertransltabl = {8317: 40, 8318: 41, 8314: 43, 8315: 45, 5159: 46, 8304: 48, 185: 49, 178: 50, 179: 51, 8308: 52, 8309: 53, 8310: 54, 8311: 55, 8312: 56, 8313: 57, 8316: 61, 7468: 65, 7470: 66, 7580: 67, 7472: 68, 7473: 69, 7584: 70, 7475: 71, 7476: 72, 7477: 73, 7478: 74, 7479: 75, 7480: 76, 7481: 77, 7482: 78, 7484: 79, 7486: 80, 5456: 81, 7487: 82, 738: 83, 7488: 84, 7489: 85, 11389: 86, 7490: 87, 739: 88, 89: 89, 7611: 90, 7491: 97, 7495: 98, 7496: 100, 7497: 101, 7501: 103, 688: 104, 8305: 105, 690: 106, 7503: 107, 737: 108, 7504: 109, 8319: 110, 7506: 111, 7510: 112, 691: 114, 7511: 116, 7512: 117, 7515: 118, 695: 119, 696: 121, 7469: 198, 7601: 216, 7582: 240, 43000: 294, 43870: 322, 7505: 330, 43001: 338, 7605: 354, 7507: 390, 7474: 398, 7498: 399, 7499: 400, 736: 404, 7590: 406, 7588: 407, 7514: 412, 7598: 413, 7604: 425, 7607: 433, 7614: 439, 7485: 546, 7599: 565, 740: 578, 7606: 580, 7610: 581, 7492: 592, 7493: 593, 7579: 594, 7581: 597, 7500: 604, 693: 605, 7585: 607, 7586: 608, 7609: 612, 7587: 613, 689: 614, 43868: 615, 7593: 621, 7597: 624, 7596: 625, 7600: 628, 7602: 632, 692: 633, 694: 641, 7603: 642, 7612: 656, 7613: 657, 704: 660, 705: 661, 7544: 668, 7592: 669, 7594: 682, 43869: 683, 7518: 915, 7589: 921, 7520: 934, 7521: 935, 7517: 946, 7519: 948, 7615: 952, 7494: 7425, 7471: 7427, 7583: 7431, 7502: 7433, 7483: 7438, 7508: 7446, 7509: 7447, 7513: 7453, 7516: 7461, 7591: 7547, 734: 7570, 43871: 7577, 42864: 42862}


def subscript(itm, decode=False):
    "Returns str(itm) in subscript form using unicode characters.  "\
    "Works well for digits and a few arithmetic operators, but subscript letters are sparse.  "\
    "The sister function, superscript, works much better."
    v = str(itm)
    return v.translate(_de_subtransltabl if decode else _subtransltabl)

def superscript(itm, decode=False):
    "Returns str(itm) in subscript form using unicode characters (see subscript).  "\
    "While there are plenty of altered forms, duplicate or identical but different versions of "\
    "any given character in the Latin alphabet, for some reason there is no sub-or-superscript"\
    " “q”, so the closest approximation, u1550//“CANADIAN SYLLABICS R”//‘ᕐ’// is used instead."
    v = str(itm)
    return v.translate(_de_supertransltabl if decode else _supertransltabl)


def getname(obj, dflt=None, *, call=False, alias='name'):
    "Tries to return obj.__name__.  If not found, falls back on getattr(obj, ‘alias’,) (if alias is not None), "\
    "and, failing that, resorts to ‘dflt’.  If ‘call’ == True, returns dflt(obj), otheewise returns dflt."
    if alias is None: return getattr(obj, '__name__', getattr(obj, alias, dflt if not call else dflt(obj)))
    return getattr(obj, '__name__', dflt if not call else dflt(obj))
    
def clsname(obj, dflt=None, *, call=False, alias=None):
    "Calls getname with the given inputs on obj.__class__--(or type(obj), if that fails for some reason)."
    return getname(getattr(obj, '__class__', type(obj)), dflt=dflt, call=call)
    


"printfuncs (1)"

def try_format(item, format_spec, *fallbacks):
    try:
        st = format(item, format_spec)
    except TypeError:
        if fallbacks: return try_format(item, *fallbacks)
        if format_spec: return try_format(item, '')
        raise
    else: return st
        

def fept(strings: str, *, split=', ', sep='\n', end='\n\n', format_spec='', globals_=None, **kwg):
    '''Specifically for when you’ve already typed out a long, incomprehensible print statement '''\
    '''and don’t want to manually change each value to the «f"{x = }"» form.  '''\
    '''Example:   \n'''\
    '''    print(a, b, a*b, c, (d,p,q), (b|d)^(p|q)) \n'''\
    '''     →+(f,",") \n'''\
    '''    → fprint("a, b, a*b, c, (d,p,q), (b|d)^(p|q)") → \n'''\
    "a = 3 \n"\
    "b = 5 \n"\
    "a*b = 15 \n"\
    "c = 15 \n"\
    "(d,p,q) = (7, 11, 13) \n"\
    "(b|d)^(p|q) = 8"
    formst = ("{0} = :"+format_spec).format
    strings = f'}}{sep}{{'.join(map(formst, strings.split(split)))
    if kwg.pop('preview', 0):
        print("f'''{"+strings+"}'''", **kwg)
    print(eval("f'''{"+strings+"}'''", globals_ or globals()), end=end, **kwg)

fprint = fept


Printers__ = [rpt, printrows, fept, prinL2, pri_]


__all__ = ['nL', 'nT', 'nT2', 'nL2', 'nLT', 'nL2T', 'nLT2',
         '_jo_', '_jc_', '_jnL', '_jnT', '_jnLT', '_jnL2', '_jnLT2', 
         'jo', 'jo_', 'jc_', 'jnT', 'jnL', 'jnLT', 'jnL2', 'jnLT2', 
         '_jB', '_jBn', '_jBnx', '_jBnL', '_jB_', 
         'jB', 'jBn', 'jBnx', 'jBnL', 'jB_',  
         "join", "joinst", "subscript", "superscript", 
          'strEscapeSeprs', 
          'strJoiners', 'byteJoiners', 'strJoinsters', 'byteJoinsters', 
           '_formst_kyvl', 'Formstrs__', "getname", "clsname", 
            'rpt', 'derpt', 'printrows', 'fprint', 'fept', "prinL2", "pri_",
            'Printers__', 
            'OutputSummoner', 'EndExc', 'endexc'
            ]


#!/usr/local/bin/python
# coding: utf-8 -*-
from typing import Callable, Any
from itertools import cycle


__name__ = "StringStuff"

'''
print(...)
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
    
    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
'''

class OutputSummoner(Exception):
        """ Dummy Exception for summoning output window """
        #pass
        def rais(self, header='\n\n', msg=None, traceback=None, cause=None, **printkwg):
            import tkinter
            slf = self
            if msg is not None:
                slf = type(self)(msg)
            if traceback is not None:
                slf = slf.with_traceback(traceback)
            print(header, **printkwg)
            raise slf from cause

ExceptionPass = OutputSummoner

EndExc = ExceptionPass("    ...    End")

def endexc(exc=EndExc):
    exc.rais()


if "print (0)":
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
        "Accepts an instance of-, or the bound join method of- an instance of str or bytes, "\
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
    
    
    def _stq(sq, qey: type=list, sr: Callable[[Any], str]=str, maxlen=100):
        '''  ? ¿ ? ¿ '''
        end = len(str(sq))
        if maxlen:
            end = min(maxlen, end)
        if isinstance(sq, str):
            sq = sq.splitlines()
        if callable(qey):
            reseq = qey(iter(_stq(sq, None, sr=sr, maxlen=maxlen)))
            if hasattr(reseq, "__getitem__"):
                if not isinstance(reseq, str):
                    end = (end) // max(1,len(max(reseq, key=len)))
                return reseq[:end]()
        return (sr(it) for it in sq)
    
    
    subsupref = (('1', '₁', '¹'), ('2', '₂', '²'), ('3', '₃', '³'),
     ('4', '₄', '⁴'), ('5', '₅', '⁵'), ('6', '₆', '⁶'), ('7', '₇', '⁷'), ('8', '₈', '⁸'), 
     ('9', '₉', '⁹'), ('0', '₀', '⁰'), (' ', ' ', ' '), 
     ('a', 'ᵃ', 'ᵃ'), ('b', 'ᵇ', 'ᵇ'), ('c', 'ᶜ', 'ᶜ'), ('d', 'ᵈ', 'ᵈ'), ('e', 'ᵉ', 'ᵉ'), 
     ('f', 'ᶠ', 'ᶠ'), ('g', 'ᶢ', 'ᶢ'), ('h', 'ʰ', 'ʰ'), ('i', 'ⁱ', 'ⁱ'), ('j', 'ʲ', 'ʲ'), 
     ('k', 'ᵏ', 'ᵏ'), ('l', 'ˡ', 'ˡ'), ('m', 'ᵐ', 'ᵐ'), ('n', 'ⁿ', 'ⁿ'), ('o', 'ᵒ', 'ᵒ'), 
     ('p', 'ᵖ', 'ᵖ'), ('q', 'ᕐ', 'ᕐ'), ('r', 'ʳ', 'ʳ'), ('s', 'ˢ', 'ˢ'), ('t', 'ᵗ', 'ᵗ'), 
     ('u', 'ᵘ', 'ᵘ'), ('v', 'ᵛ', 'ᵛ'), ('w', 'ʷ', 'ʷ'), ('x', 'ˣ', 'ˣ'), ('y', 'ʸ', 'ʸ'), 
     ('z', 'ᶻ', 'ᶻ'), 
     ('.', '.', 'ˑ'), ('=', '₌', '⁼'), ('(', '₍', '⁽'), (')', '₎', '⁾'), ('+', '₊', '⁺'), ('-', '₋', '⁻'))
    
    "ₐ _ _ _ ₑ __ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ _ ᵣ ₛ ₜ ᵤ ᵥ _ ₓ _ _   _   _ ᵦ ᵧ   _ ___ _ _ _ _ _ _ _ _ _ _ _ ᵨ _ _ ᵩ    ᵪ"

    _supertransltabl = {40: '⁽', 41: '⁾', 43: '⁺', 45: '⁻', 46: 'ᐧ', 48: '⁰', 49: '¹', 50: '²', 51: '³', 52: '⁴', 53: '⁵', 54: '⁶', 55: '⁷', 56: '⁸', 57: '⁹', 61: '⁼', 65: 'ᴬ', 66: 'ᴮ', 67: 'ᶜ', 68: 'ᴰ', 69: 'ᴱ', 70: 'ᶠ', 71: 'ᴳ', 72: 'ᴴ', 73: 'ᴵ', 74: 'ᴶ', 75: 'ᴷ', 76: 'ᴸ', 77: 'ᴹ', 78: 'ᴺ', 79: 'ᴼ', 80: 'ᴾ', 81: 'ᕐ', 82: 'ᴿ', 83: 'ˢ', 84: 'ᵀ', 85: 'ᵁ', 86: 'ⱽ', 87: 'ᵂ', 88: 'ˣ', 89: 'Y', 90: 'ᶻ', 97: 'ᵃ', 98: 'ᵇ', 99: 'ᶜ', 100: 'ᵈ', 101: 'ᵉ', 102: 'ᶠ', 103: 'ᵍ', 104: 'ʰ', 105: 'ⁱ', 106: 'ʲ', 107: 'ᵏ', 108: 'ˡ', 109: 'ᵐ', 110: 'ⁿ', 111: 'ᵒ', 112: 'ᵖ', 113: 'ᕐ', 114: 'ʳ', 115: 'ˢ', 116: 'ᵗ', 117: 'ᵘ', 118: 'ᵛ', 119: 'ʷ', 120: 'ˣ', 121: 'ʸ', 122: 'ᶻ', 198: 'ᴭ', 199: 'ᶜ', 216: 'ᶱ', 231: 'ᶜ', 240: 'ᶞ', 248: 'ᶱ', 294: 'ꟸ', 295: 'ꟸ', 322: 'ꭞ', 330: 'ᵑ', 331: 'ᵑ', 338: 'ꟹ', 339: 'ꟹ', 354: 'ᶵ', 355: 'ᶵ', 385: 'ᴮ', 390: 'ᵓ', 391: 'ᶜ', 392: 'ᶜ', 393: 'ᶞ', 394: 'ᴰ', 398: 'ᴲ', 399: 'ᵊ', 400: 'ᵋ', 403: 'ᴳ', 404: 'ˠ', 406: 'ᶦ', 407: 'ᶤ', 408: 'ᴷ', 409: 'ᵏ', 411: 'ᵗ', 412: 'ᵚ', 413: 'ᶮ', 414: 'ᵑ', 415: 'ᶱ', 420: 'ᴾ', 421: 'ᵖ', 422: 'ᴿ', 425: 'ᶴ', 426: 'ᶴ', 428: 'ᵀ', 429: 'ᵗ', 430: 'ᶵ', 433: 'ᶷ', 434: 'ⱽ', 439: 'ᶾ', 442: 'ᶾ', 544: 'ᵑ', 545: 'ᵈ', 546: 'ᴽ', 547: 'ᴽ', 564: 'ᵈ', 565: 'ᶯ', 566: 'ᶵ', 568: 'ᵇ', 569: 'ᵖ', 578: 'ˤ', 580: 'ᶶ', 581: 'ᶺ', 586: 'ᕐ', 587: 'ᕐ', 592: 'ᵄ', 593: 'ᵅ', 594: 'ᶛ', 595: 'ᵇ', 596: 'ᵓ', 597: 'ᶝ', 598: 'ᵈ', 599: 'ᵈ', 600: 'ᵊ', 601: 'ᵊ', 602: 'ᵊ', 603: 'ᵋ', 604: 'ᵌ', 605: 'ʵ', 606: 'ᵋ', 607: 'ᶡ', 608: 'ᶢ', 609: 'ᶢ', 610: 'ᴳ', 611: 'ˠ', 612: 'ᶹ', 613: 'ᶣ', 614: 'ʱ', 615: 'ꭜ', 616: 'ᶤ', 618: 'ᶦ', 619: 'ꭞ', 620: 'ꭞ', 621: 'ᶩ', 622: 'ᶾ', 623: 'ᵚ', 624: 'ᶭ', 625: 'ᶬ', 626: 'ᶮ', 627: 'ᶯ', 628: 'ᶰ', 629: 'ᶱ', 630: 'ꟹ', 631: 'ᶷ', 632: 'ᶲ', 633: 'ʴ', 634: 'ʴ', 635: 'ʵ', 636: 'ʳ', 637: 'ʳ', 638: 'ʳ', 640: 'ᴿ', 641: 'ʶ', 642: 'ᶳ', 643: 'ᶴ', 644: 'ᶡ', 646: 'ᶴ', 647: 'ᵗ', 648: 'ᶵ', 649: 'ᶶ', 650: 'ᶷ', 651: 'ᵛ', 652: 'ᶺ', 653: 'ᶺ', 654: 'ꭞ', 655: 'ʸ', 656: 'ᶼ', 657: 'ᶽ', 658: 'ᶾ', 659: 'ᶾ', 660: 'ˀ', 661: 'ˁ', 662: 'ˀ', 663: 'ᶜ', 665: 'ᴮ', 667: 'ᴳ', 668: 'ᵸ', 669: 'ᶨ', 670: 'ᵏ', 671: 'ᶫ', 672: 'ᕐ', 673: 'ˀ', 674: 'ˁ', 675: 'ᶻ', 676: 'ᶾ', 677: 'ᶽ', 678: 'ˢ', 679: 'ᶴ', 680: 'ᶝ', 682: 'ᶪ', 683: 'ᶻ', 686: 'ᶣ', 687: 'ᶣ', 913: 'ᵅ', 914: 'ᴮ', 915: 'ᵞ', 916: 'ᴰ', 917: 'ᵋ', 918: 'ᶽ', 919: 'ꭜ', 920: 'ᶿ', 921: 'ᶥ', 922: 'ᴷ', 923: 'ᶫ', 924: 'ᴹ', 925: 'ᴺ', 926: 'ˣ', 927: 'ᴼ', 928: 'ᴾ', 929: 'ᴿ', 931: 'ˢ', 932: 'ᵀ', 933: 'ᶹ', 934: 'ᵠ', 935: 'ᵡ', 937: 'ᵂ', 945: 'ᵅ', 946: 'ᵝ', 947: 'ᵞ', 948: 'ᵟ', 949: 'ᵋ', 950: 'ᶽ', 951: 'ꭜ', 952: 'ᶿ', 953: 'ᶥ', 954: 'ᵏ', 955: 'ˡ', 956: 'ᵐ', 957: 'ⁿ', 958: 'ˣ', 959: 'ᵒ', 960: 'ᵖ', 961: 'ʳ', 962: 'ˢ', 963: 'ˢ', 964: 'ᵗ', 965: 'ᶷ', 966: 'ᶲ', 967: 'ᵡ', 969: 'ʷ', 984: 'ᕐ', 985: 'ᕐ', 7424: 'ᴀ', 7425: 'ᴭ', 7426: 'ᵆ', 7427: 'ᴯ', 7428: 'ᶜ', 7429: 'ᴰ', 7430: 'ᶞ', 7431: 'ᴱ', 7432: 'ᶟ', 7433: 'ᵎ', 7434: 'ᴶ', 7435: 'ᴷ', 7436: 'ꭞ', 7437: 'ᴹ', 7438: 'ᴻ', 7439: 'ᴼ', 7440: 'ᵓ', 7441: 'ᴼ', 7442: 'ᵒ', 7443: 'ᶱ', 7444: 'ꟹ', 7445: 'ᴽ', 7446: 'ᵔ', 7447: 'ᵕ', 7448: 'ᴾ', 7449: 'ʶ', 7450: 'ʶ', 7451: 'ᶴ', 7452: 'ᵁ', 7453: 'ᵙ', 7454: 'ᵙ', 7456: 'ᵛ', 7457: 'ʷ', 7458: 'ᶻ', 7459: 'ᶾ', 7460: 'ˢ', 7461: 'ᵜ', 7462: 'ᵞ', 7463: 'ꭞ', 7465: 'ʳ', 7547: 'ᶧ', 7550: 'ᶶ', 7557: 'ꭞ', 7567: 'ᵃ', 7568: 'ᵅ', 7569: 'ᵈ', 7570: 'ᵉ', 7571: 'ᵋ', 7572: 'ᶟ', 7573: 'ᵊ', 7575: 'ᵓ', 7577: 'ꭟ', 11362: 'ꭞ', 11364: 'ᴿ', 11373: 'ᵅ', 11374: 'ᶬ', 11375: 'ᵄ', 11376: 'ᶛ', 11377: 'ⱽ', 11387: 'ᴲ', 42800: 'ᶠ', 42801: 'ˢ', 42862: 'ꝰ', 42863: 'ꝰ', 42870: 'ᴿ', 42893: 'ᶣ', 42894: 'ᶩ', 42922: 'ʱ', 42923: 'ᵌ', 42924: 'ᶢ', 42925: 'ꭞ', 42928: 'ᴷ', 42929: 'ᵀ', 43002: 'ᴹ', 43831: 'ꭝ', 43832: 'ꭞ', 43833: 'ꭞ', 43846: 'ᴿ', 43858: 'ꭟ', 43859: 'ᵡ', 43877: 'ᶷ'}

    #| ''.maketrans({'Ɗ': 'ᴰ', 'ɖ': 'ᵈ', 'ɝ': 'ʵ', 'ʣ': 'ᶻ', 'ʤ': 'ᶾ', 'ʥ': 'ᶽ', 'ʦ': 'ˢ', 'ʧ': 'ᶴ', 'ᴛ': 'ᶴ', 'Λ': 'ᶫ', 'λ': 'ˡ', 'ʟ': 'ᶫ', 'ʨ': 'ᶝ', 'ɮ': 'ᶾ', 'ʪ': 'ᶪ', 'ʫ': 'ᶻ', 'ꞎ': 'ᶩ', 'Ɬ': 'ꭞ', 'ꬷ': 'ꭝ', 'ꬸ': 'ꭞ', 'ꬹ': 'ꭞ', 'Η': 'ꭜ', 'Θ': 'ᶿ', 'τ': 'ᵗ', 'ᴀ': 'ᴀ', 'ᴁ': 'ᴭ', 'ᴂ': 'ᵆ', 'ᴃ': 'ᴯ', 'ᴄ': 'ᶜ', 'ᴅ': 'ᴰ', 'ᴆ': 'ᶞ', 'ᴇ': 'ᴱ', 'ᴈ': 'ᶟ', 'ᴉ': 'ᵎ', 'ᴊ': 'ᴶ', 'ᴋ': 'ᴷ', 'ᴏ': 'ᴼ', 'ᴐ': 'ᵓ', 'ᴑ': 'ᴼ', 'ᴒ': 'ᵒ', 'ᴓ': 'ᶱ', 'ɶ': 'ꟹ', 'ᶒ': 'ᵉ', 'ᶓ': 'ᵋ', 'ᶔ': 'ᶟ', 'ᶕ': 'ᵊ', 'ᶗ': 'ᵓ', 'ⱻ': 'ᴲ', 'Ʞ': 'ᴷ'})
    _de_supertransltabl = {8317: '(', 8318: ')', 8314: '+', 8315: '-', 5159: '.', 8304: '0', 185: '1', 178: '2', 179: '3', 8308: '4', 8309: '5', 8310: '6', 8311: '7', 8312: '8', 8313: '9', 8316: '=', 7468: 'A', 7470: 'B', 7580: 'C', 7472: 'D', 7473: 'E', 7584: 'F', 7475: 'G', 7476: 'H', 7477: 'I', 7478: 'J', 7479: 'K', 7480: 'L', 7481: 'M', 7482: 'N', 7484: 'O', 7486: 'P', 5456: 'Q', 7487: 'R', 738: 'S', 7488: 'T', 7489: 'U', 11389: 'V', 7490: 'W', 739: 'X', 89: 'Y', 7611: 'Z', 7491: 'a', 7495: 'b', 7496: 'd', 7497: 'e', 7501: 'g', 688: 'h', 8305: 'i', 690: 'j', 7503: 'k', 737: 'l', 7504: 'm', 8319: 'n', 7506: 'o', 7510: 'p', 691: 'r', 7511: 't', 7512: 'u', 7515: 'v', 695: 'w', 696: 'y', 7469: 'Æ', 7601: 'Ø', 7582: 'ð', 43000: 'Ħ', 43870: 'ł', 7505: 'Ŋ', 43001: 'Œ', 7605: 'Ţ', 7507: 'Ɔ', 7474: 'Ǝ', 7498: 'Ə', 7499: 'Ɛ', 736: 'Ɣ', 7590: 'Ɩ', 7588: 'Ɨ', 7514: 'Ɯ', 7598: 'Ɲ', 7604: 'Ʃ', 7607: 'Ʊ', 7614: 'Ʒ', 7485: 'Ȣ', 7599: 'ȵ', 740: 'ɂ', 7606: 'Ʉ', 7610: 'Ʌ', 7492: 'ɐ', 7493: 'ɑ', 7579: 'ɒ', 7581: 'ɕ', 7500: 'ɜ', 693: 'ɝ', 7585: 'ɟ', 7586: 'ɠ', 7609: 'ɤ', 7587: 'ɥ', 689: 'ɦ', 43868: 'ɧ', 7593: 'ɭ', 7597: 'ɰ', 7596: 'ɱ', 7600: 'ɴ', 7602: 'ɸ', 692: 'ɹ', 694: 'ʁ', 7603: 'ʂ', 7612: 'ʐ', 7613: 'ʑ', 704: 'ʔ', 705: 'ʕ', 7544: 'ʜ', 7592: 'ʝ', 7594: 'ʪ', 43869: 'ʫ', 7518: 'Γ', 7589: 'Ι', 7520: 'Φ', 7521: 'Χ', 7517: 'β', 7519: 'δ', 7615: 'θ', 7494: 'ᴁ', 7471: 'ᴃ', 7583: 'ᴇ', 7502: 'ᴉ', 7483: 'ᴎ', 7508: 'ᴖ', 7509: 'ᴗ', 7513: 'ᴝ', 7516: 'ᴥ', 7591: 'ᵻ', 734: 'ᶒ', 43871: 'ᶙ', 42864: 'Ꝯ'}
    
    #print({(k): v for k,v in _supertransltabl.items()})
#    import tkinter
#    cᶜhʰsˢ = [print(f" {repr(chr(k))} →͢→ {repr(ᵛ)}") for k,ᵛ in _supertransltabl.items()]
#    0/0
#    endexc()
    def subscript(itm):
        "Returns str(itm) in subscript form using unicode characters.  "\
        "Works well for digits and a few arithmetic operators, but subscript letters are sparse.  "\
        "The sister function, superscript, works much better.  Symbols without subscript forms are superscripted by this function."
        cvrt = subsupref
        v = str(itm)
        
        for cv in cvrt:
            v = v.replace(*cv[:2:])
        return v
    def superscript(itm, decode=False):
        "Returns str(itm) in subscript form using unicode characters (see subscript).  "\
        "While there are plenty of altered forms, duplicate or identical but different versions of "\
        "any given character in the Latin alphabet, for some reason there is no sub-or-superscript"\
        " “q”, so the closest approximation, u1550//“CANADIAN SYLLABICS R”//‘ᕐ’// is used instead."
        #cvrt = subsupref
        v = str(itm)
        return v.translate(decode and _de_supertransltabl or _supertransltabl)
        #for cv in cvrt:
         #   v = v.replace(*cv[::2])
        #return=s v
    '''
    '''
    
    def getname(obj, dflt=None, *, call=False, alias='name'):
        "Tries to return obj.__name__.  If not found, falls back on getattr(obj, ‘alias’,) (if alias is not None), "\
        "and, failing that, resorts to ‘dflt’.  If ‘call’ == True, returns dflt(obj), otheewise returns dflt."
        if alias is None: return getattr(obj, '__name__', getattr(obj, alias, dflt if not call else dflt(obj)))
        return getattr(obj, '__name__', dflt if not call else dflt(obj))
        
    def clsname(obj, dflt=None, *, call=False, alias=None):
        "Calls getname with the given inputs on obj.__class__--(or type(obj), if that fails for some reason)."
        return getname(getattr(obj, '__class__', type(obj)), dflt=dflt, call=call)
        
    

if "print (1)":
    
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
        '''    «print(a, b, a*b, c, (d,p,q), (b|d)^(p|q))» →+(f,",")→ fprint("a, b, a*b, c, (d,p,q), (b|d)^(p|q)") → \n'''\
        "a = 3 \n"\
        "b = 5 \n"\
        "a*b = 15 \n"\
        "c = 15 \n"\
        "(d,p,q) = (7, 11, 13) \n"\
        "(b|d)^(p|q) = 8"
        #strings = f'}}{sep}{{'.join(f"{s} = :{format_spec}" for s in strings)
        formst = ("{0} = :"+format_spec).format
        strings = f'}}{sep}{{'.join(map(formst, strings.split(split)))
        if kwg.pop('preview', 0):
            print("f'''{"+strings+"}'''", **kwg)
        print(eval("f'''{"+strings+"}'''", globals_ or globals()), end=end, **kwg)
    
    fprint = fept
    
    
    '''def evlpt(descr, *value: [str], joint=':  ', sep=nLT, end='\n', **kwg):
        if not value:    value = [descr]
        value = listize(value)
        #print(value)
        vstrs = (str(v) + joint for v in value)
        value = value+ value
        vgets = (eval(str(v)) for v in value)
        vstrvs = (f"{vs}{vgets.__next__()}" for vs in vstrs)
        print(sep, end='')
        print(*vstrvs, sep=sep, end=end, **kwg)
        if len(value) == 1:    return vgets.__next__()
            #return exec(value[0])
        return list(vgets)
        #return [exec(v) for v in value]
    
    def pritrf(formstr, *value: [str], sep=' ', end='\n', **kwg):
        value = listize(value)
        vstrs = [[str(v).strip("}{") for v in listize(val)] for val in value]
        fstitr = (fst.format for fst in itrtls.cycle(listize(formstr)))
        try:
            vstrs = rpt("vstrs=", *[next(fstitr)(*vst) for vi, vst in enumerate(vstrs)])
            print(*vstrs, sep=sep, end=end, **kwg)
        except ValueError as exc:
            print("ValueError", exc)
            fstitr = (lambda *s: fst.__add__(str(s)) for fst in cycle(listize(formstr)))
            vstrs = rpt("vstrs=", *[next(fstitr)(*vst) for vi, vst in enumerate(vstrs)])
            print(*vstrs, sep=sep, end=end, **kwg)'''

#evlpt("", *["1/2","2/3","3/4","4/5","5/6","6/7"])

Printers__ = [rpt, printrows, fept, prinL2, pri_]


#globs = globals().copy()
#_all__ = list(globs.keys())
#allomits = ["_all__", "globs", 'sys', '_', '__all__', \
#    "allomits", "__name__"]

#for aky in allomits:
#    if aky in _all__:
#        _all__.remove(aky)

#__all__ = list(_all__)#.__add__(["__all__"])
#print(__all__)
__all__ = ['nL', 'nT', 'nT2', 'nL2', 'nLT', 'nL2T', 'nLT2',
         '_jo_', '_jc_', '_jnL', '_jnT', '_jnLT', '_jnL2', '_jnLT2', 
         'jo', 'jo_', 'jc_', 'jnT', 'jnL', 'jnLT', 'jnL2', 'jnLT2', 
         '_jB', '_jBn', '_jBnx', '_jBnL', '_jB_', 
         'jB', 'jBn', 'jBnx', 'jBnL', 'jB_',  
         "join", "joinst", "subscript", "superscript", 
          'strEscapeSeprs', 
          'strJoiners', 'byteJoiners', 'strJoinsters', 'byteJoinsters', 
           '_formst_kyvl', 'Formstrs__', '_stq', "getname", "clsname", 
            'rpt', 'derpt', 'printrows', 'fprint', 'fept', "prinL2", "pri_",
            'Printers__', 
            'OutputSummoner', 'EndExc', 'endexc'
            ]


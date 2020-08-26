import unicodedata
import re


def stripAccents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def removeUnknownSymbols(s):
    for i in range(len(s)):
        char = s[i]
        if ord(char) > 127:
            s = s[:i] + " " + s[i+1:]
    return s


def noParentheses(s):
    while True:
        i = 0
        while i < len(s):
            if s[i] == "(":
                break
            i += 1
        if i >= len(s):
            break
        j = i+1
        while j < len(s):
            if s[j] == ")":
                s = s[:i] + s[j+1:]
            j += 1
        if j >= len(s):
            break
    return s


def doHyphens(s):
    # for i in range(1,len(s)-1):
    #     if s[i] == "-":
    #         if s[i-1] != " " and s[i+1] != " ":
    #             s = s[:i] + " " + s[i+1:]
    s = s.replace('- ', '')
    return s


def removeColon(s):
    s = s.replace(':', '')
    return s


def removeComma(s):
    s = s.replace(',', '')
    return s


def norm(s):
    return doHyphens(noParentheses(removeUnknownSymbols(stripAccents(s))))


def normName(s):
    return removeComma(removeColon(norm(s))).lower()


def normImdbId(s):
    return " ".join((re.sub(r"([^\s\w\.!']|_)+", ' ', norm(s))).split())


def normUrl(s):
    return " ".join((re.sub(r"([^\w!-])+", ' ', norm(s).replace("'", "").replace(".", ""))).split()).lower()


def normUrlRt(s):
    return normUrl(s.replace("&", "and"))

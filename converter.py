import re


def encodeToXML(methodName, url, keyword, depth):
    return f'<methodCall><methodName>{methodName}</methodName><params><param><value><string>{url}</string></value></param><param><value><string>{keyword}</string></value></param><param><value><int>+{depth}</int></value><param></params></value>'


def decodeToValues(XMLString):
    vals = []
    methodNameRegex = '<methodName>((.|\n)*?)<\\/methodName>'
    stringsRegex = '<string>((.|\n)*?)<\\/string>'
    integerRegex = '<int>((.|\n)*?)<\\/int>'

    vals.append(re.findall(methodNameRegex, XMLString)[0][0])
    vals.append(re.findall(stringsRegex, XMLString)[0][0])
    vals.append(re.findall(stringsRegex, XMLString)[1][0])
    vals.append(int(re.findall(integerRegex, XMLString)[0][1]))
    return vals

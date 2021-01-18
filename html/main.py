import re
import inspect


class HTMLTree:
    def __init__(self, type, attributes, body):
        """
        Constructor
        """
        self.type = type
        self.attributes = attributes
        self.body = body

    def __str__(self):
        return f"Type: {self.type}, Attributes: {','.join(self.attributes)}, Body: \n{self.body}"


class HTMLParser:
    def __init__(self, data):
        """
        Constructor
        """
        self.genericVariables = [i for i in dir(self) if not inspect.ismethod(i)]
        self.genericVariables.append("genericVariables")
        self.decode(data)

    def decode(self, data):
        """
        A function to decode html
        """
        data = re.sub("<!--(.*?)-->", "", data)
        self.parse(data)

    def parse(self, data):
        tags = re.findall("<([A-Za-z]*)[A-Za-z0-9= \"\-]*>", data)
        for tag in tags:
            try:
                try:
                    attributes = re.findall("<[A-Za-z]* ([A-Za-z0-9= \"\-]+)>", data)[0].split(" ")
                except IndexError:
                    attributes = []
                bodyData = re.findall(f"<{tag}>(.*)</{tag}>", data, flags=re.S)[0]
                setattr(self, tag, HTMLTree(tag, attributes, bodyData))
                self.parse(bodyData)
            except IndexError:
                return

    def __str__(self):
        [print(getattr(self, i)) for i in dir(self) if not inspect.ismethod(i) and i not in self.genericVariables]
        return ' '.join([i for i in dir(self) if not inspect.ismethod(i) and i not in self.genericVariables])


with open(r"C:\Users\olive\Desktop\Coding\After Da USB\Parsers\html\example.html") as f:
    data = f.read()
    html = HTMLParser(data)
    print(html)
    print(html.head)

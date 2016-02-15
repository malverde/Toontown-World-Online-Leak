#!/usr/bin/env python2
import collections
import compiler
import re


class CategoryParser:
    def __init__(self, filepath):
        self.filepath = filepath

        self.categories = {}

    def parse(self):
        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                if (not line.startswith('# --- ')) or (not line.endswith(' ---')):
                    continue
                self.addCategory(i + 1, line[6:-4].title())

    def addCategory(self, lineno, category):
        self.categories[lineno] = category

    def getCategory(self, lineno):
        category = 'Unknown'
        for k in sorted(self.categories.keys()):
            if k > lineno:
                break
            category = self.categories[k]
        return category


class MethodParser(CategoryParser):
    def __init__(self, filepath):
        CategoryParser.__init__(self, filepath)

        # Order matters, so store the method information in an OrderedDict:
        self.methods = collections.OrderedDict()

    def parse(self):
        CategoryParser.parse(self)

        # Get the root node:
        node = compiler.parseFile(self.filepath).node

        # Parse any class objects:
        for child in node.getChildren():
            if isinstance(child, compiler.ast.Class):
                self.parseClass(child)

    def parseClass(self, node):
        # Skip past the class definition, and go into the body:
        stmt = node.getChildNodes()[-1]

        # Parse any function objects:
        for child in stmt.getChildren():
            if isinstance(child, compiler.ast.Function):
                self.parseFunction(child)

    def parseFunction(self, node):
        # First, verify that this is an RPC method:
        if not node.name.startswith('rpc_'):
            # RPC methods are required to have their name begin with 'rpc_'.
            return
        name = node.name[4:]
        if node.decorators is None:
            # RPC methods are also required to utilize the @rpcmethod
            # decorator.
            return
        for decorator in node.decorators:
            if decorator.node.name != 'rpcmethod':
                continue
            accessLevel = 'Unknown'
            for arg in decorator.args:
                if arg.name != 'accessLevel':
                    continue

                # Format the access level string:
                accessLevel = ' '.join(arg.expr.name.split('_')).title()
            break
        else:
            return

        # A docstring is also required:
        if node.doc is None:
            return

        # Get rid of the indentation in our docstring so that we can have an
        # easier time parsing it:
        lines = node.doc.split('\n')
        for i, line in enumerate(lines):
            lines[i] = line.lstrip()
        doc = '\n'.join(lines)

        # Get the category in which this method is underneath:
        category = self.getCategory(node.lineno)

        # Store this method's information:
        self.methods.setdefault(category, []).append((name, accessLevel, doc))

    def getMethods(self):
        return self.methods


class MediaWikiGenerator:
    def __init__(self, methods):
        self.methods = methods

        self.content = ''

    def generate(self):
        # Start on a clean slate:
        self.content = ''

        # Write the documentation header:
        self.writeHeader()

        # Write the categories and methods:
        for category, methods in self.methods.items():
            self.writeCategory(category)
            for name, accessLevel, doc in methods:
                self.writeMethod(name, accessLevel, doc)

        # Write the documentation footer:
        self.writeFooter()

        return self.content

    def writeHeader(self):
        # Force a table of contents:
        self.content += '__TOC__\n'

    def writeCategory(self, category):
        self.content += '= %s =\n' % category

    def writeMethod(self, name, accessLevel, doc):
        # First, add the method name and access level:
        self.writeHeading(3, name + ' <sub>- <code>%s</code></sub>' % accessLevel)

        # Split the docstring by the '\n\n' terminator:
        doc = doc.split('\n\n')

        # A summary is required, so let's assume it's first:
        summary = doc[0][9:].strip()
        self.writeBlockQuote(' '.join(summary.split('\n')))

        # Let's do parameters next if we have them:
        for entry in doc:
            if entry.startswith('Parameters:'):
                entry = entry[13:].strip()
                break
        else:
            entry = None
        if entry is not None:
            parameters = []
            for parameter in re.split('\\n\\[|\\n<', entry):
                name, description = parameter.split(' = ', 1)
                type, name = name.strip()[:-1].split(' ', 1)
                description = ' '.join(description.split('\n'))
                parameters.append((name, type, description))
            self.writeParameters(parameters)

        # Finally, we have an optional example response:
        for entry in doc:
            if entry.startswith('Example response:'):
                entry = entry[18:].strip()
                break
        else:
            entry = None
        if entry is not None:
            self.content += '{|\n'
            self.content += '|-\n'
            if (not entry.startswith('On success:')) or (
                'On failure:' not in entry):
                # Generate a single-row table:
                self.content += '! Example Response\n'
                self.content += '| <nowiki>%s</nowiki>\n' % entry
            else:
                # Generate a double-row table:
                success, failure = entry[12:].split('On failure:', 1)
                self.content += '! rowspan="2"|Example Response\n'
                self.content += '| Success\n'
                self.content += '| <nowiki>%s</nowiki>\n' % success.strip()
                self.content += '|-\n'
                self.content += '| Failure\n'
                self.content += '| <nowiki>%s</nowiki>\n' % failure.strip()
            self.content += '|}\n'

        return self.content

    def writeHeading(self, size, text):
        self.content += '<h%d>%s</h%d>\n' % (size, text, size)

    def writeBlockQuote(self, text):
        self.content += '<blockquote><nowiki>%s</nowiki></blockquote>\n' % text

    def writeParameters(self, parameters):
        self.content += '{|\n'
        self.content += '|-\n'
        self.content += '! rowspan="%d"|Parameters\n' % (len(parameters) + 1)
        self.content += '! Name\n'
        self.content += '! Type\n'
        self.content += '! Description\n'
        for name, type, description in parameters:
            self.content += '|-\n'
            self.content += '| <nowiki>%s</nowiki>\n' % name
            self.content += '| <nowiki>%s</nowiki>\n' % type
            self.content += '| <nowiki>%s</nowiki>\n' % description
        self.content += '|}\n'

    def writeFooter(self):
        # Let the reader know that this documentation was automatically
        # generated:
        self.content += '----\n'
        self.content += ("''This document was automatically generated by the "
                         "<code>write_rpc_doc.py</code> utility.''\n")


parser = MethodParser('toontown/rpc/ToontownRPCHandler.py')
parser.parse()
generator = MediaWikiGenerator(parser.getMethods())
with open('wiki.txt', 'w') as f:
    f.write(generator.generate())

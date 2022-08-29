class Obfuscatator:
    contextLevel = 0        # Used to keep track of the current level of indentation for the current line
    origLines = []          # List of the original lines from the file
    newLines = []           # List of the modified lines that will be written to the file
    currentLine = ''        # The current line that is being obfuscated
    names = {               # Dictionary of all the names that are being used
        'imports': [],      # List of all the import variables that have been obfuscated
        'functions': [],    # List of all the function names that have been obfuscated
        'arguments': [],    # List of all the function arguments that have been obfuscated
        'variables': [],    # List of all the variables that have been obfuscated
        'classes': [],      # List of all the class names that have been obfuscated
        'objects': []       # List of all the object instances that have been obfuscated
    }
    updateLater = {
        # A dictionary of any lines that need to be added to the new lines list after a certain point in the code
        # ie: The obfuscated init function for a class that is made into a variable can only be added after the
        # class has been defined.
        # <contextLevel> : <line>
    }

    def __init__(self, file):
        self.file = file
        self.obfuscate()

    def obfuscate(self):
            print('Obfuscating...')
            print('Getting lines from file...')
            self._getLines()

            print('Obfuscating imports...')
            print('Obfuscating functions...')
            print('Obfuscating variables...')
            print('Obfuscating classes...')
            print('Obfuscating objects...')

            for line in self.origLines:
                self.currentLine = line
                self.contextLevel = 0
                for i in self.currentLine:
                    if i == ' ':
                        self.contextLevel += 1
                    else:
                        break
                self.type = self._getNameType(self.currentLine)
                self._checkLineForNames(self.currentLine, self.type)
                
                if self.type == 'imports':
                    self._obfuscateImports(self.currentLine, var=True)
                elif self.type == 'importAs':
                    self._obfuscateImports(self.currentLine, var=False)
                elif self.type == 'functions':
                    self._obfuscateFunctions(self.currentLine)
                elif self.type == 'arguments':
                    self._obfuscateFunctions(self.currentLine, args=True)
                elif self.type == 'variables':
                    self._obfuscateVariables(self.currentLine)
                # elif self.type == 'classes':
                #     self._obfuscateClasses(self.currentLine)
                # elif self.type == 'objects':
                #     self._obfuscateObjects(self.currentLine)

                self.newLines.append(self.currentLine)
                
            print('Writing to file...')
            self._writeLines()
            print('Done!')

    def _getLines(self):
        with open(self.file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.origLines.append(line)

    def _writeLines(self):
        with open(self.file, 'w') as f:
            for line in self.newLines:
                f.write(line)
    
    def _getNewName(self, prefix='lol'):
        import secrets
        import string
        import hashlib
        return prefix + hashlib.sha512(''.join(secrets.choice(string.ascii_lowercase) for _ in range(45)).encode()).hexdigest()[:10]

    def _getNameType(self, line):
        if 'import ' in line and ' as ' in line:
            return 'imports'
        elif 'import ' in line:
            return 'importAs'
        elif 'def ' in line and '(' in line:
            test = line.split('def ')[1].split('(')[1]
            return 'arguments' if len(test) > 1 else 'functions'
        elif ' = ' in line and '(' not in line:
            return 'variables'
        elif ' = ' in line:
            return 'objects'
        elif 'class ' in line and ':' in line:
            return 'classes'
        else:
            return None

    def _checkLineForNames(self, line, kind=None):
        # TODO: Update to this later
        # This should work better than the current way it is implemented, but it doesn't
        
        # import string
        # newLine = ''.join(" " if char == string.punctuation else char for char in line)
        # words = newLine.split(' ')
        # for word in words:
        #     for kind in self.names.keys():
        #         if word.strip() in self.names[kind]:
        #             line = line.replace(word, self.names[kind][word])
        
        pun = ['', ' ', '=', '(', ')', '[', ']', '{', '}', '<', '>', '!', '@', '#', '$', '%', '^', '&', '*', '+', '-', '/', '\\', '|', ';', ':', '"', "'", ',', '.', '?', '~', '`', '_', '\n']

        if kind is None:
            for name in self.names.keys():
                for value in self.names[name]:
                    try:
                        if value[0] in line:
                            test = line.split(value[0])
                            if test[1][0] in pun and test[0][-1] in pun:
                                line = line.replace(value[0], value[1])
                    except IndexError:
                        if test[0] in pun:
                            line = line.replace(value[0], value[1])
                    except ValueError:
                        print(value)
        else:
            for value in self.names[kind]:
                try:
                    if value[0] in line:
                        test = line.split(value[0])
                        if test[1][0] in pun and test[0][-1] in pun:
                            line = line.replace(value[0], value[1])
                except IndexError:
                    if test[0] in pun:
                        line = line.replace(value[0], value[1])
                except ValueError:
                    print(value)

        self.currentLine = line

    def _obfuscateImports(self, line, var=False):
        if var:
            newName = line.split('import ')[1].strip()
            if newName not in self.names:
                self._updateCurrentLine('imports', newName, line)
        else:
            importName = line.split(' as ')[1].strip()
            if importName not in self.names:
                self._updateCurrentLine('variables', importName, line)

    def _obfuscateFunctions(self, line, args=False):
        if 'def ' in line:
            name, dirtyArgs = line.split('def ')[1].split('(')
            if name not in self.names:
                self._updateCurrentLine('functions', name, line)
            args = dirtyArgs.split(')')[0]
            if args != '':
                for arg in args.split(','):
                    if arg.strip() not in self.names:
                        self._updateCurrentLine('variables', arg, self.currentLine)
        else:
            self.currentLine = line

    def _extractInits(self, line):
        # This is something that I want to implement later
        # Will probably require rewriting the whole script
        # IE: 
        # Class X def __init__(self) becomes 
        # def garbage(self)
        # Class X.__init__ = garbage()
        print('lol, not yet')

    def _obfuscateVariables(self, line):
        if ' = ' in line:
            name = line.split(' = ')[0].strip()
            if name not in self.names:
                self._updateCurrentLine('variables', name, line)
        else:
            self.currentLine = line

    def _obfuscateStrings(self, line):
        # Need to test this
        # 1. Make into character arrays
        # 2. Hex encode each character
        charArry = list(line)
        for i in charArry:
            charArry[i] = hex(ord(charArry[i]))
        return charArry

    def _updateCurrentLine(self, type, value, line):
        newName = self._getNewName()
        self.names[type].append([value, newName])
        self.currentLine = line.replace(value, newName)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        Obfuscatator(sys.argv[1])
    else:
        # TODO: Uncomment and remove the second line
        # print('Please provide a file to obfuscate.')
        obfuscator = Obfuscatator('test.py')
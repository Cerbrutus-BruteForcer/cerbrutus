import os


class Wordlist:
    words = []

    def __init__(self, path, words=[]):
        if os.path.exists(path) and os.path.isfile(path):
            self.path = path
        else:
            raise FileNotFoundError(f"[!] - {path} cannot be found")

        if isinstance(words, list) and words:
            self.words = words

    def read(self, append=False):
        if not append:
            self.words = []
        try:
            with open(self.path, 'rb') as words_file:
                for line in words_file.readlines():
                    if not line:
                        continue
                    try:
                        self.words.append(line.decode('UTF-8').strip())
                    except UnicodeDecodeError:
                        # print("Skipping... ", end="")
                        # print(line)
                        try:
                            self.words.append(line.decode('Latin-1').strip())
                            # print(f"Read successfully {line.decode('Latin-1')}")
                        except UnicodeDecodeError:
                            continue
                        
            print(f"Read in {len(self.words)} words from {self.path}")
        except IOError:
            raise IOError(f"File {self.path} is not readable...")
        return self.words

    def write(self):
        if not self.words:
            print("No words to write")
            return

        try:
            with open(self.path, 'w') as f:
                print(f"Writing {len(self.words)} words to {self.path} ")
                for word in self.words:
                    print(word.encode('utf-8'), file=f)
        except IOError:
            raise IOError(f"File {self.path} cannot be written to")

    def clean(self):
        self.read()
        self.write()        
        print(f"Successfully Wrote {len(self.words)} to {self.path}")

    '''
    def extend(self):
        # Will extend the password list
        pass
    '''
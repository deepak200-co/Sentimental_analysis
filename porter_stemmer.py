class PorterStemmer:

    def __init__(self):
        self.vowels = ('a', 'e', 'i', 'o', 'u')
        self.word = ''
        self.end = 0
        self.start = 0
        self.offset = 0

    def is_vowel(self, letter):
        return letter in self.vowels

    def is_consonant(self, index):
        if self.is_vowel(self.word[index]):
            return False
        if self.word[index] == 'y':
            if index == self.start:
                return True
            else:
                return not self.is_consonant(index - 1)
        return True

    def m(self):  # measure
        """
           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.start
        while True:
            if i > self.offset:
                return n
            if not self.is_consonant(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.offset:
                    return n
                if self.is_consonant(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self.offset:
                    return n
                if not self.is_consonant(i):
                    break
                i += 1
            i += 1

    def contains_vowel(self):
        for i in range(self.start, self.offset + 1):
            if not self.is_consonant(i):
                return True
        return False

    def contains_double_consonant(self, j):
        if j < (self.start + 1):
            return False
        if self.word[j] != self.word[j - 1]:
            return False
        return self.is_consonant(j)

    def is_of_form_cvc(self, i):
        if i < (self.start + 2) or not self.is_consonant(i) or self.is_consonant(i - 1) or not self.is_consonant(i - 2):
            return 0
        ch = self.word[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends_with(self, s):
        length = len(s)
        if s[length - 1] != self.word[self.end]:  # tiny speed-up
            return False
        if length > (self.end - self.start + 1):
            return False
        if self.word[self.end - length + 1: self.end + 1] != s:
            return False
        self.offset = self.end - length
        return True

    def set_to(self, s):
        length = len(s)
        self.word = self.word[:self.offset + 1] + \
            s + self.word[self.offset + length + 1:]
        self.end = self.offset + length

    def replace_morpheme(self, s):
        if self.m() > 0:
            self.set_to(s)

    def remove_plurals(self):
        """
           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat
           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable
           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess
           meetings  ->  meet
        """
        if self.word[self.end] == 's':
            if self.ends_with("sses"):
                self.end = self.end - 2
            elif self.ends_with("ies"):
                self.set_to("i")
            elif self.word[self.end - 1] != 's':
                self.end = self.end - 1
        if self.ends_with("eed"):
            if self.m() > 0:
                self.end = self.end - 1
        elif (self.ends_with("ed") or self.ends_with("ing")) and self.contains_vowel():
            self.end = self.offset
            if self.ends_with("at"):
                self.set_to("ate")
            elif self.ends_with("bl"):
                self.set_to("ble")
            elif self.ends_with("iz"):
                self.set_to("ize")
            elif self.contains_double_consonant(self.end):
                self.end = self.end - 1
                ch = self.word[self.end]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.end = self.end + 1
            elif self.m() == 1 and self.is_of_form_cvc(self.end):
                self.set_to("e")

    def terminal_y_to_i(self):
        if self.ends_with('y') and self.contains_vowel():
            self.word = self.word[:self.end] + 'i' + self.word[self.end + 1:]

    def map_double_to_single_suffix(self):
        # relational --> relate
        # conditional --> condition
        # digitizer --> digitize
        if self.word[self.end - 1] == 'a':
            if self.ends_with("ational"):
                self.replace_morpheme("ate")
            elif self.ends_with("tional"):
                self.replace_morpheme("tion")
        elif self.word[self.end - 1] == 'c':
            if self.ends_with("enci"):
                self.replace_morpheme("ence")
            elif self.ends_with("anci"):
                self.replace_morpheme("ance")
        elif self.word[self.end - 1] == 'e':
            if self.ends_with("izer"):
                self.replace_morpheme("ize")
        elif self.word[self.end - 1] == 'l':
            if self.ends_with("bli"):
                self.replace_morpheme("ble")
            elif self.ends_with("alli"):
                self.replace_morpheme("al")
            elif self.ends_with("entli"):
                self.replace_morpheme("ent")
            elif self.ends_with("eli"):
                self.replace_morpheme("e")
            elif self.ends_with("ousli"):
                self.replace_morpheme("ous")
        elif self.word[self.end - 1] == 'o':
            if self.ends_with("ization"):
                self.replace_morpheme("ize")
            elif self.ends_with("ation"):
                self.replace_morpheme("ate")
            elif self.ends_with("ator"):
                self.replace_morpheme("ate")
        elif self.word[self.end - 1] == 's':
            if self.ends_with("alism"):
                self.replace_morpheme("al")
            elif self.ends_with("iveness"):
                self.replace_morpheme("ive")
            elif self.ends_with("fulness"):
                self.replace_morpheme("ful")
            elif self.ends_with("ousness"):
                self.replace_morpheme("ous")
        elif self.word[self.end - 1] == 't':
            if self.ends_with("aliti"):
                self.replace_morpheme("al")
            elif self.ends_with("iviti"):
                self.replace_morpheme("ive")
            elif self.ends_with("biliti"):
                self.replace_morpheme("ble")
        elif self.word[self.end - 1] == 'g':
            if self.ends_with("logi"):
                self.replace_morpheme("log")

    def step3(self):
        # triplicate --> triplic
        # formative --> form
        # electrical --> electric
        # hopeful --> hope
        # goodness --> good
        if self.word[self.end] == 'e':
            if self.ends_with("icate"):
                self.replace_morpheme("ic")
            elif self.ends_with("ative"):
                self.replace_morpheme("")
            elif self.ends_with("alize"):
                self.replace_morpheme("al")
        elif self.word[self.end] == 'i':
            if self.ends_with("iciti"):
                self.replace_morpheme("ic")
        elif self.word[self.end] == 'l':
            if self.ends_with("ical"):
                self.replace_morpheme("ic")
            elif self.ends_with("ful"):
                self.replace_morpheme("")
        elif self.word[self.end] == 's':
            if self.ends_with("ness"):
                self.replace_morpheme("")

    def step4(self):
        # revival --> reviv
        # allowance --> allow
        # inference --> infer
        # defensible --> defens
        if self.word[self.end - 1] == 'a':
            if self.ends_with("al"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'c':
            if self.ends_with("ance"):
                self.replace_morpheme("")
            elif self.ends_with("ence"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'e':
            if self.ends_with("er"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'i':
            if self.ends_with("ic"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'l':
            if self.ends_with("able"):
                self.replace_morpheme("")
            elif self.ends_with("ible"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'n':
            if self.ends_with("ant"):
                self.replace_morpheme("")
            elif self.ends_with("ement"):
                self.replace_morpheme("")
            elif self.ends_with("ment"):
                self.replace_morpheme("")
            elif self.ends_with("ent"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'o':
            if self.ends_with("ion") and (self.word[self.offset] == 's' or self.word[self.offset] == 't'):
                self.replace_morpheme("")
            elif self.ends_with("ou"):
                self.replace_morpheme("")
            # takes care of -ous
            else:
                return
        elif self.word[self.end - 1] == 's':
            if self.ends_with("ism"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 't':
            if self.ends_with("ate"):
                self.replace_morpheme("")
            elif self.ends_with("iti"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'u':
            if self.ends_with("ous"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'v':
            if self.ends_with("ive"):
                self.replace_morpheme("")
            else:
                return
        elif self.word[self.end - 1] == 'z':
            if self.ends_with("ize"):
                self.replace_morpheme("")
            else:
                return
        else:
            return
        if self.m() > 1:
            self.end = self.offset

    def step5(self):
        self.offset = self.end
        if self.word[self.end] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.is_of_form_cvc(self.end - 1)):
                self.end = self.end - 1
        if self.word[self.end] == 'l' and self.contains_double_consonant(self.end) and self.m() > 1:
            self.end = self.end - 1

    def stem_document(self, document):
        result = []
        for line in document.split('\n'):
            result.append(self.stem_sentence(line))
        return '\n'.join(result)

    def alphabetic(self, word):
        return ''.join([letter if letter.isalpha() else '' for letter in word])

    def stem_sentence(self, sentence):
        result = []
        for word in sentence.split():
            result.append(self.stem_word(word))
        return ' '.join(result)

    def stem_word(self, word):
        if word == '':
            return ''

        self.word = word
        self.end = len(word) - 1
        self.start = 0

        self.remove_plurals()
        self.terminal_y_to_i()
        self.map_double_to_single_suffix()
        self.step3()
        self.step4()
        self.step5()
        return self.word[self.start: self.end + 1]

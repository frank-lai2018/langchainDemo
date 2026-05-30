class MySequence(object):
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self, value):
        print('Adding {} to sequence'.format(value))
        self.sequence.append(value)
        return self
    def __str__(self):
        return str(self.sequence)
    def run(self):
        for item in self.sequence:
            print(item)

class Test(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return '666_'+self.name
    def __or__(self, value):
        #因為a|b，所以a會呼叫__or__，而a是Test物件，所以value就是b，然後回傳MySequence物件，裡面有a和b兩個元素，所以該處的self就是調用者本身，也就是a，value就是b，所以MySequence裡面就有a和b兩個元素，然後回傳MySequence物件，接著再對MySequence物件呼叫__or__，所以MySequence物件的__or__會被呼叫，而value就是c，所以MySequence裡面就有a、b、c三個元素，最後回傳MySequence物件
        return MySequence(self, value)

if __name__ == '__main__':
    a = Test('a')
    b = Test('b')
    c = Test('c')
    res = a | b | c
    res.run()
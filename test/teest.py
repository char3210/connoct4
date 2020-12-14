class Teest:
    a = 1
    def __init__(self, aaa):
        self.a = aaa

    def ree(self):
        self.a *= 5

asdf = Teest(332)
print(asdf.a)
asdf.ree()
print(asdf.a)

print(Teest.a)
Teest.ree(Teest)
print(Teest.a)
print(asdf.a)

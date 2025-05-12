class A():
    @staticmethod
    def bbb():
        print("bbb")

A.bbb()
A().bbb()

###########################

try:
    raise ValueError("aa")
except Exception as error:
    print(type(error))

print("bbbb")
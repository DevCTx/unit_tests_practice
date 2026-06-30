
class base_API():

    def get_data(self):
        return 'data1'

class second_API(base_API):
    pass

class third_API(base_API):
    pass

if __name__ == "__main__":
    print( second_API().get_data() )
    print( third_API().get_data() )




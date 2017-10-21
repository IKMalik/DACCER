'''

only works with character passwords
password is alphabetically sorted and saved with value defining its position
example

password = bob
saved as = b0b2o1


'''


class Mergesort:
    def __init__(self):
        self.password = []    # Stores user password as list for manipulation
        self.numbered_data = []  # stores position of each element in original user password
        self.alphabet_vale = []   # stores value of each letter in English alphabet for use in encryption
        self.value_data = []   # stores the user password with alphabet values instead of positional values
        self.sorted_data = []  # stores sorted password
        self.encrypted_data = ''

        self.setup_alphabet()

    def setup_alphabet(self):
        import string as string
        count = 0
        for each in string.ascii_lowercase:
            self.alphabet_vale.append([each, count])
            count += 1

    def encrypt_data(self, password):
        self.password = list(password)
        self.setup_data()
        self.sorted_data = self.run_mergesort(self.value_data)
        self.encrypted_data = self.encryped_pass()

        return self.encrypted_data

    def setup_data(self):
        count = 0
        for letter in self.password:
            self.numbered_data.append([letter, count])  # positonal values saved for unecryped password
            count += 1
        self.setup_value()

    def setup_value(self):
        for each in self.password:
            for letter in self.alphabet_vale:
                if each == letter[0]:
                    self.value_data.append(letter[1])
                    break

    def run_mergesort(self, data):
        if len(data) <= 1:      # if less than or equal to 1 then sorted .. ie .. sort 'a' .. = .. 'a' so stop here
            return data
        midpoint = len(data) // 2    # working out where to split password
        first_half = self.run_mergesort(data[:midpoint])  # from oth element to midpoint
        second_half = self.run_mergesort(data[midpoint:]) # from midpoint to end
        return(self.merge(first_half, second_half))  # return sorted list

    def merge(self, firsthalf, secondhalf):
        pos1 = 0
        pos2 = 0
        sorted_list = []
        while pos1 < len(firsthalf) and pos2 < len(secondhalf):
            if firsthalf[pos1] <= secondhalf[pos2]:
                sorted_list.append(firsthalf[pos1])
                pos1 += 1
            else:
                sorted_list.append(secondhalf[pos2])
                pos2 += 1
        sorted_list += firsthalf[pos1:]
        sorted_list += secondhalf[pos2:]
        return sorted_list

    def encryped_pass(self):
        for val in self.sorted_data:
            for letter in self.alphabet_vale:
                if val == letter[1]:
                    for pos in self.numbered_data:
                        if letter[0] == pos[0]:
                            self.numbered_data.remove(pos)
                            self.encrypted_data = self.encrypted_data + '{}'.format(letter[0] + '{}'.format(pos[1]))
        return self.encrypted_data

    def decrypt_data(self , password):  # data comes in as tuple
        for word in password: # remove data from tuple
            password = word # password is now itself but without tuple
        temp_storage = {}
        data = list(password)  # create list of password
        midpoint = len(data)//2  # Midpoint of password

        if midpoint <= 10:  # ie max value number is 9 , single value numbers e.g f0 to i9 [max password size 10]
            charcount = 0  # counter for letter
            poscount = charcount+1  # counter for number

            while poscount <= len(data):  # While not every element checked
                char = data[charcount]  # letter is the position of pointer in data
                pos = int(data[poscount])  # position of letter acessed via its pointer in data
                temp_storage[pos] = char  # store the character in postion given in data
                charcount +=2 # incriment by 2 for next letter
                poscount+=2 # incriment by 2 for next number

            return self.decrypted_key(temp_storage)  # pass dictionary of password to function to create string of
                                                     # password and return it

        else:  # double value numbers e.g c12 [password size >10]
            import string as string  # importing string libaray
            count = 0  # three counters used
            count1 = count + 1
            count2 = count + 2

            checks = []  # list to hold positonal values 0-9 (singl value pairs)
            for val in range(0,10):
                checks.append(str(val))

            while len(data) != 0:  # while not every element checked
                if data[count] in string.ascii_lowercase:  # if letter
                    if len(data) >= 3:  # to prevent index error these checks only occur when 3 + items exist ,
                                        # ie when there is a possibility of two digigt number existing
                        if (data[count1] in checks) and (data[count2] in checks):  # if double number pair e.g d12
                            temp_storage[int(data[count1] + data[count2])] = data[count]
                            data.remove(data[count2])
                        elif data[count1] in checks:
                            temp_storage[int(data[count1])] = data[count]

                    elif data[count1] in checks:
                        temp_storage[int(data[count1])] = data[count]
                    data.remove(data[count1])
                    data.remove(data[count])

            decrypted_password = self.decrypted_key(temp_storage)
            return decrypted_password

    def decrypted_key(self, dict):
        import sys as sy
        decryped_key = ''  # holds string of decrypted key

        while len(dict) != 0:  # while not every element checked
            smallest = sy.maxsize  # set default smallest value to largest value available
            for pos in dict.keys():  # for position (numerical position of data)
                if pos < smallest:  # if it is smaller than current smallest
                    smallest = pos  # smallest now becomes it
            decryped_key = decryped_key + '{}'.format(dict[smallest]) # write the element with smallest value into key
            del dict[smallest]  # delete that smallest element from dictionary
        return decryped_key # when completed , return key


'''
if __name__ == '__main__':
    x = Mergesort()
    c = x.encrypt_data('ibrahim')
    #b = x.decrypt_data(('a0a10d16e2g8l5n7o6o14p9r3r15s11s12v1w13y4',))
'''



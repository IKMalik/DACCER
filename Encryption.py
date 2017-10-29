import string as string

class Encryption:
    def __init__(self):
        self.password = []    # Stores user password as list for manipulation
        self.numbered_data = []  # stores position of each element in original user password
        self.alphabet_vale = []   # stores value of each letter in English alphabet for use in encryption
        self.value_data = []   # stores the user password with alphabet values instead of positional values
        self.sorted_data = []  # stores sorted password
        self.encrypted_data = '' # string to store encryped data

        self.setup_alphabet()

    def setup_alphabet(self):  # Method to assign value to letters e.g a=1 b=2 etc
        count = 0
        for each in string.ascii_letters:
            self.alphabet_vale.append([each, count])
            count += 1

    def encrypt_data(self, password):  # Method where data encrypted
        self.password = list(password)  # create list of user entered password
        isvalid = self.validate_pass()  # check if a valid password was given
        if isvalid == False:
            return isvalid
        else: # valid password
            self.setup_data()  # setup the positional values for unecrypted data
            self.sorted_data = self.run_mergesort(self.value_data)  # sort data using mergesort and poitional values
            self.encrypted_data = self.encryped_pass() # encrypt data and return it
            return self.encrypted_data

    def validate_pass(self): # Method to check to ensure each char is valid
        for char in self.password:
            if char not in string.ascii_letters:
                return False

    def setup_data(self):  # Method to create initial positional values
        count = 0  # counters use to assign value
        for letter in self.password:
            self.numbered_data.append([letter, count])  # positional values saved for unecryped password
            count += 1
        self.setup_value() # set up alphabet values for each letter

    def setup_value(self): # asigns alphabet values from setup_alphabet
        for each in self.password:
            for letter in self.alphabet_vale:
                if each == letter[0]:
                    self.value_data.append(letter[1])
                    break

    def run_mergesort(self, data):  # Method to order password using mergesort
        if len(data) <= 1:      # if less than or equal to 1 then sorted .. ie .. sort 'a' .. = .. 'a' so stop here
            return data  # return data to first half/ second half
        midpoint = len(data) // 2    # working out where to split password, changes until 1 is reached as mp then merge run
        first_half = self.run_mergesort(data[:midpoint])  # from midpoint to start
        second_half = self.run_mergesort(data[midpoint:]) # from midpoint to end
        return(self.merge(first_half, second_half))  # return sorted list

    def merge(self, firsthalf, secondhalf):  # Method that carries out merge
        pos1 = 0  # counters
        pos2 = 0
        sorted_list = [] # list of sorted data
        while pos1 < len(firsthalf) and pos2 < len(secondhalf):  # while counters are less than length each half
            if firsthalf[pos1] <= secondhalf[pos2]:
                # if element in left half smaller than one on right
                sorted_list.append(firsthalf[pos1])  # add smaller one to sorted list
                pos1 += 1 # move counter on left half to next number
            else:
                sorted_list.append(secondhalf[pos2])  # else the element in second half was smaller
                pos2 += 1 # so increment its counter
        sorted_list += firsthalf[pos1:]  # after sorting add to sorted list elements from pos1 value in first half to end
        sorted_list += secondhalf[pos2:] # after sorting add to sorted list elements from pos2 value in second half to end
        return sorted_list # return sorted list

    def encryped_pass(self):  # Method to assign values to sorted data to create key
        for val in self.sorted_data:  # each char in sorted unencrypted password
            for letter in self.alphabet_vale:  # for letter in alphabet value
                if val == letter[1]: # if same letter
                    for pos in self.numbered_data: # find original position in numbered data
                        if letter[0] == pos[0]:  # if same
                            self.numbered_data.remove(pos)  # remove from numbered data
                            self.encrypted_data = self.encrypted_data + '{}'.format(letter[0] + '{}'.format(pos[1]))
                            # add to encrypted data
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
                if data[count] in string.ascii_letters:  # if letter
                    if len(data) >= 3:  # to prevent index error these checks only occur when 3 + items exist ,
                                        # ie when there is a possibility of two digigt number existing
                        if (data[count1] in checks) and (data[count2] in checks):  # if double number pair e.g d12
                            temp_storage[int(data[count1] + data[count2])] = data[count]
                            data.remove(data[count2])
                        elif data[count1] in checks:
                            temp_storage[int(data[count1])] = data[count]

                    elif data[count1] in checks:  # if single value pairs
                        temp_storage[int(data[count1])] = data[count]
                    data.remove(data[count1])
                    data.remove(data[count])

            return self.decrypted_key(temp_storage)

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

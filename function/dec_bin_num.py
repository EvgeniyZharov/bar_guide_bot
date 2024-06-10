from config import interests


c = {"0": "000",
     "1": "001",
     "2": "010",
     "3": "011",
     "4": "100",
     "5": "101",
     "6": "110",
     "7": "111"}


def match_status(a, b, n_1=2, n_2=6):
    new_a = ""
    new_b = ""
    while len(a) < n_1:
        a = "0" + a
    for ii in range(n_1):
        new_a += '{0:03b}'.format(int(a[ii]))
        new_b += '{0:03b}'.format(int(b[ii]))
    for jj in range(n_2):
        if new_a[jj] == new_b[jj] == "1":
            return True
    return False


def interest_to_bin(a, n_1=6, n_2=3):
    result = ""
    res = ""
    for elem in interests:
        if elem in a:
            res += "1"
        else:
            res += "0"
    for ii in range(n_1//n_2):
        result += str(int(res[ii*3:ii*3 + 3], 2))
    return result


def bin_to_interest(a, n_1=2, n_2=6):
    new_a = ""
    new_interests = list()
    for ii in range(n_1):
        new_a += '{0:03b}'.format(int(a[ii]))
    for jj in range(n_2):
        if new_a[jj] == "1":
            new_interests.append(interests[jj])
    return new_interests


def match_interests(a, b, n_1=2, n_2=6, n_3=2):
    new_a = ""
    new_b = ""
    counter = 0
    for ii in range(n_1):
        new_a += '{0:03b}'.format(int(a[ii]))
        new_b += '{0:03b}'.format(int(b[ii]))
    for jj in range(n_2):
        if new_a[jj] == new_b[jj] == "1":
            counter += 1
            if counter == n_3:
                return True
    return False


# print(int("111", 2))
a = ["Музыка", "Фитнес", 'Рестораны']
print(interest_to_bin(a))
print(bin_to_interest("25"))
print(interests)

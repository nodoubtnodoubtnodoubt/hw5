from copy import copy
import json
import sys


class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = copy(hash_map)
        self.wheels = copy(wheels)
        self.reflector_map = copy(reflector_map)

    def encrypt(self, message):

        wheelsTempSave = copy(self.wheels)
        letterAlreadyEncrypted = 0;
        newMessage = ""
        for elem in message:
            newLetter = self.encryptByletter(elem, letterAlreadyEncrypted)
            if (newLetter != elem):
                letterAlreadyEncrypted += 1
            newMessage += newLetter
            self.wheelsGoUp(letterAlreadyEncrypted)
        self.wheels = wheelsTempSave
        return newMessage

    def wheelsGoUp(self, letterAlreadyEncrypted):
        TEN = 10
        THREE = 3
        FIVE = 5
        W_TWO = 1
        W_THREE = 2
        TWO = 2
        MAX_W1_SIZE = 8
        if self.wheels[0] == MAX_W1_SIZE:
            self.wheels[0] = 1
        else:
            self.wheels[0] += 1
        if letterAlreadyEncrypted % TWO == 0:
            self.wheels[W_TWO] *= TWO
        else:
            self.wheels[W_TWO] -= 1
        if letterAlreadyEncrypted % TEN == 0:
            self.wheels[W_THREE] = TEN
        elif letterAlreadyEncrypted % THREE == 0:
            self.wheels[W_THREE] = FIVE
        else:
            self.wheels[W_THREE] = 0

    def encryptByletter(self, letter, letterAlreadyEncrypted):
        MODOLO_NUMBER = 26
        if letter in self.hash_map:
            i = self.hash_map.get(letter, None)
        else:
            return letter
        number = (2 * self.wheels[0] - self.wheels[1] + self.wheels[2]) % 26
        if number != 0:
            i += number
        else:
            i += 1
        i = i % MODOLO_NUMBER
        if i in self.hash_map:
            c1 = self.hash_map.get(i, None)
        else:
            return letter
        if c1 in self.reflector_map:
            c2 = self.reflector_map.get(c1, None)
        else:
            return letter
        if c2 in self.hash_map:
            i = self.hash_map.get(c2, None)
        else:
            return letter
        if number != 0:
            i -= number
        else:
            i -= 1
        i = i % MODOLO_NUMBER
        if i in self.hash_map:
            c3 = self.hash_map.get(i, None)
        else:
            return letter
        return c3


class JSONFileError(Exception):
    def __init__(self, message):
        super().__init__(message)


def load_enigma_from_path(path):
    try:
        with open(path, 'r') as f:
            load_dict = json.load(f)
            
            return Enigma(load_dict.get("hash_map"), load_dict.get("wheels"),
                          load_dict.get("reflector_map"))
    except  Exception:
        raise JSONFileError("couldnt open file")


def main():
    MAX_ARGV = 7
    MIN_ARGV = 5

    if len(sys.argv) < MIN_ARGV or len(sys.argv) > MAX_ARGV:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file> ", file=sys.stderr)
        sys.exit(1)

    config_file = None
    input_file = None
    output_file = None

    for i in range(1, len(sys.argv), 2):
        key = sys.argv[i]
        value = sys.argv[i + 1]
        if key == "-c":
            config_file = value
        elif key == "-i":
            input_file = value
        elif key == "-o":
            output_file = value
        else:
            print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file> ", file=sys.stderr)
            sys.exit(1)

    if not config_file or not input_file:
        print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file> ", file=sys.stderr)
        sys.exit(1)

    try:
        enigma = load_enigma_from_path(config_file)
        with open(input_file, 'r') as f:
            message = f.read()
            encrypted_message = enigma.encrypt(message)
        if output_file:
            with open(output_file, 'w') as output:
                output.write(encrypted_message)
        else:
            print(encrypted_message)
    except JSONFileError as e:
        print(f"The enigma script has encountered an error: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"An I/O error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
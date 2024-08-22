from copy import copy
import json
import sys


class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = copy(hash_map)
        self.wheels = copy(wheels)
        self.reflector_map = copy(reflector_map)

    def encrypt(self, message):

        wheels_temp_save = copy(self.wheels)
        letter_already_encrypted = 0
        new_message = ""
        for elem in message:
            new_letter = self.encryptByletter(elem)
            if new_letter != elem:
                letter_already_encrypted += 1
            new_message += new_letter
            self.wheelsGoUp(letter_already_encrypted)
        self.wheels = wheels_temp_save
        return new_message

    def wheelsGoUp(self, letter_already_encrypted):
        TEN = 10
        THREE = 3
        FIVE = 5
        WTWO = 1
        WTHREE = 2
        TWO = 2

        new_wheels=copy(self.wheels)
        MAXW1SIZE = 8
        if self.wheels[0] >= MAXW1SIZE:
            new_wheels[0] = 1
        else:
            self.wheels[0] += 1
        if letter_already_encrypted % TWO == 0:
            new_wheels[WTWO] *= TWO
        else:
            new_wheels[WTWO] -= 1
        if letter_already_encrypted % TEN == 0:
            new_wheels[WTHREE] = TEN
        elif letter_already_encrypted % THREE == 0:
            new_wheels[WTHREE] = FIVE
        else:
            new_wheels[WTHREE] = 0
        self.wheels=new_wheels

    def encryptByletter(self, letter):
        MODOLO_NUMBER = 26
        i = self.hash_map.get(letter)
        if i is None:
            return letter

        number = ((2 * self.wheels[0]) - self.wheels[1] + self.wheels[2]) % 26
        if number != 0:
            i += number
        else:
            i += 1
        i = i % MODOLO_NUMBER
        c1 = self.hash_map.get(i)
        if c1 is None:
            return letter
        c2 = self.reflector_map.get(c1)
        if c2 is None:
            return letter
        i = self.hash_map.get(c2)
        if i is None:
            return letter
        if number != 0:
            i =i- number
        else:
            i =i- 1
        i = i % MODOLO_NUMBER
        c3 = self.hash_map.get(i)
        if c3 is None:
            return letter
        else:
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
    except (json.JSONDecodeError, IOError) as e:
        raise JSONFileError(f"Error loading JSON file: {e}")


def main():
    MAXARGV = 7
    MINARGV = 5

    if len(sys.argv) < MINARGV or len(sys.argv) > MAXARGV:
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
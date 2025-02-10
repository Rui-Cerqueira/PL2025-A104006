def word_scanner(text: str):
    reading_on = 0
    conta_final = 0

    i = 0
    while i < len(text):
        if text[i].lower() == 'o':
            if i + 1 < len(text) and text[i+1].lower() == 'n':
                reading_on = 1
                i += 2
            elif i + 2 < len(text) and text[i+1].lower() == 'f' and text[i+2].lower() == 'f':
                reading_on = 0
                i += 3
            else:
                i += 1
                continue
        else:
            i += 1
            continue

        while reading_on == 1 and i < len(text):
            if text[i].isdigit():
                conta_final += int(text[i])
                i += 1
            elif text[i] == '=':
                return conta_final
            else:
                break

    return conta_final

def main():
    test_strings = [
        "on123off=",
        "on1off2on3off=",
        "on12off34on56off=",
        "on1on2off3off=",
        "on123=",
        "off123on456=",
        "asdgaudyadsuygOn123afyafyoff asdasdon123=asdasd"
    ]

    for test in test_strings:
        result = word_scanner(test)
        print(f"Input: {test} -> Output: {result}")

if __name__ == "__main__":
    main()
class utils:

    @staticmethod
    def remove_trailing_spaces(st: str) -> str:
        initial_val = st
        if st[-1] == " ":
            return utils.remove_trailing_spaces(st[:-1])
        if st[0] == " ":
            return utils.remove_trailing_spaces(st[1:])
        if len(st) == 0:
            raise ValueError(f"Something is wrong with either the function of the input: initial value is ({initial_val})")
        return st

# print(utils.remove_trailing_spaces("12 1234 14 4") == "12 1234 14 4")
# print(utils.remove_trailing_spaces("12 1234 14 ") == "12 1234 14")
# print(utils.remove_trailing_spaces("   1234 14 4") == "1234 14 4")
# print(utils.remove_trailing_spaces(" 12 1234       ") == "12 1234")
# print(utils.remove_trailing_spaces(" אילנית") == "אילנית")

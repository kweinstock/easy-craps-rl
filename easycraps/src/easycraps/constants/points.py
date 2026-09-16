"""Point numbers and Place bet payouts."""

POINT_NUMBERS = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]

POINT_LABEL = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "SIX",
    8: "8", 9: "NINE", 10: "10", 11: "11", 12: "12",
}

# number -> (a, b) meaning the number pays (a-b):b, i.e. a/b is the total
# return multiplier (win + stake) on a winning bet.
PLACE_PAY = {
    2: (13, 2), 3: (15, 4), 4: (14, 5), 5: (12, 5), 6: (13, 6),
    8: (13, 6), 9: (12, 5), 10: (14, 5), 11: (15, 4), 12: (13, 2),
}


def place_return_multiplier(number: int) -> float:
    a, b = PLACE_PAY[number]
    return a / b

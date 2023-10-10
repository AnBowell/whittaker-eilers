from whittaker_eilers import WhittakerSmoother

# whittaker_eilers.guess_the_number()
x = WhittakerSmoother(2e4, 2, 2, [1.0, 2.0], [1.0, 1.0])


print(x.get_order())

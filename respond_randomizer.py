from random import randint
evil_responses = [
  "image268568.jpg",
  "social-credit.gif"
]

happy_zarif_responses = [
  "plus15sc.png",
  "image_2_4.jpg"
]

def evil_randomizer():
  return evil_responses[randint(0, len(evil_responses) - 1)]

def happy_zarif_randomizer():
  return happy_zarif_responses[randint(0, len(happy_zarif_responses) - 1)]

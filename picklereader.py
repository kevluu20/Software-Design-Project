import pickle


host = "meeting3"
with open(f"events/{host}.pickle", "rb") as f:
    output = pickle.load(f)
print(output)

person = "Prof"
with open(f"schedule/{person}{host}.pickle", "rb") as f:
    output2 = pickle.load(f)
print(output2)
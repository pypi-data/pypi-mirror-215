import NeuroGraph as ng

print(ng)
root = "NeuroGraph/data/"
name ="HCPGender"

dataset = ng.NeuroGraphStatic(root, name)
print(len(dataset))

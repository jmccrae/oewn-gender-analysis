import yaml

data = yaml.safe_load(open('gendered_changes.yaml'))

male = 0
female = 0
both = 0

male_link = False
female_link = False
last_link = ""

for change in data:
    if ("add_relation" in change and change["add_relation"]["source"] == "last"
        and change["add_relation"]["target"] == "10807146-n"):
        female_link = True
    elif ("add_relation" in change and change["add_relation"]["source"] == "last"
        and change["add_relation"]["target"] == "10306910-n"):
        male_link = True
    elif ("add_relation" in change and change["add_relation"]["source"] == "last"):
        if last_link != change["add_relation"]["target"]:
            if male_link and female_link:
                both += 1
            elif male_link:
                male += 1
            elif female_link:
                female += 1
            male_link = False
            female_link = False
            last_link = change["add_relation"]["target"]

if male_link and female_link:
    both += 1
elif male_link:
    male += 1
elif female_link:
    female += 1

print("Male changes: ", male)
print("Female changes: ", female)
print("Both changes: ", both)


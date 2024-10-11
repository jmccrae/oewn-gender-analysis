import csv
import wn

wn1 = wn.Wordnet("oewn:2023")
wn2 = wn.Wordnet("oewn:2024-10-03")

female = [synset for synset in wn1.synsets("female") if "person" in synset.definition()][0]
male = [synset for synset in wn1.synsets("male") if "person" in synset.definition()][0]
print(female)
print(male)

def all_children(synset):
    children = synset.hyponyms()
    for child in children:
        children.extend(all_children(child))
    return children

male_synsets1 = [synset.id for synset in all_children(male)]
female_synsets1 = [synset.id for synset in all_children(female)]


female = [synset for synset in wn2.synsets("female") if "person" in synset.definition()][0]
male = [synset for synset in wn2.synsets("male") if "person" in synset.definition()][0]
print(female)
print(male)

def all_children(synset):
    children = synset.hyponyms()
    for child in children:
        children.extend(all_children(child))
    return children

male_synsets2 = [synset.id for synset in all_children(male)]
female_synsets2 = [synset.id for synset in all_children(female)]

print(len(set(male_synsets1)))
print(len(set(male_synsets2)))

with open("now_ungendered.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Synset ID", "Lemmas", "Definition", "F/M", "Change"])
    for ssid in set(male_synsets1).union(male_synsets2):
        try:
            synset = wn1.synset(ssid)
        except wn.Error:
            continue
        try:
            synset2 = wn2.synset(ssid)
        except wn.Error:
            continue
        if ssid in male_synsets1 and ssid not in male_synsets2:
            writer.writerow([ssid, ", ".join(synset.lemmas()), synset.definition(), "M", ""])
    for ssid in set(female_synsets1).union(female_synsets2):
        try:
            synset = wn1.synset(ssid)
        except wn.Error:
            continue
        try:
            synset2 = wn2.synset(ssid)
        except wn.Error:
            continue
        if ssid in female_synsets1 and ssid not in female_synsets2:
            writer.writerow([ssid, ", ".join(synset.lemmas()), synset.definition(), "F", ""])


import wn
import csv
from collections import defaultdict

oewn = wn.Wordnet("oewn:2024-25-09")

male_synsets = defaultdict(set)
female_synsets = defaultdict(set)

with open("gendered_words_annotated.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        ssid = row[0]
        if row[3] == "M" and row[4] == "TRUE":
            male_synsets[ssid].add(row[1])
        if row[3] == "F" and row[4] == "TRUE":
            female_synsets[ssid].add(row[1])


with open("gendered_words_male.csv", "w") as fm:
    male_out = csv.writer(fm)
    male_out.writerow(["Synset ID", "Lemmas", "Definition",
                       "New Definution",
                       "Man", "Boy", "Hypernym", 
                       "Hypo Definition", "Hypo Lemmas",
                       "Alt Definition", "Alt Lemmas"])
    for ssid, lemmas in male_synsets.items():
        synset = oewn.synset(ssid)
        male_out.writerow([ssid, ", ".join(synset.lemmas()),
                           synset.definition(), "",
                           "", "", "",
                           "", "",
                           "", ""])
        

with open("gendered_words_female.csv", "w") as ff:
    female_out = csv.writer(ff)
    female_out.writerow(["Synset ID", "Lemmas", "Definition",
                         "New Definition",
                       "Woman", "Girl", "Hypernym",
                       "Hypo Definition", "Hypo Lemmas",
                       "Alt Definition", "Alt Lemmas"])
    for ssid, lemmas in female_synsets.items():
        synset = oewn.synset(ssid)
        female_out.writerow([ssid, ", ".join(synset.lemmas()),
                           synset.definition(),
                             "",
                           "", "", "",
                           "", "",
                           "", ""])
        



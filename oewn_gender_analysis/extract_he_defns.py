import wn
import re
import csv

oewn = wn.Wordnet('oewn:2024')

with open("he_words.csv", "w") as f:
    with open("she_words.csv", "w") as f2:
        out = csv.writer(f)
        out2 = csv.writer(f2)
        for synset in oewn.synsets():
            definition = synset.definition()
            ssid = synset.id
            for word in re.split(r"\b", definition.lower().strip()):
                if word == "he" or word == "him" or word == "himself" or word == "his":
                    out.writerow([ssid, ", ".join(synset.lemmas()), definition])
                    break
                elif word == "she" or word == "her" or word == "herself" or word == "hers":
                    out2.writerow([ssid, ", ".join(synset.lemmas()), definition])
                    break


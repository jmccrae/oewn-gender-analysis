import csv
import yaml
import re

processed = set()

ewe_changes = []

checked_changes = {}

reader = csv.reader(open("pronoun_changes_checked.csv"))
next(reader)
for row in reader:
    ssid, def_old, definition, checked_definition = row
    if checked_definition:
        checked_changes[ssid] = checked_definition

with open("pronoun_changes.csv", "w") as f:
    writer = csv.writer(f)

    reader = csv.reader(open("he_pronouns.csv"))
    next(reader)
    for row in reader:
        ssid, members, definition, appropriate, unbiased, biased, incidental = row[:7]
        if not ssid:
            continue
        if biased == "FALSE":
            continue
        def_old = definition
        definition = re.sub("he or she", "they", definition)
        definition = re.sub("she or he", "they", definition)
        definition = re.sub(r"he \(or she\)", "they", definition)
        definition = re.sub(r"she \(or he\)", "they", definition)
        definition = re.sub("he/she", "they", definition)
        definition = re.sub("she/he", "they", definition)
        definition = re.sub(r"\(s\)he", "they", definition)
        definition = re.sub(r"\bhe\b", "they", definition)
        definition = re.sub("him or her", "them", definition)
        definition = re.sub("her or him", "them", definition)
        definition = re.sub("him/her", "them", definition)
        definition = re.sub(r"him \(or her\)", "them", definition)
        definition = re.sub(r"her \(or him\)", "them", definition)
        definition = re.sub(r"\bhim\b", "them", definition)
        definition = re.sub("his or her", "their", definition)
        definition = re.sub("her or his", "their", definition)
        definition = re.sub("his/her", "their", definition)
        definition = re.sub(r"his \(or her\)", "their", definition)
        definition = re.sub(r"her \(or his\)", "their", definition)
        definition = re.sub(r"\bhis\b", "their", definition)
        definition = re.sub("himself or herself", "themself", definition)
        definition = re.sub("herself or himself", "themself", definition)
        definition = re.sub("himself/herself", "themself", definition)
        definition = re.sub(r"himself \(or herself\)", "themself", definition)
        definition = re.sub(r"herself \(or himself\)", "themself", definition)
        definition = re.sub("himself", "themself", definition)
        if ssid in checked_changes:
            definition = checked_changes[ssid]
        if def_old == definition:
            print(f"No change to definition for {ssid}: {definition}")
        writer.writerow([ssid, def_old, definition])
        ewe_changes.append({"change_definition": {"synset": ssid, "definition": definition}})

    reader = csv.reader(open("she_pronouns.csv"))
    next(reader)
    for row in reader:
        ssid, members, definition, appropriate, unbiased, biased, incidental = row[:7]
        def_old = definition
        if not ssid:
            continue
        if biased == "FALSE":
            continue
        definition = re.sub("he or she", "they", definition)
        definition = re.sub("she or he", "they", definition)
        definition = re.sub(r"he \(or she\)", "they", definition)
        definition = re.sub(r"she \(or he\)", "they", definition)
        definition = re.sub("he/she", "they", definition)
        definition = re.sub("she/he", "they", definition)
        definition = re.sub(r"\(s\)he", "they", definition)
        definition = re.sub(r"\bshe\b", "they", definition)
        definition = re.sub("him or her", "them", definition)
        definition = re.sub("her or him", "them", definition)
        definition = re.sub("him/her", "them", definition)
        definition = re.sub(r"him \(or her\)", "them", definition)
        definition = re.sub(r"her \(or him\)", "them", definition)
        definition = re.sub(r"\bhers\b", "theirs", definition)
        definition = re.sub("his or her", "their", definition)
        definition = re.sub("her or his", "their", definition)
        definition = re.sub("his/her", "their", definition)
        definition = re.sub(r"his \(or her\)", "their", definition)
        definition = re.sub(r"her \(or his\)", "their", definition)
        definition = re.sub(r"\bher\b", "their", definition)
        definition = re.sub("himself or herself", "themself", definition)
        definition = re.sub("herself or himself", "themself", definition)
        definition = re.sub("himself/herself", "themself", definition)
        definition = re.sub(r"himself \(or herself\)", "themself", definition)
        definition = re.sub(r"herself \(or himself\)", "themself", definition)
        definition = re.sub("herself", "themself", definition)
        if def_old == definition:
            print(f"No change to definition for {ssid}: {definition}")
        if ssid in checked_changes:
            definition = checked_changes[ssid]
        writer.writerow([ssid, def_old, definition])
        ewe_changes.append({"change_definition": {"synset": ssid[5:], "definition": definition}})


ewe_changes.append(
    {
        "change_definition": {
            "synset": "04812863-n",
            "definition": "belief of the Roman Catholic Church that God protects the pope from error when the pope speaks about faith or morality"
        }
    })

ewe_changes.append(
        {
            "change_definition": {
                "synset": "10049710-n",
                "definition": "British soldier; so-called because of the soldier's red coat (especially during the American Revolution)"
            }
        })

with open("pronoun_changes.yaml", "w") as outp:
    yaml.dump(ewe_changes, outp)


import yaml
import csv
import wn

oewn = wn.Wordnet("oewn:2023")

ewe_changes = []

def process_row(row, woman_ssid, girl_ssid, man_ssid, boy_ssid):
    (ssid, members, definition, new_definition, woman, girl, hyper, hypo_def, 
    hypo_members, alt_def, alt_members, gen_members) = row[:12]
    if not ssid:
        return
    ssid = ssid[5:]
    members = set(members.split(", "))
    if new_definition.strip():
        ewe_changes.append({"change_definition": {"synset": ssid, 
                                                  "definition": new_definition}})
    if woman == "TRUE":
        ewe_changes.append({"add_relation": {"source": ssid, "relation": 
                                             "hypernym", "target":  woman_ssid}})
    if girl == "TRUE":
        ewe_changes.append({"add_relation": {"source": ssid, "relation": 
                                             "hypernym", "target": girl_ssid}})
    if hyper:
        ewe_changes.append({"add_relation": {"source": ssid, "relation": 
                                             "hypernym", "target": hyper}})

    has_generic = gen_members or len(hypo_members.split(", ")) != len(members)

    if hypo_def.strip():
        if has_generic:
            # Add a new synset of this gender
            ewe_changes.append({"add_synset": {
                "definition": hypo_def,
                "lexfile": "noun.person",
                "pos": "n",
                "lemmas": [] }})
            ewe_changes.append({"add_relation": {"source": "last", "relation": 
                                                 "hypernym", "target": ssid}})
            ewe_changes.append({"add_relation": {"source": "last", "relation": 
                                                 "hypernym", "target": woman_ssid}})
        else:
            # Gender the existing synset
            ewe_changes.append({"change_definition": {"synset": ssid, 
                                                      "definition": hypo_def}})
            ewe_changes.append({"add_relation": {"source": ssid, "relation": 
                                                 "hypernym", "target": woman_ssid}})

    if hypo_members:
        for member in hypo_members.split(", "):
            if has_generic:
                if member in members:
                    ewe_changes.append({"move_entry": {
                        "synset": ssid,
                        "lemma": member,
                        "target_synset": "last" }})
                else:
                    ewe_changes.append({"add_entry": {
                        "synset": "last",
                        "lemma": member,
                        "pos": "n" }})
    if alt_def:
        ewe_changes.append({"add_synset": {
            "definition": alt_def,
            "lexfile": "noun.person",
            "pos": "n",
            "lemmas": alt_members.split(", ") }})
        if has_generic:
            ewe_changes.append({"add_relation": {"source": "last", "relation": 
                                                 "hypernym", "target": ssid}})
        else:
            for hyp in oewn.synset("oewn-" + ssid).hypernyms():
                ewe_changes.append({"add_relation": {"source": "last", "relation": 
                                                     "hypernym", "target": hyp.id[5:]}})
        if girl == "TRUE":
            ewe_changes.append({"add_relation": {"source": "last", "relation": 
                                                 "hypernym", "target": boy_ssid}})
        else:
            ewe_changes.append({"add_relation": {"source": "last", "relation": 
                                                 "hypernym", "target": man_ssid}})
    if gen_members:
        for member in gen_members.split(", "):
            ewe_changes.append({"add_entry": {
                "synset": ssid,
                "lemma": member.strip(),
                "pos": "n" }})

reader = csv.reader(open("gendered_words_female_annotated.csv"))
next(reader)

for row in reader:
    process_row(row + [''], "10807146-n", "10149362-n", "10306910-n", "10305010-n")

reader = csv.reader(open("gendered_words_male_annotated.csv"))
next(reader)

for row in reader:
    process_row(row, "10306910-n", "10305010-n", "10807146-n", "10149362-n")


ewe_changes.append("fix_transitivity")

with open("gendered_changes.yaml", "w") as outp:
    yaml.dump(ewe_changes, outp)

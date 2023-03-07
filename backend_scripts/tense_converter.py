
import os
import pandas as pd


df = pd.read_csv("data/dict.tsv", header=None, sep="\t")

verbs = df[1].tolist()

# print(verbs)

pt_exc = pd.read_csv("data/past_tense_exceptions.csv")
p_part_exc = pd.read_csv("data/irregular_verbs_past_participle.csv")


def df_to_dict(df):
    return dict(zip(df.iloc[:,0], df.iloc[:,1]))

pt_exc =df_to_dict(pt_exc)
p_part_exc = df_to_dict(p_part_exc)


def to_past(verb, exc):
    if len(verb.split(" ")) > 1:
        return to_past(verb.split(" ")[0], exc) + " " + " ".join(verb.split(" ")[1:])
    if verb.startswith("be "):
        return verb.replace("be ", "was ")
    if verb.startswith("put on"):
        return verb

    if verb in exc:
        return exc[verb]
    if verb.endswith("e"):
        return verb + "d"
    elif verb.endswith("y"):
        return verb[:-1] + "ied"
    elif verb.endswith("d"):
        return verb[:-1] + "t"
    else:
        return verb+"ed"
    
    
def to_future(verb):
    return "will " + verb

def get_past_participle(verb, exc):
    if verb in exc:
        return exc[verb]
    elif verb.endswith("e"):
        return verb + "d"
    elif len(verb) > 2 and verb.endswith("y") and verb[-2] not in "aeiou":
        return verb.replace("y", "ied")
    else:
        return verb+"ed"
    
        
def to_past_perfect(verb, exc):
    if verb.startswith("be "):
        return "had been " + verb[3:]
    elif len(verb.split(" ")) > 1:
        return "had " + get_past_participle(verb.split(" ")[0], exc) + " " + " ".join(verb.split(" ")[1:])
    return "had " + get_past_participle(verb, exc)


# for verb in verbs:
#     past_verb = to_past(verb, pt_exc)
#     print(f"{verb:<20} | {past_verb:<20} | {to_future(verb):<20}| {to_past_perfect(verb, p_part_exc):<20}")
    



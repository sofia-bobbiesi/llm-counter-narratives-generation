import random
from glob import glob


def parse_dataset(filenames, use_extra_info="", language="spanish"):
    # TODO - remove language, use spanish as default
    cns_by_tweet = {}
    nonargs = 0
    cn_length = 0
    cn_type_not_present = 0
    for filename in glob(filenames):
        f = open(filename, "r")
        tweet_list = []
        is_arg = True
        need_collective = use_extra_info == "collective" or use_extra_info == "all" or use_extra_info == "cn_a" or use_extra_info == "cn_b"
        need_premises = use_extra_info == "premises" or use_extra_info == "all" or use_extra_info == "cn_c" or use_extra_info == "cn_a"
        if need_collective:
            collective = []
            consecutive_collective = False
            property = []
            consecutive_property = False
        if need_premises:
            justification = []
            consecutive_just = False
            if need_premises:
                conclusion = []
                consecutive_conc = False
                pivot = []
                consecutive_pivot = False
        prev_line = ["", "", "", "", "", "", "", "", ""]
        for line in f:
            splitted_line = line.split("\t")
            if splitted_line[1].startswith("NoArgumentative"):
                is_arg = False
                break
            if splitted_line[4].startswith("Collective") and need_collective:
                if not prev_line[4].startswith("Collective") and consecutive_collective:
                    collective.append(" - ")
                collective.append(splitted_line[0])
                consecutive_collective = True
            if splitted_line[5].startswith("Property") and need_collective:
                if not prev_line[5].startswith("Property") and consecutive_property:
                    property.append(" - ")
                property.append(splitted_line[0])
                consecutive_property = True
            if splitted_line[2].startswith("Premise2Justification") and need_premises:
                if not prev_line[2].startswith("Premise2Justification") and consecutive_just:
                    justification.append(" - ")
                justification.append(splitted_line[0])
                consecutive_just = True
            if splitted_line[3].startswith("Premise1Conclusion") and need_premises:
                if not prev_line[3].startswith("Premise1Conclusion") and consecutive_conc:
                    conclusion.append(" - ")
                conclusion.append(splitted_line[0])
                consecutive_conc = True
            if splitted_line[6].startswith("pivot") and need_premises:
                if not prev_line[6].startswith("pivot") and consecutive_pivot:
                    pivot.append(" - ")
                pivot.append(splitted_line[0])
                consecutive_pivot = True
            if (not splitted_line[7].startswith("O")) and need_premises:
                type_just = splitted_line[7].strip()
            if (not splitted_line[8].startswith("O")) and need_premises:
                type_conc = splitted_line[8].strip()

            tweet_list.append(splitted_line[0])
            prev_line = splitted_line
            # if splitted_line[]
        if not is_arg:
            nonargs += 1
            continue
        tweet = " ".join(tweet_list)
        number = filename.split("_")[-1].replace(".conll", "")
        extra_info = {"number": number}
        if need_collective:
            extra_info["collective"] = " ".join(collective)
            extra_info["property"] = " ".join(property)
        if need_premises:
            extra_info["justification"] = " ".join(justification) + " (" + type_just + ") "
            extra_info["conclusion"] = " ".join(conclusion) + " (" + type_conc + ") "
            extra_info["pivot"] = " ".join(pivot)

        # print(tweet)
        counternarratives = []
        cn = open(filename.replace("conll", "cn"), "r")
        if use_extra_info.startswith("cn_"):
            cn_not_present = False
        for idx, line in enumerate(cn):
            if use_extra_info == "cn_a" or use_extra_info == "cn_a_no_info":
                if idx == 0:
                    if line.replace("\n", "").strip() != "":
                        counternarratives.append(line)
                    else:
                        cn_not_present = True
            elif use_extra_info == "cn_b" or use_extra_info == "cn_b_no_info":
                if idx == 1:
                    if line.replace("\n", "").strip() != "":
                        counternarratives.append(line)
                    else:
                        cn_not_present = True
            elif use_extra_info == "cn_c" or use_extra_info == "cn_c_no_info":
                if idx == 2:
                    if line.replace("\n", "").strip() != "":
                        counternarratives.append(line)
                    else:
                        cn_not_present = True
            else:
                if line.replace("\n", "").strip() != "":
                    counternarratives.append(line)
        if tweet in cns_by_tweet:
            cns_by_tweet[tweet]["cns"] += counternarratives
        else:
            if use_extra_info.startswith("cn_") and cn_not_present:
                cn_type_not_present += 1
            else:
                cns_by_tweet[tweet] = {"cns": counternarratives, "lang": language, "extra_info": extra_info}
        cn_length += len(counternarratives)
        # TODO: Change for an assert
        if use_extra_info.startswith("cn_") and len(counternarratives) > 1:
            raise ValueError(
                f"Error parsing the data: Expected at most one counternarrative for {use_extra_info}, "
                f"but found {len(counternarratives)}. Check the file {filename} for inconsistencies."
            )
    return cns_by_tweet, nonargs, cn_length, cn_type_not_present

def load_asohmo(use_extra_info="", finetuning=False):

    cns_by_tweet, nonargs, cn_length, cn_type_not_present = parse_dataset(f"dataset/ASOHMO/spanish/test/*.conll", use_extra_info=use_extra_info)
    cns_by_tweet_train, nonargs2, cn_length2, cn_type_not_present2 = parse_dataset(f"dataset/ASOHMO/spanish/train/*.conll", use_extra_info=use_extra_info)
    cns_by_tweet_dev, nonargs3, cn_length3, cn_type_not_present3 = parse_dataset(f"dataset/ASOHMO/spanish/dev/*.conll", use_extra_info=use_extra_info)
    print(f"{nonargs} - {nonargs2} - {nonargs3}")
    nonargs += nonargs2 + nonargs3
    cn_length += cn_length2 + cn_length3
    cn_type_not_present += cn_type_not_present2 + cn_type_not_present3

    # REVIEW
    print(f"Counter narratives without the required type of counter-narrative: {cn_type_not_present}")
    print(f"Non arg examples discarted for not having CN: {nonargs}")
    test_dataset = []
    print(f"{len(cns_by_tweet.keys())} - {len(cns_by_tweet_train.keys())} - {len(cns_by_tweet_dev.keys())}")
    train_dataset = []
    val_dataset = []
    keys = list(cns_by_tweet.keys())
    keys.sort()
    random.seed(42)
    random.shuffle(keys)
    for key in keys:
        # If we are finetuning a model we generate one example by each cn. Otherwise, all cns are within an example as a list
        if finetuning:
            for cn in cns_by_tweet[key]["cns"]:
                to_append = {"hateSpeech": key, "extra_info": cns_by_tweet[key]["extra_info"], "counterSpeech": cn, "language": cns_by_tweet[key]["lang"]}
                test_dataset.append(to_append)
        else:
            to_append = {"hateSpeech": key, "extra_info": cns_by_tweet[key]["extra_info"], "counterSpeech": cns_by_tweet[key]["cns"], "language": cns_by_tweet[key]["lang"]}
            test_dataset.append(to_append)

    for key in cns_by_tweet_train:
        for cn in cns_by_tweet_train[key]["cns"]:
            to_append = {"hateSpeech": key, "extra_info": cns_by_tweet_train[key]["extra_info"], "counterSpeech": cn, "language": cns_by_tweet_train[key]["lang"]}
            train_dataset.append(to_append)
    for key in cns_by_tweet_dev:
        for cn in cns_by_tweet_dev[key]["cns"]:
            to_append = {"hateSpeech": key, "extra_info": cns_by_tweet_dev[key]["extra_info"], "counterSpeech": cn, "language": cns_by_tweet_dev[key]["lang"]}
            val_dataset.append(to_append)
    return [test_dataset, train_dataset, val_dataset]
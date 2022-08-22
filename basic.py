import json
import pandas as pd
from tabulate import tabulate

cols = ["Age",
        "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10",
        "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19", "Q20",
        "Q21", "Q22", "Q23", "Q24", "Q25", "Q26", "Q27", "Q28", "Q29", "Q30",
        "Q31", "Q32", "Q33", "Q34",
        "Gender", "ID", "Student", "AnsSE", "AnsIA", "AnsHAPPY"]


def create_df(filename="data.json"):
    df = pd.DataFrame()
    for column in cols:
        df[column] = ""

    f = open(filename, "r")
    data = json.loads(f.read())
    print()
    for i in data:
        temp_list = []

        temp_list.append(data[i][" respondent"]["Age"].strip())
        iter_data = iter(data[i][" respondent"]["Answers1"])
        for j in iter_data:
            temp_list.append(j)
        temp_list.append(data[i][" respondent"]["Gender"].strip())
        temp_list.append(data[i][" respondent"]["ID"])
        temp_list.append(data[i][" respondent"]["Student"])

        temp_list.append(data[i][" samoocena"]["AnsSE"])
        temp_list.append(data[i][" uzaleznienie"]["AnsIA"])
        temp_list.append(data[i][" zadowolenie"]["AnsHAPPY"])

        del(temp_list[1])
        df.loc[len(df)] = temp_list
    df = df[(df.AnsIA <= 135) & (df.AnsIA >= 30)]
    df = df[(df.AnsSE <= 39) & (df.AnsSE >= 11)]
    df = df[(df.AnsHAPPY <= 15) & (df.AnsHAPPY >= 5)]
    df = df.drop(df[(df["Age"] == "0-15") & (df["Student"] is True)].index)
    return df


def evaluate_data():
    df = create_df()

    addicted = 0
    semi_addicted = 0
    not_addicted = 0

    confident = 0
    semi_confident = 0
    not_confident = 0

    happy = 0
    semi_happy = 0
    not_happy = 0

    for x in df['AnsIA'].tolist():  # Addiction
        if x >= 97:
            addicted += 1
        elif 97 > x >= 64:
            semi_addicted += 1
        else:
            not_addicted += 1

    for x in df['AnsSE'].tolist():  # Self-Confidence
        if x >= 25:
            confident += 1
        elif 25 > x >= 18:
            semi_confident += 1
        else:
            not_confident += 1

    for x in df['AnsHAPPY'].tolist():  # Happiness
        if x >= 11:
            happy += 1
        elif 11 > x >= 8:
            semi_happy += 1
        else:
            not_happy += 1

    num_of_rows = len(df)
    add = round((addicted / num_of_rows * 100), 2)
    sadd = round((semi_addicted / num_of_rows * 100), 2)
    nadd = round((not_addicted / num_of_rows * 100), 2)
    conf = round((confident / num_of_rows * 100), 2)
    sconf = round((semi_confident / num_of_rows * 100), 2)
    nconf = round((not_confident / num_of_rows * 100), 2)
    hpy = round((happy / num_of_rows * 100), 2)
    shpy = round((semi_happy / num_of_rows * 100), 2)
    nhpy = round((not_happy / num_of_rows * 100), 2)
    answers = [["addicted", addicted, add],
               ["semi addicted", semi_addicted, sadd],
               ["not addicted", not_addicted, nadd],
               ["confident", confident, conf],
               ["semi confident", semi_confident, sconf],
               ["not confident", not_confident, nconf],
               ["happy", happy, hpy],
               ["semi happy", semi_happy, shpy],
               ["not happy", not_happy, nhpy]]
    print(tabulate(answers, headers=["Classification", "Number of answers", "% of group"]))
    print()

    return df


def create_ml_dataframe():
    df = create_df()
    
    addicted = []
    confident = []
    happy = []

    for x in df['AnsIA'].tolist():  # Addiction
        if x >= 97:
            addicted.append("addicted")
        elif 97 > x >= 64:
            addicted.append("semi-addicted")
        else:
            addicted.append("not addicted")

    for x in df['AnsSE'].tolist():  # Self-Confidence
        if x >= 25:
            confident.append("confident")
        elif 25 > x >= 18:
            confident.append("semi-confident")
        else:
            confident.append("not confident")

    for x in df['AnsHAPPY'].tolist():  # Happiness
        if x >= 11:
            happy.append("happy")
        elif 11 > x >= 8:
            happy.append("semi-happy")
        else:
            happy.append("not happy")

    df["Addicted"] = addicted
    df["Confident"] = confident
    df["Happy"] = happy
    return df


if __name__ == "__main__":
    evaluate_data()

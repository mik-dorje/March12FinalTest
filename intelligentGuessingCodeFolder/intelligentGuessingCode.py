import pandas as pd


df = pd.read_csv("../intelligentGuessingDataSet.csv", encoding="ISO-8859-1")


def get_match_upto_index(text, sub_string):
    match = 0
    for i in range(len(sub_string) + 1):
        if sub_string[:i] in text:
            match = i
    return match


def clean_text(text):
    return (
        str(text).lower().replace("ô", "o").replace("ï", "i").replace("'", "").strip()
    )


def email_to_pattern(row):
    first_name = clean_text(row["firstname"])
    last_name = clean_text(row["lastname"])
    email = row["email"].split("@")[0].strip()
    email_pattern = ""

    if f"{first_name}{last_name}" == email:
        email_pattern = "<11><22>"

    elif email == first_name:
        email_pattern = "<11>"

    elif email == last_name:
        email_pattern = "<22>"

    elif "." in email or "-" in email:
        seperator = "." if "." in email else "-"

        if f"{first_name}{seperator}{last_name}" == email:
            email_pattern = f"<11>{seperator}<22>"

        elif f"{last_name}{seperator}{first_name}" == email:
            email_pattern = f"<22>{seperator}<11>"

        elif f"{first_name[0]}{seperator}{last_name}" == email:
            email_pattern = f"<1>{seperator}<22>"

        elif f"{last_name[0]}{seperator}{first_name}" == email:
            email_pattern = f"<20>{seperator}<11>"

        if " " in last_name or "-" in last_name:
            first_name_match_index = get_match_upto_index(email, first_name)

            last_name_split = (
                last_name.split(" ") if " " in last_name else last_name.split("-")
            )
            last_name0_match_index = get_match_upto_index(email, last_name_split[0])
            last_name1_match_index = get_match_upto_index(email, last_name_split[1])

            if (
                f"{first_name[:first_name_match_index]}{seperator}{''.join(last_name_split)}"
                == email
            ):
                if len(first_name) == first_name_match_index:
                    email_pattern = f"<11>{seperator}<20><21>"

                else:
                    chars = len(first_name[:first_name_match_index])
                    email_pattern = f"<11-f{chars}l>{seperator}<20><21>"

            elif (
                f"{first_name}{seperator}{last_name_split[0][:last_name0_match_index]}{last_name_split[1][:last_name1_match_index]}"
                == email
            ):

                if (
                    len(last_name_split[0]) == last_name0_match_index
                    and len(last_name_split[1]) == last_name1_match_index
                ):
                    email_pattern = f"<11>{seperator}<20><21>"

                elif (
                    len(last_name_split[0]) == last_name0_match_index
                    and len(last_name_split[1]) != last_name1_match_index
                ):
                    chars = len(last_name_split[1][:last_name1_match_index])
                    email_pattern = (
                        f"<11>{seperator}<20><21-f{chars}l>"
                        if chars > 0
                        else f"<11>{seperator}<20>"
                    )

                elif (
                    len(last_name_split[0]) != last_name0_match_index
                    and len(last_name_split[1]) == last_name1_match_index
                ):
                    chars = len(last_name_split[0][:last_name0_match_index])
                    email_pattern = (
                        f"<11>{seperator}<20-f{chars}l><21>"
                        if chars > 0
                        else f"<11>{seperator}<21>"
                    )

            elif f"{first_name}{seperator}{last_name_split[0]}" == email:
                email_pattern = f"<11>{seperator}<20>"

            elif f"{first_name}{seperator}{last_name_split[1]}" == email:
                email_pattern = f"<11>{seperator}<21>"

            elif f"{first_name}{seperator}{''.join(last_name_split)}" == email:
                email_pattern = f"<11>{seperator}<20><21>"

            elif (
                f"{first_name}{last_name_split[0]}{seperator}{last_name_split[1]}"
                == email
            ):
                email_pattern = f"<11><20>{seperator}<21>"

        elif "-" in first_name:
            first_name_split = first_name.split("-")
            if f"{first_name_split[0]}{seperator}{last_name}" == email:
                email_pattern = f"<10>{seperator}<22>"

            elif f"{first_name_split[1]}{seperator}{last_name}" == email:
                email_pattern = f"<11>{seperator}<22>"

            elif f"{''.join(first_name_split)}{seperator}{last_name}" == email:
                email_pattern = f"<10><11>{seperator}<22>"

            elif (
                f"{first_name_split[0]}{last_name_split[0]}{seperator}{last_name_split[1]}"
                == email
            ):
                email_pattern = f"<10><20>{seperator}<21>"

    elif f"{last_name[0]}{first_name}" == email:
        email_pattern = "<2><11>"

    elif f"{first_name[0]}{last_name}" == email:
        email_pattern = "<1><22>"

    return email_pattern


for index, row in df.loc[df["firstname"].isnull()].iterrows():
    email = row["email"].split("@")[0]
    if "." in email or "-" in email:
        first_name, last_name = email.split(".") if "." in email else email.split("-")
        df.loc[index, "firstname"] = first_name

for index, row in df.loc[df["lastname"].isnull()].iterrows():
    email = row["email"].split("@")[0]
    if "." in email or "-" in email:
        first_name, last_name = email.split(".") if "." in email else email.split("-")
        df.loc[index, "lastname"] = last_name


for index, row in df.loc[df["Email Pattern"].isnull()].iterrows():
    email_pattern = email_to_pattern(row)
    # print(index, email_pattern, comments, row["email"])
    df.loc[index, "Email Pattern"] = email_pattern

df.to_csv("../problemset1_submission.csv", index=False, columns=["rownum", "firstname", "lastname", "email", "Email Pattern"],
)

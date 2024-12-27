columns_correct = [
    "id",
    "name",
    "url",
    "price",
    "knowledge_id",
    "platform_id",
    "size_id",
    "created_at",
    "updated_at",
]


def columns_checker(file):
    if all(file.columns == columns_correct):
        print("columns ok!")
    else:
        print("incorrect columns!")


def id_checker(file):
    if file[columns_correct[0]].notnull().all():
        if file[columns_correct[0]].dtypes == "int64":
            print("id ok!")
        else:
            print("incorrect id values")
    else:
        print("there are null ids")


def name_checker(file):
    if file[columns_correct[1]].notnull().all():
        if file[columns_correct[1]].dtypes == "O":
            print("name ok!")
        else:
            print("incorrect name values")
    else:
        print("there are null names")


def url_checker(file):
    if file[columns_correct[2]].notnull().all():
        if file[columns_correct[2]].dtypes == "O":
            print("url ok!")
        else:
            print("incorrect url values")
    else:
        print("there are null urls")


def price_checker(file):
    if file[columns_correct[3]].notnull().all():
        if file[columns_correct[3]].dtypes == "int64":
            print("price ok!")
        else:
            print("incorrect price value")
    else:
        print("there are null prices")


def knowledge_id_checker(file):
    if file[columns_correct[4]].notnull().all():
        if file[columns_correct[4]].dtypes == "int64":
            print("knowledge_id ok!")
        else:
            print("incorrect knowledge_id value")
    else:
        print("there are null knowledge_ids")


def platform_id_checker(file):
    if file[columns_correct[5]].notnull().all():
        if file[columns_correct[5]].dtypes == "int64":
            print("pltaform_id ok!")
        else:
            print("incorrect pltaform_id value")
    else:
        print("there are null pltaform_ids")


def size_id_checker(file):
    if file[columns_correct[6]].notnull().all():
        if file[columns_correct[6]].dtypes == "int64":
            print("size_id ok!")
        else:
            print("incorrect size_id value")
    else:
        print("there are null size_ids")


def created_at_checker(file):
    if file[columns_correct[7]].notnull().all():
        if file[columns_correct[7]].dtypes == "O":
            print("created_at ok!")
        else:
            print("incorrect created_at values")
    else:
        print("there are null created_at")


def updated_at_checker(file):
    if file[columns_correct[8]].notnull().all():
        if file[columns_correct[8]].dtypes == "O":
            print("updated_at ok!")
        else:
            print("incorrect updated_at values")
    else:
        print("there are null updated_at")


def run_all_if_checker(df_bulk):
    columns_checker(df_bulk)
    id_checker(df_bulk)
    name_checker(df_bulk)
    knowledge_id_checker(df_bulk)
    platform_id_checker(df_bulk)
    url_checker(df_bulk)
    price_checker(df_bulk)
    size_id_checker(df_bulk)
    updated_at_checker(df_bulk)
    created_at_checker(df_bulk)
    print("finish if check")

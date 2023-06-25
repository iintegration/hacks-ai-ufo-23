import dramatiq
from dramatiq.brokers.redis import RedisBroker

import nltk
import re

from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from sklearn.metrics import mean_absolute_error
import os
from catboost import CatBoostRegressor, CatBoostClassifier, Pool, cv
from app.settings import SETTINGS

redis_broker = RedisBroker(url=SETTINGS.redis_dsn)
dramatiq.set_broker(redis_broker)


def preproc(df, info):
    col = info.columns[0]
    print(col)
    if col == "target":
        info = info.drop(columns=["target"])
        print(len(df["date_report"].unique()))
        for date_rep in df["date_report"].unique():
            info_val = df.loc[(df["date_report"] < date_rep), "target"].describe()
            info_list = [date_rep, info_val["count"], info_val["mean"], info_val["std"]]
            info.loc[len(info)] = info_list
        return info
    else:
        for val in df[col].dropna().unique():
            for date_rep in df["date_report"].unique():
                info_val = df.loc[
                    (df[col] == val) & (df["date_report"] < date_rep), "target"
                ].describe()
                info_list = [val, date_rep, info_val["count"], info_val["mean"], info_val["std"]]
                info.loc[len(info)] = info_list
        return info


def train_test_dataset(dir_dataset, name_xlsx):
    # Открываем датасет для предикта
    need_data = np.datetime64(name_xlsx.replace(".xlsx", "").replace(".", "-"))

    data_test = pd.read_excel(os.path.join(dir_dataset, name_xlsx), dtype={"Кодзадачи": str})
    data_test = data_test.drop(columns=["obj_pwa_key", "№ п/п", "obj_shortName"])
    data_test = data_test.rename(
        columns={
            "Кодзадачи": "task_key",
            "НазваниеЗадачи": "task_name",
            "ПроцентЗавершенияЗадачи": "completion_percentage",
            "ДатаНачалаЗадачи": "date_start_task",
            "ДатаОкончанияЗадачи": "date_end_task",
            "ДатаначалаБП0": "date_start_bpo",
            "ДатаокончанияБП0": "date_end_bpo",
            "Статуспоэкспертизе": "examination_status",
            "Экспертиза": "examination",
        }
    )
    data_test["date_report"] = need_data
    data_test["task_key"] = data_test["task_key"].astype(str)

    # Открываем исторические данные на которых будем обучаться

    df_attr = pd.read_csv(os.path.join(dir_dataset, "attr.csv"))
    df_attr["date_report"] = pd.to_datetime(df_attr["date_report"])
    df_attr = df_attr.rename(
        columns={
            "состояние площадки": "square_status",
            "Площадь": "square",
            "Генпроектировщик": "gen_proect",
            "Генподрядчик": "gen_podr",
            "Кол-во рабочих": "n_workers",
        }
    )

    df_ksg = pd.read_csv(
        os.path.join(dir_dataset, "dataset_hackaton_ksg__v2__23062023__1710_GMT3.csv"),
        encoding="utf-8",
        sep=";",
        dtype={"Экспертиза": "object"},
    )

    df_ksg = df_ksg.drop(["Unnamed: 0", "№ п/п"], axis=1)
    df_ksg = df_ksg.rename(
        columns={
            "Кодзадачи": "task_key",
            "НазваниеЗадачи": "task_name",
            "ПроцентЗавершенияЗадачи": "completion_percentage",
            "ДатаНачалаЗадачи": "date_start_task",
            "ДатаОкончанияЗадачи": "date_end_task",
            "ДатаначалаБП0": "date_start_bpo",
            "ДатаокончанияБП0": "date_end_bpo",
            "Статуспоэкспертизе": "examination_status",
            "Экспертиза": "examination",
        }
    )

    # Добавляем данные для предсказания

    df_ksg = pd.concat([df_ksg, data_test], ignore_index=True)

    # заполняем пропуски дат в договоре

    df_ksg = df_ksg.sort_values(["obj_key", "task_key", "date_end_bpo"])
    df_ksg = df_ksg.fillna(
        {
            "date_end_bpo": df_ksg.groupby(["obj_key", "task_key"])["date_end_bpo"].transform(
                "first"
            )
        }
    )
    df_ksg = df_ksg.sort_values(["obj_key", "task_key", "date_end_bpo"])
    df_ksg = df_ksg.fillna(
        {
            "date_start_bpo": df_ksg.groupby(["obj_key", "task_key"])["date_start_bpo"].transform(
                "first"
            )
        }
    )

    # заполнем пропуски в экспертизах

    df_ksg["examination_status"] = df_ksg["examination_status"].fillna(0.0)
    df_ksg["examination"] = df_ksg["examination"].fillna("0")

    # дропаем пропуски, где не дано названия задачи и кода

    df_ksg = df_ksg.dropna(subset="task_name")
    df_ksg = df_ksg.dropna(subset="task_key")

    df_ksg["date_start_task"] = pd.to_datetime(df_ksg["date_start_task"])
    df_ksg["date_end_task"] = pd.to_datetime(df_ksg["date_end_task"])
    df_ksg["date_start_bpo"] = pd.to_datetime(df_ksg["date_start_bpo"])
    df_ksg["date_end_bpo"] = pd.to_datetime(df_ksg["date_end_bpo"])
    df_ksg["date_report"] = pd.to_datetime(df_ksg["date_report"])

    # display(df_ksg.tail())
    # display(df_ksg.info())
    # Очищаем и лемантизиреум task_name

    nltk.download("stopwords")
    stop_words = list(stopwords.words("russian"))
    df_ksg["task_name"] = df_ksg["task_name"].apply(
        lambda x: " ".join(re.sub(r"[^а-яА-ЯёЁ]", " ", x.lower()).split())
    )
    df_ksg["task_name"] = df_ksg["task_name"].apply(
        lambda x: " ".join([word for word in x.split() if word not in stop_words])
    )
    df_ksg["task_name"] = df_ksg["task_key"] + "_" + df_ksg["task_name"]

    # сбор таргета
    df_ksg["target"] = df_ksg.groupby(["obj_key", "task_name"])["date_end_task"].transform(
        lambda x: x.shift(-1) - x
    )
    df_ksg["target"] = df_ksg["target"].dt.days

    # Делаем загушку для таргета у данных которые будем предсказывать
    df_ksg.loc[df_ksg["date_report"] == need_data, "target"] = -1

    df_ksg = df_ksg.dropna(subset="target")
    df_ksg["target"] = df_ksg["target"].astype(int)

    # Очищаем датасет от аномалий
    q001 = df_ksg["target"].quantile(0.01)
    q099 = df_ksg["target"].quantile(0.99)

    anomaly_df = (
        df_ksg.loc[(df_ksg["target"] > q099) | (df_ksg["target"] < q001)]
        .groupby(["obj_key", "task_name"], as_index=False)
        .count()
    )

    anomaly_df = anomaly_df[["obj_key", "task_name"]]

    df_ksg = pd.merge(df_ksg, anomaly_df, on=["obj_key", "task_name"], how="outer", indicator=True)

    df_ksg = df_ksg.query("_merge == 'left_only'").drop(columns="_merge")

    # месяц и сезон для каждой даты
    dates = [col for col in df_ksg.columns if "date" in col]
    for date_name in dates:
        df_ksg.loc[:, f"{date_name}_month"] = df_ksg[date_name].dt.month
        df_ksg.loc[:, f"{date_name}_season"] = (df_ksg[f"{date_name}_month"] % 12 + 3) // 3

    # разница дат
    date_pairs = {
        "date_end_task": "date_start_task",
        "date_end_bpo": "date_start_bpo",
        "date_start_task": "date_start_bpo",
        "date_end_task": "date_end_bpo",
    }
    for date_name1, date_name2 in date_pairs.items():
        df_ksg.loc[:, f"diff_{date_name1[5:]}_{date_name2[5:]}"] = (
            df_ksg[date_name1] - df_ksg[date_name2]
        ).dt.days.astype(float)

    df_ksg = df_ksg.merge(df_attr, how="left", on=["obj_key", "date_report"])

    # Данные по таргету
    gen_target_info = pd.DataFrame(
        columns=["target", "date_report", "gen_target_count", "gen_target_mean", "gen_target_std"]
    )

    gen_target_info = preproc(df_ksg, gen_target_info)

    # Данные о подрядчике
    gen_podr_info = pd.DataFrame(
        columns=[
            "gen_podr",
            "date_report",
            "podr_target_count",
            "podr_target_mean",
            "podr_target_std",
        ]
    )
    gen_podr_info = preproc(df_ksg, gen_podr_info)

    # Программа строительства
    gen_obj_prg_info = pd.DataFrame(
        columns=[
            "obj_prg",
            "date_report",
            "obj_prg_target_count",
            "obj_prg_target_mean",
            "obj_prg_target_std",
        ]
    )

    gen_obj_prg_info = preproc(df_ksg, gen_obj_prg_info)

    # Подпрограмма строительства
    sub_prg_info = pd.DataFrame(
        columns=[
            "obj_subprg",
            "date_report",
            "sub_prg_target_count",
            "sub_prg_target_mean",
            "sub_prg_target_std",
        ]
    )

    sub_prg_info = preproc(df_ksg, sub_prg_info)

    # Статус по экспертизе
    exam_stat_info = pd.DataFrame(
        columns=[
            "examination_status",
            "date_report",
            "exam_stat_target_count",
            "exam_stat_target_mean",
            "exam_stat_target_std",
        ]
    )

    exam_stat_info = preproc(df_ksg, exam_stat_info)

    # Экспертиза
    ex_info = pd.DataFrame(
        columns=[
            "examination",
            "date_report",
            "ex_target_count",
            "ex_target_mean",
            "ex_target_std",
        ]
    )

    ex_info = preproc(df_ksg, ex_info)

    # Мерджим всё
    df_ksg = df_ksg.merge(exam_stat_info, on=["examination_status", "date_report"], how="left")
    df_ksg = df_ksg.merge(sub_prg_info, on=["obj_subprg", "date_report"], how="left")
    df_ksg = df_ksg.merge(gen_obj_prg_info, on=["obj_prg", "date_report"], how="left")
    df_ksg = df_ksg.merge(gen_podr_info, on=["gen_podr", "date_report"], how="left")
    df_ksg = df_ksg.merge(ex_info, on=["examination", "date_report"], how="left")
    df_ksg = df_ksg.merge(gen_target_info, on=["date_report"], how="left")

    data_test = df_ksg[df_ksg["date_report"] == need_data].drop(columns=["target"])
    df_ksg = df_ksg[df_ksg["date_report"] != need_data]

    return df_ksg, data_test


def train_test_dataset(dir_dataset, name_xlsx):
    # Открываем датасет для предикта
    need_data = np.datetime64(name_xlsx.replace(".xlsx", "").replace(".", "-"))

    data_test = pd.read_excel(os.path.join(dir_dataset, name_xlsx), dtype={"Кодзадачи": str})
    data_test = data_test.drop(columns=["obj_pwa_key", "№ п/п", "obj_shortName"])
    data_test = data_test.rename(
        columns={
            "Кодзадачи": "task_key",
            "НазваниеЗадачи": "task_name",
            "ПроцентЗавершенияЗадачи": "completion_percentage",
            "ДатаНачалаЗадачи": "date_start_task",
            "ДатаОкончанияЗадачи": "date_end_task",
            "ДатаначалаБП0": "date_start_bpo",
            "ДатаокончанияБП0": "date_end_bpo",
            "Статуспоэкспертизе": "examination_status",
            "Экспертиза": "examination",
        }
    )
    data_test["date_report"] = need_data
    data_test["task_key"] = data_test["task_key"].astype(str)

    # Открываем исторические данные на которых будем обучаться

    df_attr = pd.read_csv(os.path.join(dir_dataset, "attr.csv"))
    df_attr["date_report"] = pd.to_datetime(df_attr["date_report"])
    df_attr = df_attr.rename(
        columns={
            "состояние площадки": "square_status",
            "Площадь": "square",
            "Генпроектировщик": "gen_proect",
            "Генподрядчик": "gen_podr",
            "Кол-во рабочих": "n_workers",
        }
    )

    df_ksg = pd.read_csv(
        os.path.join(dir_dataset, "dataset_hackaton_ksg__v2__23062023__1710_GMT3.csv"),
        encoding="utf-8",
        sep=";",
        dtype={"Экспертиза": "object"},
    )

    df_ksg = df_ksg.drop(["Unnamed: 0", "№ п/п"], axis=1)
    df_ksg = df_ksg.rename(
        columns={
            "Кодзадачи": "task_key",
            "НазваниеЗадачи": "task_name",
            "ПроцентЗавершенияЗадачи": "completion_percentage",
            "ДатаНачалаЗадачи": "date_start_task",
            "ДатаОкончанияЗадачи": "date_end_task",
            "ДатаначалаБП0": "date_start_bpo",
            "ДатаокончанияБП0": "date_end_bpo",
            "Статуспоэкспертизе": "examination_status",
            "Экспертиза": "examination",
        }
    )

    # Добавляем данные для предсказания

    df_ksg = pd.concat([df_ksg, data_test], ignore_index=True)

    # заполняем пропуски дат в договоре

    df_ksg = df_ksg.sort_values(["obj_key", "task_key", "date_end_bpo"])
    df_ksg = df_ksg.fillna(
        {
            "date_end_bpo": df_ksg.groupby(["obj_key", "task_key"])["date_end_bpo"].transform(
                "first"
            )
        }
    )
    df_ksg = df_ksg.sort_values(["obj_key", "task_key", "date_end_bpo"])
    df_ksg = df_ksg.fillna(
        {
            "date_start_bpo": df_ksg.groupby(["obj_key", "task_key"])["date_start_bpo"].transform(
                "first"
            )
        }
    )

    # заполнем пропуски в экспертизах

    df_ksg["examination_status"] = df_ksg["examination_status"].fillna(0.0)
    df_ksg["examination"] = df_ksg["examination"].fillna("0")

    # дропаем пропуски, где не дано названия задачи и кода

    df_ksg = df_ksg.dropna(subset="task_name")
    df_ksg = df_ksg.dropna(subset="task_key")

    df_ksg["date_start_task"] = pd.to_datetime(df_ksg["date_start_task"])
    df_ksg["date_end_task"] = pd.to_datetime(df_ksg["date_end_task"])
    df_ksg["date_start_bpo"] = pd.to_datetime(df_ksg["date_start_bpo"])
    df_ksg["date_end_bpo"] = pd.to_datetime(df_ksg["date_end_bpo"])
    df_ksg["date_report"] = pd.to_datetime(df_ksg["date_report"])

    # display(df_ksg.tail())
    # display(df_ksg.info())
    # Очищаем и лемантизиреум task_name

    nltk.download("stopwords")
    stop_words = list(stopwords.words("russian"))
    df_ksg["task_name"] = df_ksg["task_name"].apply(
        lambda x: " ".join(re.sub(r"[^а-яА-ЯёЁ]", " ", x.lower()).split())
    )
    df_ksg["task_name"] = df_ksg["task_name"].apply(
        lambda x: " ".join([word for word in x.split() if word not in stop_words])
    )
    df_ksg["task_name"] = df_ksg["task_key"] + "_" + df_ksg["task_name"]

    # сбор таргета
    df_ksg["target"] = df_ksg.groupby(["obj_key", "task_name"])["date_end_task"].transform(
        lambda x: x.shift(-1) - x
    )
    df_ksg["target"] = df_ksg["target"].dt.days

    # Делаем загушку для таргета у данных которые будем предсказывать
    df_ksg.loc[df_ksg["date_report"] == need_data, "target"] = -1

    df_ksg = df_ksg.dropna(subset="target")
    df_ksg["target"] = df_ksg["target"].astype(int)

    # Очищаем датасет от аномалий
    q001 = df_ksg["target"].quantile(0.01)
    q099 = df_ksg["target"].quantile(0.99)

    anomaly_df = (
        df_ksg.loc[(df_ksg["target"] > q099) | (df_ksg["target"] < q001)]
        .groupby(["obj_key", "task_name"], as_index=False)
        .count()
    )

    anomaly_df = anomaly_df[["obj_key", "task_name"]]

    df_ksg = pd.merge(df_ksg, anomaly_df, on=["obj_key", "task_name"], how="outer", indicator=True)

    df_ksg = df_ksg.query("_merge == 'left_only'").drop(columns="_merge")

    # месяц и сезон для каждой даты
    dates = [col for col in df_ksg.columns if "date" in col]
    for date_name in dates:
        df_ksg.loc[:, f"{date_name}_month"] = df_ksg[date_name].dt.month
        df_ksg.loc[:, f"{date_name}_season"] = (df_ksg[f"{date_name}_month"] % 12 + 3) // 3

    # разница дат
    date_pairs = {
        "date_end_task": "date_start_task",
        "date_end_bpo": "date_start_bpo",
        "date_start_task": "date_start_bpo",
        "date_end_task": "date_end_bpo",
    }
    for date_name1, date_name2 in date_pairs.items():
        df_ksg.loc[:, f"diff_{date_name1[5:]}_{date_name2[5:]}"] = (
            df_ksg[date_name1] - df_ksg[date_name2]
        ).dt.days.astype(float)

    df_ksg = df_ksg.merge(df_attr, how="left", on=["obj_key", "date_report"])

    # Данные по таргету
    gen_target_info = pd.DataFrame(
        columns=["target", "date_report", "gen_target_count", "gen_target_mean", "gen_target_std"]
    )

    gen_target_info = preproc(df_ksg, gen_target_info)

    # Данные о подрядчике
    gen_podr_info = pd.DataFrame(
        columns=[
            "gen_podr",
            "date_report",
            "podr_target_count",
            "podr_target_mean",
            "podr_target_std",
        ]
    )
    gen_podr_info = preproc(df_ksg, gen_podr_info)

    # Программа строительства
    gen_obj_prg_info = pd.DataFrame(
        columns=[
            "obj_prg",
            "date_report",
            "obj_prg_target_count",
            "obj_prg_target_mean",
            "obj_prg_target_std",
        ]
    )

    gen_obj_prg_info = preproc(df_ksg, gen_obj_prg_info)

    # Подпрограмма строительства
    sub_prg_info = pd.DataFrame(
        columns=[
            "obj_subprg",
            "date_report",
            "sub_prg_target_count",
            "sub_prg_target_mean",
            "sub_prg_target_std",
        ]
    )

    sub_prg_info = preproc(df_ksg, sub_prg_info)

    # Статус по экспертизе
    exam_stat_info = pd.DataFrame(
        columns=[
            "examination_status",
            "date_report",
            "exam_stat_target_count",
            "exam_stat_target_mean",
            "exam_stat_target_std",
        ]
    )

    exam_stat_info = preproc(df_ksg, exam_stat_info)

    # Экспертиза
    ex_info = pd.DataFrame(
        columns=[
            "examination",
            "date_report",
            "ex_target_count",
            "ex_target_mean",
            "ex_target_std",
        ]
    )

    ex_info = preproc(df_ksg, ex_info)

    # Мерджим всё
    df_ksg = df_ksg.merge(exam_stat_info, on=["examination_status", "date_report"], how="left")
    df_ksg = df_ksg.merge(sub_prg_info, on=["obj_subprg", "date_report"], how="left")
    df_ksg = df_ksg.merge(gen_obj_prg_info, on=["obj_prg", "date_report"], how="left")
    df_ksg = df_ksg.merge(gen_podr_info, on=["gen_podr", "date_report"], how="left")
    df_ksg = df_ksg.merge(ex_info, on=["examination", "date_report"], how="left")
    df_ksg = df_ksg.merge(gen_target_info, on=["date_report"], how="left")

    data_test = df_ksg[df_ksg["date_report"] == need_data].drop(columns=["target"])
    df_ksg = df_ksg[df_ksg["date_report"] != need_data]

    return df_ksg, data_test


@dramatiq.actor
def analyze_data(object_name: str) -> None:
    dir_dataset = "train_dataset_Дипстрой"  # Папка где у меня хранятся датасеты
    name_xlsx = "2023.06.19.xlsx"  # Датасет, который необходимо предсказать

    data_train, data_predict = train_test_dataset(dir_dataset, name_xlsx)

    data_train = data_train.drop(
        columns=[
            "date_start_task",
            "date_end_task",
            "date_start_bpo",
            "date_end_bpo",
            "date_report",
        ]
    )
    data_predict = data_predict.drop(
        columns=[
            "date_start_task",
            "date_end_task",
            "date_start_bpo",
            "date_end_bpo",
            "date_report",
        ]
    )

    # Создаём датасет для классификации
    data_train_class = data_train.copy()
    data_train_class.loc[data_train_class["target"] != 0, "target"] = 1

    features_train, target_train = (
        data_train_class.drop(columns=["target"]),
        data_train_class["target"],
    )

    features_train[list(features_train.select_dtypes("object").columns)] = features_train[
        list(features_train.select_dtypes("object").columns)
    ].fillna("Пропущенное значение")

    data_predict[list(data_predict.select_dtypes("object").columns)] = data_predict[
        list(data_predict.select_dtypes("object").columns)
    ].fillna("Пропущенное значение")

    model_class = CatBoostClassifier(
        task_type="GPU",
        cat_features=list(features_train.select_dtypes(include=["object"]).columns),
        iterations=5000,  # Уменьшает разрыв очка если поставишь  100
        random_state=12345,
        learning_rate=0.006,
        depth=8,
        loss_function="Logloss",
        eval_metric="F1",
    )

    model_class.fit(features_train, target_train)

    del data_train_class

    # Создаём датасет для регрессии
    data_train = data_train[data_train["target"] != 0]
    features_train, target_train = data_train.drop(columns=["target"]), data_train["target"]
    del data_train

    features_train[list(features_train.select_dtypes("object").columns)] = features_train[
        list(features_train.select_dtypes("object").columns)
    ].fillna("Пропущенное значение")
    model_regres = CatBoostRegressor(
        task_type="GPU",
        cat_features=list(features_train.select_dtypes(include=["object"]).columns),
        iterations=8000,
        random_state=12345,
        depth=8,
        # loss_function ='RMSE',
        learning_rate=0.05,
    )

    model_regres.fit(features_train, target_train)

    pass

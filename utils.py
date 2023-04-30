import csv
import json
from glob import iglob
import datetime


posts_dir = "data/posts"
post_metadata_path = "data/post_metadata.tsv"
table_path = "data/table.tsv"


def load_table():
    with open(table_path, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        table = []
        for row in reader:
            table.append(row)
        return table


def load_post_metadata():
    try:
        with open(post_metadata_path, "r") as f:
            reader = csv.reader(f, delimiter="\t")
            metadata = []
            for row in reader:
                if len(row) == 3:
                    metadata.append({"url": row[0], "score": row[1], "num_comments": row[2]})
            return metadata
    except FileNotFoundError:
        return []


def append_post_metadata(record):
    # Open the TSV file in append mode
    with open(post_metadata_path, "a", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        # Write a new row to the TSV file with the extracted data
        writer.writerow([record.get("url"), record.get("score"), record.get("num_comments")])


def load_posts():
    submissions = []
    for data_path in iglob(f"{posts_dir}/*.json"):
        data = json.load(open(data_path))
        try:
            submissions.extend(data)
        except:
            print(data_path)
            exit()
    submissions = sorted(submissions, key=lambda x: x["created_utc"])

    oldest = min(submissions, key=lambda x: x["created_utc"])
    most_recent = max(submissions, key=lambda x: x["created_utc"])
    print(
        "Oldest submission:", datetime.datetime.utcfromtimestamp(oldest["created_utc"]).strftime("%Y-%m-%d %H:%M:%S")
    )
    print(
        "Most recent submission:",
        datetime.datetime.utcfromtimestamp(most_recent["created_utc"]).strftime("%Y-%m-%d %H:%M:%S"),
    )
    print("Number of submissions:", len(submissions))
    return submissions

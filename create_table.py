from utils import load_posts
from utils import load_post_metadata
import csv


def create_post_metadata_map(post_metadata):
    post_metadata_map = {}
    for post in post_metadata:
        post_metadata_map[post["url"]] = post
    return post_metadata_map


def main():
    table_path = "data/table.tsv"

    posts = load_posts()
    post_metadata = load_post_metadata()
    post_metadata_map = create_post_metadata_map(post_metadata)
    records = []

    for post in posts:
        url = post["url"]
        if len(url) == 0:
            continue
        score = None
        num_comments = None
        if url in post_metadata_map:
            score_str = post_metadata_map[url]["score"]
            num_comments_str = post_metadata_map[url]["num_comments"]
            score = int(score_str) if score_str else None
            num_comments = int(num_comments_str) if num_comments_str else None
        record = {
            "created_utc": post["created_utc"],
            "utc_datetime_str": post["utc_datetime_str"],
            "score": score,
            "num_comments": num_comments,
            "title": post["title"],
            "author": post["author"],
            "url": post["url"],
        }
        records.append(record)

    # Sort records by score
    records = sorted(records, key=lambda r: r["score"] if r["score"] is not None else float("-inf"), reverse=True)

    # Write records to table TSV file
    with open(table_path, mode="w", newline="", encoding="utf-8") as tsv_file:
        writer = csv.DictWriter(tsv_file, delimiter="\t", fieldnames=records[0].keys())
        writer.writeheader()
        for record in records:
            writer.writerow(record)


if __name__ == "__main__":
    main()

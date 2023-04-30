from utils import load_table
import datetime
import os
import matplotlib.pyplot as plt


def main():
    figures_dir = "analysis/data/figures"
    best_time_comments_fig_path = os.path.join(figures_dir, "best_time_comments.png")
    best_time_likes_fig_path = os.path.join(figures_dir, "best_time_upvotes.png")

    os.makedirs(figures_dir, exist_ok=True)
    table = load_table()

    hour_counts = {}
    for post in table:
        created_utc = post.get("created_utc")
        num_comments = post.get("num_comments")

        score = post.get("score")
        if score is not None and len(score) > 0:
            score = int(score)
        else:
            score = 0

        if created_utc is None or num_comments is None or len(created_utc) == 0 or len(num_comments) == 0:
            continue

        created_utc = int(created_utc)
        num_comments = int(num_comments)

        hour = datetime.datetime.utcfromtimestamp(created_utc).hour
        if hour in hour_counts:
            hour_counts[hour]["num_comments"] += num_comments
        else:
            hour_counts[hour] = {"num_comments": num_comments, "score": 0}

        if hour in hour_counts:
            hour_counts[hour]["score"] += score
        else:
            hour_counts[hour]["score"] = score

    # sort the table by num_comments in descending order
    table = sorted(hour_counts.items(), key=lambda x: x[1]["num_comments"], reverse=True)

    # print the table
    print("Hour\tNum Comments\tNumber of Upvotes")
    for hour, counts in table:
        num_comments = counts["num_comments"]
        score = counts["score"]
        print(f"{hour:02d}\t{num_comments}\t{score}")

    # find the hour with the most comments
    best_hour = table[0][0]

    # print the best hour to post
    print("Best hour to post (by number of comments):", best_hour)

    x = [hour for hour, counts in table]
    y = [counts["num_comments"] for hour, counts in table]
    plt.bar(x, y)

    # set the title and axis labels
    plt.title("Number of Comments by Hour of Day")
    plt.xlabel("Hour of Day (UTC)")
    plt.ylabel("Number of Comments")

    # save the chart as a PNG file
    plt.savefig(best_time_comments_fig_path)

    # sort the table by score in descending order
    table = sorted(hour_counts.items(), key=lambda x: x[1]["score"], reverse=True)

    # find the hour with the most score
    best_hour = table[0][0]

    # print the best hour to post
    print("Best hour to post (by number of upvotes):", best_hour)

    x = [hour for hour, counts in table]
    y = [counts["score"] for hour, counts in table]
    plt.bar(x, y)

    # set the title and axis labels
    plt.title("Number of Upvotes by Hour of Day")
    plt.xlabel("Hour of Day (UTC)")
    plt.ylabel("Number of Upvotes")

    # save the chart as a PNG file
    plt.savefig(best_time_likes_fig_path)


if __name__ == "__main__":
    main()

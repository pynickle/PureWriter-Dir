import sqlite3
import os
import shutil

book_name = "Python旅途"
db_name = "/data/data/com.drakeet.purewriter/databases/room.db"
root_dir = "/storage/emulated/0/documents/"

def between(lst, target):
    for i in range(len(lst)):
        if target >= lst[i] and target < lst[i+1]:
            return i

def make(book_name, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    folder = cur.execute("select * from Folder")
    for i in folder:
        if i[1] == book_name:
            folder_id = i[0]
            break

    categories = cur.execute("select * from Category order by rank")
    category_selected_id = []
    category_selected_name = []
    category_selected_rank = []

    for i in categories:
        if i[1] == folder_id:
            category_selected_id.append(i[0])
            category_selected_name.append(i[2])
            category_selected_rank.append(i[5])

    if os.path.isdir(root_dir + book_name):
        shutil.rmtree(root_dir + book_name)
    os.mkdir(root_dir + book_name)

    for i in category_selected_name:
        if not os.path.isdir(root_dir + book_name + "/" + i):
            os.mkdir(root_dir + book_name + "/" + i)

    rank_now = 2
    folder_now = 0

    articles = cur.execute(
        f"select * from Article where folderId='{folder_id}' and rank>0 order by rank asc")
    for i in articles:
        index = between(category_selected_rank, i[9])
        folder = category_selected_name[index]
        with open(root_dir + book_name + "/" + folder + "/" + i[1] + ".md", "w", encoding="utf-8") as f:
            f.write(i[2])

    cur.close()


if __name__ == "__main__":
    make(book_name, db_name)

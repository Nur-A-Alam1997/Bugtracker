import os


def remove_csv(filepath):
    dir_name = filepath
    test = os.listdir(dir_name)
    print(test)
    for item in test:
        if item.endswith(".csv") or item.endswith(".CSV"):
            # os.remove(item)
            print("done")
            # os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))


if __name__=="__main__":
    remove_csv()
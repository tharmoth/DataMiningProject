import csv
import time
import pickle
import matplotlib.pyplot as plt
from adjustText import adjust_text
import math


class AnimeStat:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.watchers_names = set()


class DataMiner:
    def __init__(self):
        self.key_to_anime = dict()
        self.key_to_pop = dict()
        self.animelist_path = "MAL_Dataset/UserAnimeList.csv"
        self.anime_path = "MAL_Dataset/AnimeList.csv"
        self.animelist_filtered_path = "MAL_Dataset/animelists_filtered.csv"
        self.row_count = 0
        self.sorted_dict = dict()
        self.key_to_AnimeStat = dict()
        pass

    def count_rows(self, path):
        tic = time.perf_counter()
        row_count = sum(1 for row in open(path))
        print(row_count)
        toc = time.perf_counter()
        print("Row counting took " + str(toc - tic) + " seconds.")
        self.row_count = row_count
        return row_count

    def read_anime(self):
        tic = time.perf_counter()
        csv.field_size_limit(1000000)
        num = 0
        with open(self.anime_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                self.key_to_anime[row[0]] = row[1]
                num += 1
        for k, v in self.key_to_anime.items():
            pass
        toc = time.perf_counter()
        print("Read in the info about " + str(num) + " shows")
        print("Anime read took " + str(toc - tic) + " seconds.")

    def read_animelists(self):
        tic = time.perf_counter()
        with open(self.animelist_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    self.key_to_pop[row[1]] += 1
                except KeyError:
                    self.key_to_pop[row[1]] = 1

        toc = time.perf_counter()
        print("Animelist read took " + str(toc - tic) + " seconds.")

    def read_anime_animelist(self, anime1_id, anime2_id):
        names = set()
        num_shared = 0
        tic = time.perf_counter()
        with open(self.animelist_filtered_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[1] == anime1_id:
                    if row[0] in names:
                        num_shared += 1
                    names.add(row[0])
                elif row[1] == anime2_id:
                    if row[0] in names:
                        num_shared += 1
                    names.add(row[0])

        toc = time.perf_counter()
        print(num_shared)
        print("Animelist read took " + str(toc - tic) + " seconds.")

    def read_animelist_adv(self):
        tic = time.perf_counter()
        with open(self.animelist_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                try:
                    self.key_to_AnimeStat[row[1]].watchers_names.add(row[0])
                except KeyError:
                    self.key_to_AnimeStat[row[1]] = AnimeStat(row[1], self.key_to_anime.get(row[1]))
                    self.key_to_AnimeStat[row[1]].watchers_names.add(row[0])

        toc = time.perf_counter()
        print("Animelist read took " + str(toc - tic) + " seconds.")
        for stat in self.key_to_AnimeStat.values():
            print(stat.id, stat.name, len(stat.watchers_names))

    def print_top(self):
        self.sorted_dict = sorted(self.key_to_pop.items(), key=lambda x: x[1], reverse=True)
        i = 0
        for k, v in self.sorted_dict:
            i += 1
            print("#" + str(i) + " - " + str(self.key_to_anime.get(k)) + " " + str(v))
            if i >= 100:
                break

    def read(self, refresh=True):
        if refresh:
            self.read_anime()
            self.read_animelists()
            pickle.dump(self.key_to_pop, open("key_to_pop.p", "wb"))
            pickle.dump(self.key_to_anime, open("key_to_anime.p", "wb"))
        else:
            self.key_to_pop = pickle.load(open("key_to_pop.p", "rb"))
            self.key_to_anime = pickle.load(open("key_to_anime.p", "rb"))
        #self.print_top()
        #self.read_anime_animelist(self.get_id_from_name("Death Note"), self.get_id_from_name("Toradora!"))
        self.read_animelist_adv()
        #self.plot()

    def get_id_from_name(self, search_value):
        for key, value in self.key_to_anime.items():
            if value == search_value:
                return key

    def plot(self):
        print("Plotting!")
        # repackage data into array-like for matplotlib
        # (see a preferred pythonic way below)
        data = {"x": [], "y": [], "label": []}
        i = 0
        for label, coord in self.sorted_dict:
            i += 1
            data["x"].append(i)
            data["y"].append(coord)
            data["label"].append(self.key_to_anime.get(label))
            if i >= 50:
                break

        # display scatter plot data
        plt.figure(figsize=(10, 8))
        plt.title('Popularity of Anime in 2018', fontsize=20)
        plt.xlabel('Anime Rank', fontsize=15)
        plt.ylabel('Number of Viewers on MAL', fontsize=15)
        plt.scatter(data["x"], data["y"], marker='o')

        # add labels
        for label, x, y in zip(data["label"], data["x"], data["y"]):
            plt.annotate(label, xy=(x+.25, y+1000), fontsize=10, rotation=90, rotation_mode='anchor')

        plt.show()


if __name__ == '__main__':
    # miner = DataMiner()
    # miner.read(False)
    print(math.factorial(15000)/(2*math.factorial(14998)))



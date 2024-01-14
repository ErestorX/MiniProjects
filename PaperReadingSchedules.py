from copy import deepcopy
import datetime
import argparse
import random
import json
import os


parser = argparse.ArgumentParser()
parser.add_argument('-date', default=datetime.date.today(), type=str)


def makeMondayListFromStart(startDate, nbWeeks):
    """
    Return a list of dates, starting from startDate, with nbWeeks weeks
    """
    mondayList = []
    for i in range(nbWeeks):
        date = startDate + datetime.timedelta(days=7*i)
        mondayList.append(date.strftime("%b-%d-%Y"))
    return mondayList


def loadStudentLists(path):
    """
    Return a list of students lists from a json file
    """
    with open(path, 'r') as f:
        studentsLists = json.load(f)
    return studentsLists["PhD"], studentsLists["MS"], studentsLists["BS"]


def makePresentorReviewersList(studentsList):
    """
    Return a list of tuple of 1 presentors and 2 random reviewers from a students list
    """
    def hasAlreadyReviewed(reviewer, trinomes, key="Reviewer 1"):
        """
        Return True if reviewer has already reviewed 2 times
        """
        for trinome in trinomes:
            if reviewer == trinome[key]:
                return True
        return False

    random.shuffle(studentsList)
    presentors = studentsList
    reviewers1 = deepcopy(studentsList)
    reviewers2 = deepcopy(studentsList)
    trinomes = []
    for presentor in presentors:
        trinome = {"Presentor": presentor, "Reviewer 1": None, "Reviewer 2": None}
        reviewer1 = random.sample(reviewers1, 1)[0]
        while hasAlreadyReviewed(reviewer1, trinomes, key="Reviewer 1") or reviewer1 == presentor:
            reviewer1 = random.sample(reviewers1, 1)[0]
        trinome["Reviewer 1"] = reviewer1
        reviewers1.remove(reviewer1)
        reviewer2 = random.sample(reviewers2, 1)[0]
        while hasAlreadyReviewed(reviewer2, trinomes, key="Reviewer 2") or reviewer2 == presentor or reviewer2 == reviewer1:
            reviewer2 = random.sample(reviewers2, 1)[0]
        trinome["Reviewer 2"] = reviewer2
        reviewers2.remove(reviewer2)
        trinomes.append(trinome)
    return trinomes


def send_BSstudents_to_end(trinomes, list_BSstudents):
    """
    Return a list of trinomes with BS students at the end
    """
    trinomes_BS = []
    trinomes_others = []
    for trinome in trinomes:
        if trinome["Presentor"] in list_BSstudents:
            trinomes_BS.append(trinome)
        else:
            trinomes_others.append(trinome)
    return trinomes_others + trinomes_BS


if __name__ == '__main__':
    args = parser.parse_args()
    if isinstance(args.date, type(datetime.date.today())):
        date = args.date
    else:
        Y, M, D = args.date.split("-")
        date = datetime.date(int(Y), int(M), int(D))

    PhD, MS, BS = loadStudentLists(os.path.join(os.path.dirname(__file__), "studentLists.json"))
    paperReadingPresentors = PhD + MS + BS
    trinomes = makePresentorReviewersList(paperReadingPresentors)
    trinomes = send_BSstudents_to_end(trinomes, BS)
    mondays = makeMondayListFromStart(date, len(trinomes))

    for i in range(len(trinomes)):
        print(mondays[i], "- Presentor:", trinomes[i]["Presentor"], "\n\t\t\t  Reveiwers:", trinomes[i]["Reviewer 1"], ",", trinomes[i]["Reviewer 2"])
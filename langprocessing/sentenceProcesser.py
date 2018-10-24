import views.ois.courses as oisCourses
import views.ois.structuralUnits as oisStrucUnits
from collections import defaultdict
import estnltk as enl
from estnltk import Text
import itertools
import logging
import csv
import os
from langprocessing.wordTags import WordTag as wt

class SentenceProcessor:
    def __init__(self):
        self.courses = self._getCourses()
        self.structuralUnits = self._getStructuralUnits()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('DEBUG')

    def getWords(self, sentence):
        """
        :param sentence: User input
        :return: tagged words in dictionary
        """
        text = Text(sentence)
        result = self._tagWords(text)
        self.logger.debug('Founded words: ' + str(result))
        return result

    def _tagWords(self, inputText: Text):
        """
        Tags words and forms result dictionary
        :param inputText: Text object with morph_analysis layer
        :return: tagged words in dictionary
        """
        questionwords = ['kes', 'mis', 'kus', 'mitu']  # todo more or think something else
        whatIsQuestionSecondWord = ['tähendama', 'on'] # TODO: think of a better variable name
        courseCodeWords = ['ainekood', 'kood']
        preReqMentionWords = ['eeldusaine', 'eeldus']
        greetings = ['tere', 'hei', 'hommikust', 'hommik', 'õhtust', 'tsau', 'ahoi']
        pronoun = ['mina', 'sina', 'tema', 'teie', 'meie', 'nemad']
        result = defaultdict(list)
        courses = self._getCourses()
        inputText.tag_layer(['morph_analysis'])

        # looks for courses from lemmatized courses dictionary
        lemmas = [x[0].lower() for x in inputText.morph_analysis.lemma]
        i = len(lemmas)
        coursesWords = []
        otherWords = []
        counter = 0
        wordCounter = 0

        for word in lemmas:
            if 'eap' in word and len(word) <= 4:
                result[wt.ects] = True
            elif word in courseCodeWords:
                result[wt.courseCodeMentioned] = True
            elif word in preReqMentionWords:
                result[wt.preReqs] = True
            elif word in questionwords:
                result[wt.questionWord] = word
            elif word in whatIsQuestionSecondWord and counter == 1:
                result[wt.whatIsQuestionSecondWord] = word
            elif word in greetings:
                result[wt.greeting] = True
            elif word in pronoun:
                result[wt.pronoun] = word
            elif word in self.structuralUnits:
                result[wt.structureUnitCode] = word
            else:
                otherWords.append(word)

            counter += 1

        while i > 0:
            for lemma in itertools.combinations(lemmas, i):
                word = " ".join(lemma)
                if word in courses:
                    result[wt.courseID] += (courses[word])
                    coursesWords += lemma
                elif i == 1 and word not in coursesWords and word in otherWords:
                    result[wordCounter] = word
                    wordCounter += 1
            i -= 1

        #for searching single words


        return result


    def _getCourses(self):
        """
        Reads courses from csv file
        :return: courses in dictionary
        """
        courses = defaultdict(list)
        with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), encoding="UTF-8") as file:
            reader = csv.reader(file)
            for line in reader:
                courses[line[0].strip()].append(line[1].strip())
            return courses

    def _getStructuralUnits(self):
        """
        Reads structural Units from csv file
        :return: structural Units' codes and names in estonian in a dictionary
        """
        sUnits = defaultdict(list)
        with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), encoding="UTF-8") as file:
            reader = csv.reader(file)
            for line in reader:
                sUnits[line[0].strip()].append(line[1].strip())
            return sUnits

    def updateCourses(self):
        self.updateCourses()
        self.logger.info('Updated courses dictionary')


def updateCoursesCSV():
    """
    Updates csv file where is all courses
    """
    with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), 'w', newline='', encoding="UTF-8") as file:
        n = 300
        writer = csv.writer(file, delimiter=',')
        i = 1
        courses = oisCourses.getNCourses(n, i)
        while len(courses) != 0:
            for c in courses:
                if 'title' in c:
                    if 'et' in c['title']:
                        t = Text(c['title']['et'].lower())
                        t.tag_layer(['morph_analysis'])
                        writer.writerow([" ".join([x[0] for x in t.morph_analysis.lemma]), c['code']])
                    elif 'en' in c['title']:
                        t = Text(c['title']['en'].lower())
                        t.tag_layer(['morph_analysis'])
                        writer.writerow([" ".join([x[0] for x in t.morph_analysis.lemma]), c['code']])
            i += n
            courses = oisCourses.getNCourses(n, i)

def updateStructuralUnitsCSV():
    """
    Updates csv file where are all the university structure units
    """
    with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), 'w', newline='', encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=',')
        sUnits = oisStrucUnits.getAllStructuralUnits()
        for c in sUnits:
            if 'code' in c:
                if 'et' in c['name']:
                    t = Text(c['name']['et'].lower())
                    t.tag_layer(['morph_analysis'])
                    writer.writerow([c['code'].lower(), " ".join([x[0] for x in t.morph_analysis.lemma])])









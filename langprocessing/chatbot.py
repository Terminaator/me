import views.ois.courses as oisCourses
import views.ois.structuralUnits as oisStructuralUnits
from estnltk.vabamorf.morf import synthesize, analyze
import langprocessing.sentenceProcesser as sentProc
from random import randint
from langprocessing.wordTags import WordTag as wt


class chatbot():
    def __init__(self):
        self.frames = {}
        self.currentFrame = -1
        self.sentenceProcessor = sentProc.SentenceProcessor()

    def getResponse(self, inputSentence):
        """
        fills the frame and returns an answer
        :param inputSentence: Question that the client asked
        :return:A response for the client
        """
        words = self.sentenceProcessor.getWords(inputSentence)
        self.addFrameLayer(words)
        return self.putTogetherAnAnswer()

    def putTogetherAnAnswer(self):
        """
        looks at the frame and answers based on that.
        :return: A response for the client
        """
        currentLayer = self.frames["layer " + str(self.currentFrame)]
        misc = currentLayer[wt.misc]
        courses = currentLayer[wt.courses]
        sUnits = currentLayer[wt.structureUnits]

        #WHAT IS questions
        if self.isWhatIsQuestionAsked(currentLayer):
            if sUnits[wt.structureUnitCode] != "":
                return self.answerWhatIsStructureCode(sUnits[wt.structureUnitCode])
            if courses[wt.courseID] != "":
                return self.answerWhatIsCourseCode(courses[wt.courseID])



        #COURSES questions
        if len(courses[wt.courseID]) != 0:
            if courses[wt.ects]:
                return self.answerCourseEcts(courses[wt.courseID])
            if courses[wt.courseCodeMentioned]:
                return self.answerCourseCode(courses[wt.courseID])
            if courses[wt.preReqs]:
                return self.answerCoursePreReqs(courses[wt.courseID])

        if misc[wt.greeting]:
            return self.sayHello()

        return "Kahjuks ma ei saanud teist aru."

    def addFrameLayer(self, words):
        """
        creates a new frame layer
        :param words:  dictionary of words to be added to the new frame layer
        """
        self.currentFrame += 1
        self.frames["layer " + str(self.currentFrame)] = self.fillFrameLayer(words)

    def fillFrameLayer(self, words):
        """
        fills a frame layer
        :param words: dictionary of words to be added to the layer
        :return: filled frame layer
        """
        layer = self.createEmptyLayer()
        for key in layer:
            for k in layer[key]:
                if (k in words):
                    layer[key][k] = words[k]
        for k in words:
            layer[wt.sentence].append(k)
        return layer

    def createEmptyLayer(self):
        """
        Creates a layer for frame
        Frame with 1 layer structure
        frame = {
            layer 0: {
                sentence : [words]
                misc : {questionWord: String, greeting: boolean, pronoun: String, wt.whatIsQuestionSecondWord: String}
                courses : {courseID: String, ects : boolean, preReqs : boolean, CourseCodeMentioned: boolean}
                structuralUnits: {structuralUnitCode: String}
            }
        }
        """
        misc = {wt.questionWord: "", wt.greeting: False, wt.pronoun: "", wt.whatIsQuestionSecondWord: ""}
        courses = {wt.courseID: "", wt.ects: False, wt.preReqs: False, wt.courseCodeMentioned: False}
        sUnit = {wt.structureUnitCode: ""}
        layer = {wt.sentence: [], wt.misc: misc, wt.courses: courses, wt.structureUnits: sUnit}
        return layer

    def isWhatIsQuestionAsked(self, currentLayer):
        """
        tries to see if user asked a "What is x" question
        :param currentLayer: currently used layer
        :return: Returns if client asked a term explanation question
        """
        misc = currentLayer[wt.misc]
        sentence = currentLayer[wt.sentence]
        if len(sentence) < 3:
            return False
        if sentence[1] != wt.whatIsQuestionSecondWord or sentence[0] != wt.questionWord:
            return False

        return (misc[wt.questionWord] in ["mis"] and misc[wt.whatIsQuestionSecondWord] in ["tähendama", "on"]) and (sentence[2] == wt.structureUnitCode or sentence[2] == wt.courseID)

    def answerWhatIsStructureCode(self, structureCode):
        """
        Creates an answer for a what is structure code question
        :param structureCode: structure code, that the client wants to know about
        :return: answer about the structure unit
        """
        json = oisStructuralUnits.getStructuralUnit(structureCode)
        return "Antud koodi kasutab struktuuriüksus: " + json["name"]["et"] + "."

    def answerWhatIsCourseCode(self, courseCode):
        json = oisCourses.coursesId(courseCode)
        return ""

    def answerCourseEcts(self, courseId):
        """
        Creates an answer for questions about course ects.
        :param courseId: Courses which, were asked for
        :return: an answer
        """
        if len(courseId) == 1:
            json = oisCourses.coursesId(courseId[0])
            title = json["title"]["et"]
            if " " in title:
                return "Kursuse " + title + " maht on " + str(json["credits"]) + " eap."
            return self.synthesizeWord(title, "g").capitalize() + " maht on " + str(json["credits"]) + " eap."

        else:
            response = "Selle nimega on " + str(len(courseId)) + " erinevat kursust."
            json = oisCourses.coursesId(courseId[0])
            response += " " + courseId[0] + " mille maht on " + str(json["credits"]) + " eap"
            for i in courseId[1:-1]:
                json = oisCourses.coursesId(i)
                response += ", " + i + " mille maht on " + str(json["credits"]) + " eap"
            json = oisCourses.coursesId(courseId[-1])
            response += " ja " + courseId[-1] + " mille maht on " + str(json["credits"]) + " eap."
            return response

    def answerCourseCode(self, courseId):
        """
        Creates an answer for questions about course code. like "mis on masinõppe ainekood"
        :param courseId: Courses which, were asked for
        :return: an answer with course code(s)
        """
        if len(courseId) == 1:
            id = courseId.pop()
            json = oisCourses.coursesId(id)
            title = json["title"]["et"]
            if " " in title:
                return "Kursuse " + title + " ainekood on " + id
            return self.synthesizeWord(title, "g").capitalize() + " ainekood on " + id
        else:
            response = "Selle nimega on " + str(len(courseId)) + " erinevat kursust. Nende ainekoodid on "
            for i in courseId[:-2]:
                response += i + ", "
            response += courseId[-2] + " ja "
            return response + courseId[-1] + "."

    def answerCoursePreReqs(self, courseId):
        """
        Creates an answer for question about prerequired courses
        :param courseId: Courses which, were asked for
        :return: An answer, that contains prerequired courses
        """
        if len(courseId) == 1:
            result = "Selle kursuse"
        else:
            result = "Selle nimega on " + str(len(courseId)) + " erinevat kursust."

        for id in courseId:

            json = oisCourses.coursesId(id)
            if "prerequisites" in json["additional_info"]:
                if len(courseId) > 1:
                    result += " Kursuse " + id

                preReqs = json["additional_info"]["prerequisites"]
                if len(preReqs) == 1:
                    result += " eeldusaine on"
                else:
                    result += " eeldusained on"

                for req in preReqs:
                    result += " " + req["code"] + " \"" + req["title"]["et"] + "\""
                    if "alternatives" in req:
                        alternatives = req["alternatives"]
                        for alt in alternatives:
                            result += " või " + alt["code"] + " \"" + alt["title"]["et"] + "\""
            elif len(courseId) > 1:
                result += " Kursusel " + id + " eeldusained puuduvad"
            else:
                return "Sellel kursusel pole eeldusaineid."
        return result + "."

    def sayHello(self):
        greetings = ['Tere!', 'Hello!', 'Ahoi!', 'Tervitus!', 'Ära ehmata! Hommikust sullegi!', '01010100 01100101 01110010 01100101 00001010', 'Tsau tsau!']
        return greetings[randint(0, len(greetings) - 1)]


    def synthesizeWord(self, word, f):
        """
        Changes the word's form without changing it form plural to singular or vice versa
        :param word: word to be formed
        :param f: desired form
        :return: word in desired form
        """
        # need to check if the title is plural or not.
        form = analyze(word)[0]["analysis"][0]["form"]
        return synthesize(word, form[:2] + " " + f, "S")[0]
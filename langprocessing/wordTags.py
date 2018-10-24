from enum import Enum, unique
@unique
class WordTag(Enum):

    sentence = -1

    #misc
    misc = 0
    questionWord = 1
    greeting = 2
    pronoun = 3
    whatIsQuestionSecondWord = 4
    whatIsQuestionTargetWord = 5

    #courses
    courses = 20
    courseID = 21
    ects = 22
    preReqs = 23
    courseCodeMentioned = 24

    #Structure Units
    structureUnits = 40
    structureUnitCode = 41


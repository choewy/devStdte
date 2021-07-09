import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class RealTimeDB:
    def __init__(self, central=None):
        self.central = central

    def __setScheduler__(self):
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())

        creditPath = "src/firebase/scheduler_privacy_key.json"
        databaseURL = "https://stdte-scheduler-2abac-default-rtdb.firebaseio.com/"
        credit = credentials.Certificate(creditPath)
        firebase_admin.initialize_app(credit, {
            "databaseURL": databaseURL
        })

    def __setSurvey__(self):
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())

        creditPath = "src/firebase/survey_privacy_key.json"
        databaseURL = "https://stdte-survey-default-rtdb.asia-southeast1.firebasedatabase.app/"
        credit = credentials.Certificate(creditPath)
        firebase_admin.initialize_app(credit, {
            "databaseURL": databaseURL
        })

    def getUserPwd(self, userId):
        return db.reference(f"user/{userId}/password").get()

    def getUserAuthor(self, userId):
        return db.reference(f"user/{userId}/author").get()

    def getSurveySources(self, clientId):
        surveys = db.reference(f"survey").get()

        surveySources = []

        for uuid in surveys.keys():
            surveySource = surveys[uuid]
            views = {} if "views" not in surveySource.keys() else surveySource["views"]
            answers = {} if "answers" not in surveySource.keys() else surveySource["answers"]
            surveySources.append([
                uuid,
                surveySource["status"],
                surveySource["title"],
                1 if clientId in views.keys() else 0,
                surveySource["createTime"],
                len(answers.keys()),
            ])

        return surveySources

    def getSurveySource(self, uuid):
        return db.reference(f"survey/{uuid}").get()


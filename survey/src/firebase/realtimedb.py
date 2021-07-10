import datetime
import time

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

        if surveys:

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

        else:
            return {}

    def newSurveySource(self, clientId, title, contents):
        uuid = int(time.time())
        now = datetime.datetime.now()
        db.reference(f"survey/{uuid}").update({
            "admin": clientId,
            "answers": {},
            "title": title,
            "contents": contents,
            "createTime": now.strftime("%Y-%m-%d %H:%M"),
            "status": 1,
            "views": {clientId: now.strftime("%Y-%m-%d")}
        })
        return uuid

    def setSurveySource(self, uuid, newSurveySource):
        db.reference(f"survey/{uuid}").update(newSurveySource)

    def getSurveySource(self, uuid):
        return db.reference(f"survey/{uuid}").get()

    def removeSurveySource(self, uuid):
        db.reference(f"survey/{uuid}").delete()

    def setAnswer(self, uuid, answer):
        now = datetime.datetime.now()
        db.reference(f"survey/{uuid}/answers").update(
            {int(time.time()): {
                "answer": answer,
                "uploadTime": now.strftime("%Y-%m-%d %H:%M")
            }}
        )

    def removeAnswer(self, uuid, key):
        db.reference(f"survey/{uuid}/answers/{key}").delete()

    def setSurveyView(self, clientId, uuid):
        now = datetime.datetime.now()
        db.reference(f"survey/{uuid}/views").update(
            {clientId: now.strftime("%Y-%m-%d")}
        )

    def getManualSource(self):
        return db.reference("manual").get()

    def setManualSource(self, newManual):
        db.reference().update({
            "manual": newManual
        })

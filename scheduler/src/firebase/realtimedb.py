import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from calendar import monthrange
import pandas as pd
import datetime
import time
import os


CREDIT_PATH = "src/firebase/privacy_key.json"
DATABASE_URL = "https://stdte-scheduler-2abac-default-rtdb.firebaseio.com/"
TASK_OPTIONS = {
    "0": "회의",
    "1": "교육/훈련",
    "2": "기타업무",
    "3": "사업관리",
    "4": "기술업무"
}


class RealtimeDB:
    def __init__(self, central):
        self.central = central

        credit = credentials.Certificate(CREDIT_PATH)
        firebase_admin.initialize_app(credit, {
            "databaseURL": DATABASE_URL
        })

    def getUserPwd(self, userId):
        return db.reference(f"user/{userId}/password").get()

    def getUserAuthor(self, userId):
        return db.reference(f"user/{userId}/author").get()

    def newUser(self, userId, name, password):
        userData = {
            "name": name,
            "password": password,
            "birth": "",
            "phone": "",
            "science": "",
            "position": "사원",
            "degree": "학사",
            "school": "",
            "major": "",
            "carType": "",
            "carNumber": "",
            "author": "일반",
            "status": "재직",
            "time": {},
            "memo": {},
            "editTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "uuid": int(time.time())
        }

        db.reference(f"user/{userId}").update(userData)

    def getUserTimeYears(self, currentUserId):
        ref = db.reference(f"user/{currentUserId}").get()

        if "time" in ref.keys():
            userYears = [int(year) for year in ref["time"].keys()]
            userYears.sort(reverse=True)
            return [f"{year}" for year in userYears]

        else:
            return [f"{datetime.date.today().year}"]

    def getScheduleUserListSource(self):
        ref = db.reference("user").get()

        userSource = []

        for userId in ref.keys():
            userStatus = ref[userId]["status"]
            userName = ref[userId]["name"]
            editTime = ref[userId]["editTime"]
            uuid = ref[userId]["uuid"]

            userSource.append([userId, userName, userStatus, editTime, uuid])

        return [x[:-1] for x in sorted(userSource, key=lambda x: x[4])]

    def getScheduleTimeColumns(self, currentYear):
        columns = []
        year = int(currentYear)
        for month in range(1, 13):
            for day in range(1, monthrange(year, month)[1]+1):
                day = datetime.date(year, month, day)
                weekday = ["(월)", "(화)", "(수)", "(목)", "(금)", "(토)", "(일)"][day.weekday()]
                dayString = day.strftime('%m/%d')
                columns.append(f"{dayString}{weekday}")

        return columns

    def getScheduleTaskSource(self):
        ref = db.reference("task").get()

        rowSource = []
        taskSource = []

        optionKeys = list(TASK_OPTIONS.keys())

        for taskNumber in ref.keys():
            taskName = ref[taskNumber]["name"]
            taskCode = ref[taskNumber]["code"]
            taskVisible = ref[taskNumber]["visible"]

            if taskVisible:

                if taskNumber == "1000000000" \
                                 "":
                    for optionKey in optionKeys[:3]:
                        taskSource.append([taskNumber, taskName, taskCode, TASK_OPTIONS[optionKey]])
                        rowSource.append((taskNumber, optionKey))

                else:
                    for optionKey in optionKeys[3:]:
                        taskSource.append([taskNumber, taskName, taskCode, TASK_OPTIONS[optionKey]])
                        rowSource.append((taskNumber, optionKey))

        return taskSource, rowSource

    def getScheduleTimeSource(self, currentYear, currentUserId, timeColumns, taskSource, rowSource):
        timeSource = [[0.0 for _ in timeColumns] for _ in taskSource]
        ref = db.reference(f"user/{currentUserId}/time").get()

        columnSource = [column[:-3] for column in timeColumns]

        if ref:
            for key, oldTime in ref[currentYear].items():
                month, day, taskNumber, optionKey = key.split("-")
                if (taskNumber, optionKey) in rowSource:
                    row = rowSource.index((taskNumber, optionKey))
                    col = columnSource.index(f"{month}/{day}")
                    timeSource[row][col] = round((float(oldTime)), 2)

        return pd.DataFrame(data=timeSource, columns=timeColumns)

    def getScheduleMemoSource(self, currentYear, currentUserId, timeColumns):
        ref = db.reference(f"user/{currentUserId}/memo/{currentYear}").get()
        memoSource = [[f"{currentYear}-{column[:-3].replace('/', '-')}", ""] for column in timeColumns]

        if ref:
            columnSource = [column[:-3] for column in timeColumns]

            for key, memo in ref.items():
                col = columnSource.index(f"{key.replace('-', '/')}")
                memoSource[col][1] = memo

        return memoSource

    def __setEditTime__(self):
        editTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        ref = db.reference(f"user/{self.central.clientId}")
        ref.update({"editTime": editTime})

    def setTime(self, currentYear, key, newTime):
        ref = db.reference(f"user/{self.central.clientId}/time/{currentYear}")
        timeSource = ref.get()

        if timeSource:
            if newTime:
                timeSource[key] = newTime
                ref.update(timeSource)
                self.__setEditTime__()

            else:
                db.reference(f"user/{self.central.clientId}/time/{currentYear}/{key}").delete()
                self.__setEditTime__()
        else:
            if newTime:
                timeSource = {f"{key}": newTime}
                ref.update(timeSource)
                self.__setEditTime__()

    def toExcelSchedule(self, savePath, currentUserName, currentYear, taskSource, timeColumns, timeSource) -> None:
        tasks, codes, options = [], [], []

        for uuid, name, code, option in taskSource:
            tasks.append(name)
            codes.append(code)
            options.append(option)

        timeSource.columns = timeColumns
        timeSource["사업명"] = tasks
        timeSource["사업코드"] = codes
        timeSource["구분"] = options
        timeSource = timeSource[["사업명", "사업코드", "구분"] + timeColumns]

        timeSource.to_excel(savePath, index=False, sheet_name=f"시간관리-{currentYear}-{currentUserName}")
        os.startfile(savePath)

    def setMemo(self, currentYear, key, newMemo):
        ref = db.reference(f"user/{self.central.clientId}/memo/{currentYear}")
        memoSource = ref.get()

        if memoSource:
            if newMemo:
                memoSource[key] = newMemo
                ref.update(memoSource)
                self.__setEditTime__()

            else:
                db.reference(f"user/{self.central.clientId}/memo/{currentYear}/{key}").delete()
                self.__setEditTime__()
        else:
            if newMemo:
                memoSource = {f"{key}": newMemo}
                ref.update(memoSource)
                self.__setEditTime__()

    def getUserSource(self):
        ref = db.reference("user")
        users = ref.get()

        tempSource = []

        for userId in users.keys():
            tempSource.append([
                userId,
                users[userId]["uuid"]
            ])

        tempSource = [x[0] for x in sorted(tempSource, key=lambda x: x[-1])]

        userSource = {}

        for userId in tempSource:
            userSource[userId] = users[userId]

        return userSource

    def setUserSource(self, userId, updateSource):
        ref = db.reference(f"user/{userId}")

        userSource = ref.get()

        for key, value in updateSource.items():
            userSource[key] = value

        ref.update(userSource)

    def delUserSource(self, userId):
        db.reference(f"user/{userId}").delete()

    def newTask(self):
        uuid = int(time.time())
        taskSource = {
            "name": "",
            "code": "",
            "type": "",
            "summary": "",
            "order": "",
            "start": datetime.date.today().strftime("%Y-%m-%d"),
            "end": datetime.date.today().strftime("%Y-%m-%d"),
            "totalMonth": 0,
            "keep": datetime.date.today().strftime("%Y-%m-%d"),
            "revenue": 0,
            "admin": "",
            "whole": "",
            "part": "",
            "status": "",
            "visible": 1
        }
        db.reference(f"task/{uuid}").update(taskSource)

    def getTaskSource(self):
        taskSource = db.reference("task").get()
        del taskSource["1000000000"]
        del taskSource["9999999999"]

        return taskSource

    def setTaskSource(self, taskSeq, updateSource):
        ref = db.reference(f"task/{taskSeq}")

        taskSource = ref.get()

        for key, value in updateSource.items():
            taskSource[key] = value

        ref.update(taskSource)

    def delTaskSource(self, uuid):
        db.reference(f"task/{uuid}").delete()

    def getYearList(self):
        ref = db.reference(f"user")

        userSource = ref.get()

        yearList = []

        for userId in userSource.keys():
            for year in list(userSource[userId]["time"].keys()):
                if year not in yearList:
                    yearList.append(year)

        return yearList

    def getTaskList(self):
        ref = db.reference("task")

        taskSource = ref.get()

        taskList = []

        for uuid in taskSource.keys():
            taskList.append([
                uuid,
                taskSource[uuid]["name"],
                taskSource[uuid]["visible"]
            ])

        return taskList

    def getUserList(self):
        ref = db.reference("user")

        userSource = ref.get()

        tempSource = []

        for userId in userSource.keys():
            tempSource.append([
                userId,
                userSource[userId]["uuid"]
            ])

        tempSource = [x[0] for x in sorted(tempSource, key=lambda x: x[-1])]

        userList = []

        for userId in tempSource:
            userList.append([
                userId,
                userSource[userId]["name"],
                userSource[userId]["status"]
            ])

        return userList

    def getTotalYear(self, years, tasks, taskInfo, users):
        ref = db.reference("user")

        userSource = ref.get()

        totalSource = {}

        for year in years:
            totalSource[year] = {uuid: 0.0 for uuid in tasks}

        for userId in users:
            for year in years:
                if year in userSource[userId]["time"].keys():
                    timeSource = userSource[userId]["time"][year]
                    for key, value in timeSource.items():
                        uuid = key.split("-")[2]
                        if uuid in tasks:
                            totalSource[year][uuid] = round(totalSource[year][uuid] + value, 2)

        totalSource = pd.DataFrame(totalSource)
        totalSource["합계"] = [totalSource.loc[x].sum() for x in totalSource.index]
        rowTotals = {"사업명": "합계"}

        for header in totalSource.columns:
            rowTotals[header] = totalSource[header].sum(axis=0)

        totalSource["사업명"] = [taskInfo[x] for x in totalSource.index]
        totalSource = totalSource[["사업명"] + years + ["합계"]]
        totalSource = totalSource.append(rowTotals, ignore_index=True)
        return totalSource

    def toExcelTotalYear(self, savePath, totalSource):
        totalSource.to_excel(savePath, index=False)
        os.startfile(savePath)

    def getTotalUser(self, year, tasks, taskInfo, users, userInfo):
        ref = db.reference("user")

        userSource = ref.get()
        tempSources = {"전체": {}}

        for month in range(1, 13):
            tempSources["전체"][f"{month}월" if month >= 10 else f"0{month}월"] = {uuid: 0.0 for uuid in tasks}

        for userId in users:
            tempSources[userId] = {}

            for month in range(1, 13):
                tempSources[userId][f"{month}월" if month >= 10 else f"0{month}월"] = {uuid: 0.0 for uuid in tasks}

        for userId in users:
            if year in userSource[userId]["time"].keys():
                timeSource = userSource[userId]["time"][year]

                for key, value in timeSource.items():
                    split = key.split("-")
                    month = f"{split[0]}월"
                    uuid = split[2]
                    if uuid in tasks:
                        tempSources["전체"][month][uuid] = round(tempSources["전체"][month][uuid] + value, 2)
                        tempSources[userId][month][uuid] = round(tempSources[userId][month][uuid] + value, 2)

        columns = ["사업명", "01월", "02월", "03월", "1분기", "04월", "05월", "06월", "2분기", "07월", "08월", "09월", "3분기", "10월", "11월", "12월", "4분기", "합계"]

        totalSources = {}

        for key, totalSource in tempSources.items():
            totalSource = pd.DataFrame(totalSource)
            totalSource["합계"] = [totalSource.loc[x].sum() for x in totalSource.index]

            totalSource["1분기"] = [sum(totalSource.loc[x].tolist()[0:3]) for x in totalSource.index]
            totalSource["2분기"] = [sum(totalSource.loc[x].tolist()[3:6]) for x in totalSource.index]
            totalSource["3분기"] = [sum(totalSource.loc[x].tolist()[6:9]) for x in totalSource.index]
            totalSource["4분기"] = [sum(totalSource.loc[x].tolist()[9:12]) for x in totalSource.index]

            rowTotals = {"사업명": "합계"}

            for header in totalSource.columns:
                rowTotals[header] = totalSource[header].sum(axis=0)

            totalSource["사업명"] = [taskInfo[x] for x in totalSource.index]
            totalSource = totalSource[columns]
            totalSource = totalSource.append(rowTotals, ignore_index=True)

            totalSources[userInfo[key]] = totalSource

        return totalSources

    def toExcelTotalUser(self, savePath, totalSources) -> None:
        writer = pd.ExcelWriter(savePath)

        for key, totalSource in totalSources.items():
            totalSource.to_excel(writer, sheet_name=key, index=False)

        writer.save()

        os.startfile(savePath)

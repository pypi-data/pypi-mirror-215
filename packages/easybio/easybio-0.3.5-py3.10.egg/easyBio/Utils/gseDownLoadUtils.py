# -*- coding: utf-8 -*-
# Author: Lei
# Date: 2023-06-08
# Description:
import os

import pandas as pd

from .toolsUtils import sraMd5Cal
from .download import Download
from .netUtils import requestGet


class gsaProject:
    def __init__(self, inputName: str, dirs_path="./") -> None:
        if inputName.startswith("PRJCA"):
            pjurl = f"https://ngdc.cncb.ac.cn/gsa-human/hra/getAjax/searchByPrjAccession?prjAccession={inputName}"
            hra = requestGet(pjurl).json()["listHras"][0]["accession"]
        elif inputName.startswith("HRA"):
            hra = inputName
        self.hra = hra
        self.getStudyId()
        # self.readExcel()
        # self.getAccList()
        print("hra:", hra)
        self.dirs_path = f"{dirs_path}/{inputName}"
        self.raw_path = f"{self.dirs_path}/raw"
        self.fq_path = f"{self.raw_path}/fq"
        if self.raw_path == "":
            self.excel_path = f"{self.hra}.xlsx"
        else:
            self.excel_path = f"{self.raw_path}/{self.hra}.xlsx"
        os.makedirs(self.dirs_path, exist_ok=True)
        os.makedirs(self.raw_path, exist_ok=True)
        os.makedirs(self.fq_path, exist_ok=True)

    def printPro(self) -> None:
        print(self.hra)

    def getStudyId(self) -> str:
        hraurl = f"https://ngdc.cncb.ac.cn/gsa-human/ajaxb/runinstudy?accession={self.hra}&pageSize=10"
        self.studyId = requestGet(hraurl).json()["runViews"][0]["studyId"]
        return self.studyId

    def downLoadRunExcel(self) -> None:
        exurl = f"https://ngdc.cncb.ac.cn/gsa-human/file/exportExcelFile?fileName=/webdb/gsagroup/webApplications/gsa_human_20200410/gsa-human/batchExcel/human/{self.hra}/{self.hra}.xlsx&study_id={self.studyId}&requestFlag=0"
        response = requestGet(exurl)
        with open(self.excel_path, 'wb') as file:
            file.write(response.content)

    def checkExcel(self) -> None:
        if not os.path.exists(self.excel_path):
            self.downLoadRunExcel()

    def readExcel(self) -> pd.DataFrame:
        self.checkExcel()
        self.exceldf = pd.read_excel(self.excel_path, sheet_name='Run')

    def checkDataFrame(self) -> None:
        if not hasattr(self, 'exceldf'):
            self.readExcel()

    def checkmd5Map(self) -> None:
        if not hasattr(self, 'md5List'):
            self.getMd5List()

    def checkfileLinkList(self) -> None:
        if not hasattr(self, 'fileLinkList'):
            self.getFileLinkList()

    def getAccList(self) -> list:
        self.checkDataFrame()
        df = self.exceldf
        AccList = []
        for i in range(len(df)):
            AccList.append(df.iloc[i, 0])
        self.accList = AccList
        return self.accList

    def getMd5List(self) -> map:
        self.checkDataFrame()
        df = self.exceldf
        md5List = {}
        for i in range(len(df)):
            file = df.iloc[i, 4]
            sra_md5 = df.iloc[i, 5]
            md5List[file] = sra_md5
            file = df.iloc[i, 7]
            sra_md5 = df.iloc[i, 8]
            md5List[file] = sra_md5
        self.md5List = md5List
        return self.md5List

    def getFileList(self) -> str:
        self.checkmd5Map()
        fileList = self.md5List.keys()
        self.fileList = fileList
        return self.fileList

    def getFileLinkList(self) -> str:
        self.checkDataFrame()
        df = self.exceldf
        FileLinkList = []
        for i in range(len(df)):
            FileLinkList.append(df.iloc[i, 6])
            FileLinkList.append(df.iloc[i, 9])
        self.fileLinkList = FileLinkList
        return self.fileLinkList

    def downloadCheck(self) -> bool:
        items = os.listdir(self.fq_path)
        fileList = []
        for item in items:
            item_path = os.path.join(self.fq_path, item)
            if os.path.isfile(item_path):
                fileList.append(item)
        return len(fileList) == len(self.fileLinkList)

    def downloadFiles(self, threads=16) -> None:
        self.checkfileLinkList()
        neededDown = self.fileMd5Check()
        while len(neededDown) > 0:
            check = self.downloadCheck()
            while not check:
                for FileLink in self.fileLinkList:
                    fileurl = f"https://download.cncb{FileLink[18:]}"
                    items = FileLink.split("/")
                    fileName = items[len(items)-1]
                    download = Download(fileurl, dirs=self.fq_path, fileName=fileName,
                                        threadNum=threads, limitTime=60000)
                    download.start()
                check = self.downloadCheck()
            neededDown = self.fileMd5Check()

    def fileMd5Check(self) -> list:
        self.checkmd5Map()
        return sraMd5Cal(self.fq_path, self.md5List, self.raw_path)

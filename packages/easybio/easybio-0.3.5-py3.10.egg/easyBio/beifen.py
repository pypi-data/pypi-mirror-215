#   def getAccList(self) -> list:
#        if os.path.exists(self.excel_path):
#             self.downLoadRunExcel()
#         df = pd.read_excel(gsap.excel_path, sheet_name='Run')
#         AccList = []
#         for i in range(len(df)):
#             AccList.append(df.iloc[i, 0])
#         #     file = df.iloc[i, 0]
#         #     sra_md5 = df.iloc[i, 5]
#         #     md5List[file] = sra_md5
#         #     file = df.iloc[i, 7]
#         #     sra_md5 = df.iloc[i, 8]
#         #     md5List[file] = sra_md5
#         # hraurl = f"https://ngdc.cncb.ac.cn/gsa-human/ajaxb/runinstudy?accession={self.hra}&pageSize=10"
#         # totalCount = requestGet(hraurl).json()["totalCount"]
#         # hraurl = f"https://ngdc.cncb.ac.cn/gsa-human/ajaxb/runinstudy?accession={self.hra}&pageSize={totalCount}"
#         # runViews = requestGet(hraurl).json()["runViews"]
#         # AccList = []
#         # for runView in runViews:
#         #     runAcc = runView["runAcc"]
#         #     if not runAcc in AccList:
#         #         AccList.append(runAcc)
#         self.accList = AccList
#         return self.accList

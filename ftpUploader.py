#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
David Basalla

Tool for uploading HTML, CSS and JS to FTP Site
"""

import sys
import os
from ftplib import FTP
import time
import json




from PyQt4.QtCore import *
from PyQt4.QtGui import *

#print dir(QtGui)


class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('FTP Uploader')
        #self.setWindowIcon(QtGui.QIcon('web.png'))        


        #INTERNAL DATA #################

        self.treeViewToggle = True
        self.fileCounter = 0
        self.binPath = '/Users/davidbasalla/Scripts/ftpUploader/'
        self.presetDict = {}
        self.presetDict['presets'] = []


        ################################


        self.initWidgets()
        self.initLayout()

        self.populateFileList()

        self.show()

    def initWidgets(self):
        print 'setting widgets'


        ### Top LEFT ########################################################

        self.frameLeftTop = QFrame()
        self.frameLeftTop.setFrameStyle(QFrame.Box | QFrame.Raised);
        self.frameLeftTop.setLineWidth(1);
        
        self.pathLabel = QLabel('Current Path')
        self.pathEdit = QLineEdit(os.getcwd())
        self.pathEdit.setMinimumWidth(300)        
        self.pathEdit.textChanged.connect(self.populateFileList)
        
        self.pathButton = QPushButton('Open')
        self.pathButton.clicked.connect(self.showDialog)



        self.targetLabel = QLabel('Target')
        self.targetEdit = QLineEdit()
        #self.targetEdit.textChanged.connect(self.populateFileList)


        ### MIDDLE LEFT ########################################################

        self.frameLeftMiddle = QFrame()
        self.frameLeftMiddle.setFrameStyle(QFrame.Box | QFrame.Raised);
        self.frameLeftMiddle.setLineWidth(1);


        self.currentLabel = QLabel('current')
        self.recursiveLabel = QLabel('recursive')

        self.htmlLabel = QLabel('HTML')
        self.cssLabel = QLabel('CSS')
        self.jsLabel = QLabel('JavaScript')
        self.otherEdit = QLineEdit()
        self.otherEdit.editingFinished.connect(self.populateFileList)

        checkboxes = []

        self.checkboxHtmlCur = QCheckBox()
        self.checkboxHtmlCur.setChecked(True)
        checkboxes.append(self.checkboxHtmlCur)

        self.checkboxHtmlRec = QCheckBox()
        checkboxes.append(self.checkboxHtmlRec)

        self.checkboxCssCur = QCheckBox()
        self.checkboxCssCur.setChecked(True)
        checkboxes.append(self.checkboxCssCur)

        self.checkboxCssRec = QCheckBox()
        checkboxes.append(self.checkboxCssRec)

        self.checkboxJsCur = QCheckBox()
        self.checkboxJsCur.setChecked(True)
        checkboxes.append(self.checkboxJsCur)

        self.checkboxJsRec = QCheckBox()
        checkboxes.append(self.checkboxJsRec)

        self.checkboxOtherCur = QCheckBox()
        checkboxes.append(self.checkboxOtherCur)

        self.checkboxOtherRec = QCheckBox()
        checkboxes.append(self.checkboxOtherRec)

        #set connections
        for item in checkboxes:
            item.stateChanged.connect(self.populateFileList)


        self.mirrorCheckbox = QCheckBox("Mirror File Structure")


        ### BOTTOM LEFT ########################################################

        self.frameLeftBottom = QFrame()
        self.frameLeftBottom.setFrameStyle(QFrame.Box | QFrame.Raised);
        self.frameLeftBottom.setLineWidth(1);

        self.hostLabel = QLabel('Host')
        self.usernameLabel = QLabel('Username')
        self.passwordLabel = QLabel('Password')

        self.hostEdit = QLineEdit()
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.rememberCheckbox = QCheckBox("Remember Settings")

        self.loadWebPresetsLabel = QLabel('Load Preset')
        self.loadWebPresetsEdit = QComboBox()

        #populate the combobox
        self.loadPresets()
        self.loadWebPresetsEdit.addItem('None')
        for item in self.presetDict['presets']:
            self.loadWebPresetsEdit.addItem(item['host'])



        self.loadWebPresetsEdit.currentIndexChanged.connect(self.loadPreset)

        ### RIGHT ########################################################

        self.frameRight = QFrame()
        self.frameRight.setFrameStyle(QFrame.Box | QFrame.Raised);
        self.frameRight.setLineWidth(1);

        self.filePreviewBtn1 = QPushButton('List View')
        self.filePreviewBtn1.clicked.connect(lambda: self.setFilePreviewType(False))
        self.filePreviewBtn2 = QPushButton('Tree View')
        self.filePreviewBtn2.clicked.connect(lambda: self.setFilePreviewType(True))

        self.filePreview = QTreeWidget()
        self.filePreview.setHeaderLabels(['File Preview','x'])
        self.filePreview.setColumnCount(1)

        self.fileCountPreview = QLabel('Files to be uploaded: 0')



        ### BOTTOM ########################################################

        self.uploadButton = QPushButton('Upload')
        self.connect(self.uploadButton, 
                     SIGNAL("clicked()"),
                     self.uploadFiles)

        self.cancelButton = QPushButton('Cancel')
        self.connect(self.cancelButton, 
                     SIGNAL("clicked()"),
                     self.deleteLater)

        action1 = QAction('Remove', self.filePreview)
        action1.triggered.connect(self.removeTreeItem)

        self.filePreview.addAction(action1)
        self.filePreview.setContextMenuPolicy(Qt.ActionsContextMenu)



    ##############################################################################################################
    # LAYOUT
    ##############################################################################################################

    def initLayout(self):
                   
        mainLayout = QVBoxLayout()

        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()

        #############################

        leftTopLayout = QGridLayout()
        #leftTopLayout.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        #leftTopLayout.setLineWidth(2)

        leftTopLayout.addWidget(self.currentLabel, 0, 1)
        leftTopLayout.addWidget(self.recursiveLabel, 0, 2)

        leftTopLayout.addWidget(self.htmlLabel, 1, 0)
        leftTopLayout.addWidget(self.checkboxHtmlCur, 1, 1)
        leftTopLayout.addWidget(self.checkboxHtmlRec, 1, 2)

        leftTopLayout.addWidget(self.cssLabel, 2, 0)
        leftTopLayout.addWidget(self.checkboxCssCur, 2, 1)
        leftTopLayout.addWidget(self.checkboxCssRec, 2, 2)

        leftTopLayout.addWidget(self.jsLabel, 3, 0)
        leftTopLayout.addWidget(self.checkboxJsCur, 3, 1)
        leftTopLayout.addWidget(self.checkboxJsRec, 3, 2)

        leftTopLayout.addWidget(self.otherEdit, 4, 0)
        leftTopLayout.addWidget(self.checkboxOtherCur, 4, 1)
        leftTopLayout.addWidget(self.checkboxOtherRec, 4, 2)

        #############################

        leftBottomLayout = QGridLayout()
        
        leftBottomLayout.addWidget(self.hostLabel, 0, 0)
        leftBottomLayout.addWidget(self.hostEdit, 0, 1)

        leftBottomLayout.addWidget(self.usernameLabel, 1, 0)
        leftBottomLayout.addWidget(self.usernameEdit, 1, 1)

        leftBottomLayout.addWidget(self.passwordLabel, 2, 0)
        leftBottomLayout.addWidget(self.passwordEdit, 2, 1)


        pathLayout = QGridLayout()
        pathLayout.addWidget(self.pathLabel, 0, 0)
        pathLayout.addWidget(self.pathEdit, 0 ,1 )
        pathLayout.addWidget(self.pathButton, 0 ,2 )
        pathLayout.addWidget(self.targetLabel, 1, 0)
        pathLayout.addWidget(self.targetEdit, 1, 1)
        self.frameLeftTop.setLayout(pathLayout)
        

        frameLeftMiddleLayout = QVBoxLayout()
        frameLeftMiddleLayout.addLayout(leftTopLayout)
        frameLeftMiddleLayout.addWidget(self.mirrorCheckbox)
        self.frameLeftMiddle.setLayout(frameLeftMiddleLayout)


        presetsLayout = QHBoxLayout()
        presetsLayout.addWidget(self.rememberCheckbox)
        presetsLayout.addStretch(2000)
        presetsLayout.addWidget(self.loadWebPresetsLabel)
        presetsLayout.addWidget(self.loadWebPresetsEdit)


        frameLeftBottomLayout = QVBoxLayout()
        frameLeftBottomLayout.addLayout(leftBottomLayout)
        frameLeftBottomLayout.addLayout(presetsLayout)
        self.frameLeftBottom.setLayout(frameLeftBottomLayout)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.frameLeftTop)
        leftLayout.addSpacing(10)
        leftLayout.addWidget(self.frameLeftMiddle)
        leftLayout.addSpacing(10)
        leftLayout.addWidget(self.frameLeftBottom)


        filePreviewButtonLayout = QHBoxLayout()
        filePreviewButtonLayout.addWidget(self.filePreviewBtn1)
        filePreviewButtonLayout.addWidget(self.filePreviewBtn2)


        rightLayout = QVBoxLayout()
        rightLayout.addLayout(filePreviewButtonLayout)
        rightLayout.addWidget(self.filePreview)
        rightLayout.addWidget(self.fileCountPreview)
        self.frameRight.setLayout(rightLayout)


        topLayout.addLayout(leftLayout)
        topLayout.addSpacing(20)
        topLayout.addWidget(self.frameRight)


        bottomLayout.addStretch(1000)
        bottomLayout.addWidget(self.uploadButton)
        bottomLayout.addWidget(self.cancelButton)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)
 

        self.setLayout(mainLayout)



    def showDialog(self):

        dirName = str(QFileDialog.getExistingDirectory(self, "Select Directory",
                                                       os.getcwd(),
                                                       QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks))
        if dirName:
            self.pathEdit.setText(dirName)



    def populateFileList(self):
        print 'populateFilelist()'

        self.dirDict = self.addDir(str(self.pathEdit.text()))

        print 'FINAL DICT:'
        print self.dirDict

        self.renderFilePreview()



    def addDir(self, directoryPath):
        """ recursive function for populating directory dict """
        print 'RECURSION LOOP - ' + directoryPath

        #print os.walk(directoryPath)
        #print os.listdir(directoryPath)


        for (dirpath, dirnames, filenames) in os.walk(directoryPath):

            #print 'Creating Dict for ' + directoryPath
            dirDict = {}

            dirDict['dirpath'] = os.path.abspath(dirpath)
            dirDict['directories'] = []
            dirDict['filenames'] = self.filterFiles(filenames, dirpath)

            for directory in dirnames:
                dirDict['directories'].append(self.addDir(dirpath + '/' + directory))

            #print 'DICT:'
            #print dirDict

            return dirDict



    def filterFiles(self, filenames, dirpath):
        """filters a list of files by their endings, depending on UI"""

        filelist = []
        
        #determine if in root directory or child directory
        root = False
        if dirpath == str(self.pathEdit.text()):
            root = True
            
        for file in filenames:
            append = False
            
            #HTML
            if self.checkboxHtmlCur.isChecked() and root and file.endswith(".html"):
                append = True
            elif self.checkboxHtmlRec.isChecked() and not root and file.endswith(".html"):
                append = True
                
            #CSS
            if self.checkboxCssCur.isChecked() and root and file.endswith(".css"):
                append = True
            elif self.checkboxCssRec.isChecked() and not root and file.endswith(".css"):
                append = True
                    
            #JavaScript
            if self.checkboxJsCur.isChecked() and root and file.endswith(".js"):
                append = True
            elif self.checkboxJsRec.isChecked() and not root and file.endswith(".js"):
                append = True
                    
            #OTHER
            if self.checkboxOtherCur.isChecked() and root and self.otherEdit.text() and file.endswith(str(self.otherEdit.text())):
                append = True
            elif self.checkboxOtherRec.isChecked() and not root and self.otherEdit.text() and file.endswith(str(self.otherEdit.text())):
                append = True

            ### APPEND THE FILE ###
            if append:
                filelist.append(file)
                
        return filelist


    def setFilePreviewType(self, value):

        self.treeViewToggle = value;
        self.renderFilePreview();



    def setFilePreviewTree(self):
        self.treeViewToggle = True;
        self.renderFilePreview();


    def setFilePreviewList(self):
        self.treeViewToggle = False;
        self.renderFilePreview();


    def renderFilePreview(self):

        self.fileCounter = 0

        print 'renderFilePreview()'
        """ need to change this so as to render complete nested dictionary """

        #clear the list
        self.filePreview.clear()

        if self.treeViewToggle:
            self.renderTree()
        else:
            self.renderList(self.dirDict)

        self.fileCountPreview.setText('Files to be uploaded: ' + str(self.fileCounter))


    def setFilePreviewTree(self):
        self.treeViewToggle = True;
        self.renderFilePreview();

    def setFilePreviewList(self):
        self.treeViewToggle = False;
        self.renderFilePreview();




    def renderTree(self):

        #create root Item
        itemRootDir = QTreeWidgetItem()
        itemRootDir.setText(0, self.dirDict['dirpath'].split('/')[-1] + '/')
        itemRootDir.setForeground(0, QBrush(QColor(175, 175, 175, 255)))

        #start recursion
        self.renderDir( self.dirDict, itemRootDir)

        #add topLevelDir to tree
        self.filePreview.addTopLevelItem(itemRootDir)
        self.filePreview.expandItem(itemRootDir)



    def renderDir(self, dirDict, parentNode):

        for filename in dirDict['filenames']:
            treeItem = QTreeWidgetItem()
            treeItem.setText(0, filename.split('/')[-1])        
            parentNode.addChild(treeItem)
            self.fileCounter += 1

        for dirDict in dirDict['directories']:
            dirItem = QTreeWidgetItem()
            dirItem.setText(0, dirDict['dirpath'].split('/')[-1] + '/')
            dirItem.setForeground(0, QBrush(QColor(175, 175, 175, 255)))

            self.renderDir(dirDict, dirItem)

            parentNode.addChild(dirItem)

            if self.checkboxHtmlRec.isChecked() or self.checkboxCssRec.isChecked() or self.checkboxJsRec.isChecked() or self.checkboxOtherRec.isChecked():
                self.filePreview.expandItem(dirItem)
        

    def renderList(self, dirDict):

        for filename in dirDict['filenames']:
            treeItem = QTreeWidgetItem()
            treeItem.setText(0, filename.split('/')[-1])        
            self.filePreview.addTopLevelItem(treeItem)  
            self.fileCounter += 1

        for directoryDict in dirDict['directories']:

            self.renderList(directoryDict)



    def removeTreeItem(self):
        """ called from context menu, figure out which file to remove! """

        print 'removing list item'
        selectedItem = self.filePreview.currentItem()

        path =  self.getPath(selectedItem) + selectedItem.text(0)

        self.removePathFromDict(path, self.dirDict)


    def getPath(self, item):
        """ recurse through tree to get full path """

        path = ""

        while item.parent():
            path = str(item.parent().text(0)) + path
            item = item.parent()


        origPath = str(self.pathEdit.text()).rstrip(str(self.pathEdit.text()).split('/')[-1])

        return origPath + path

    def removePathFromDict(self, path, dict):
        """traverse dict and remove the path once found """
        print 'removePathFromDict(' + path + ')'

        for file in dict['filenames']:
            if path == (dict['dirpath'] + '/' + file):
                print 'MATCH!'
                dict['filenames'].remove(file)
                break

        for dir in dict['directories']:
            if path == (dir['dirpath'] + '/'):
                print 'MATCH!'
                dict['directories'].remove(dir)
                break
            self.removePathFromDict(path, dir)

        #rerender!
        self.renderFilePreview()
            

    def savePreset(self):
        """ saves current preset to preset file """
        """ if toggle is set """

        if self.rememberCheckbox.isChecked():

            newDict = {'host': str(self.hostEdit.text()),
                       'username': str(self.usernameEdit.text()),
                       'password': str(self.passwordEdit.text())}


            if newDict not in self.presetDict['presets']:

                self.presetDict['presets'].append(newDict)
                
                with open(self.binPath + 'preset.json', 'w') as outfile:
                    json.dump(self.presetDict, outfile)


    def loadPresets(self):
        """ loads automatically at start time """

        json_data=open(self.binPath + 'preset.json')
        self.presetDict = json.load(json_data)
        json_data.close()


    def loadPreset(self, index):
        """ set fields when a preset is selected """

        host = ""
        username = ""
        pwd = ""
        
        if index > 0:
            index = index - 1
            host = self.presetDict['presets'][index]['host']
            username = self.presetDict['presets'][index]['username']
            pwd = self.presetDict['presets'][index]['password']

        self.hostEdit.setText(host)
        self.usernameEdit.setText(username)
        self.passwordEdit.setText(pwd)


    def uploadFiles(self):
        """ function for uploading files, does the connection and uploads all files """

        print 'uploadFiles()'


        ftpConnection = FtpConnect(webhost = str(self.hostEdit.text()),
                                   username = str(self.usernameEdit.text()),
                                   password = str(self.passwordEdit.text()),
                                   targetPath = str(self.targetEdit.text()))

        #save on successful connection
        if ftpConnection.connectStatus:
            self.savePreset()

        """
        ftpConnection = FtpConnect(webhost = 'www.davidbasalla3d.com',
                                   username = 'web250',
                                   password = '6lvrxwnf',
                                   targetPath = 'html')
        """



#######################################################################

class FtpConnect():

    def __init__(self,
                 webhost = None,
                 username = None, 
                 password = None,
                 targetPath = None,
                 callbackFunc = None):

        self.connectStatus = True

        self.callbackFunc = callbackFunc

        self.website = webhost
        self.username = username
        self.password = password
        self.folder = targetPath

        print self.website

        self.lineCounter = 0

        #login to website
        try:
            self.ftp = FTP(self.website)
            self.ftp.login(self.username, self.password)        

            #change dir to targetPath
            self.changeDir(targetPath)

            print 'Successfully connected to %s' % self.website
        except:
            print 'Warning - could not connect to %s' % self.website
            self.connectStatus = False


    def changeDir(self, path):
        self.ftp.cwd(path)


    def callbackFunc2(self,arg):
        print self.lineCounter
        self.lineCounter += 1


    def uploadFile(self, filepath = None, mode = 0, callback = None):

        print '... running ftpUploadFile.uploadFile()...'
        print 'Mode = ' + str(mode)

        if filepath:
            print 'starting upload'
            #self.ftp.cwd(self.folder)
            
            filename = filepath.split('/')[-1]
            print filename

            start = time.time()

            #self.ftp.storlines('STOR ' + self.filename,open(self.filepath,'rb'),self.callbackFunc)
            if mode == 0:
                print 'Running ftpUpload with storbinary'
                self.ftp.storbinary('STOR ' + filename, open(filepath,'rb'), blocksize = 16384, callback = self.callbackFunc)
            else:
                print 'Running ftpUpload with storlines'
                self.ftp.storlines('STOR ' + filename, open(filepath,'rb'), callback = self.callbackFunc)

            self.ftp.close()

            print 'Transfer took %.2f seconds' % (time.time() - start)

            return float(time.time() - start)

            print 'upload complete'
        else:
            print 'Warning - No filename found'
            return 0



    """
    def downloadDirContents(self,path = None):

        filenames = []
        self.ftp.retrlines('NLST', filenames.append)
        print filenames

        for filename in filenames:
            local_filename = os.path.join('C:/PhysioDatenbank/Icons/', filename)
            file = open(local_filename, 'wb')
            self.ftp.retrbinary('RETR '+ filename, file.write)
            file.close()
            print 'file copied!'

        self.ftp.close()
    """
    """
    def downloadLastFile(self,path = None):

        filenames = []
        self.ftp.retrlines('NLST', filenames.append)
        print 'Copying %s' % filenames[-1]

        local_filename = os.path.join(path, filenames[-1])
        file = open(local_filename, 'wb')
        self.ftp.retrbinary('RETR '+ filenames[-1], file.write)
        file.close()
        print 'file copied!'

        self.ftp.close()

        return path + filenames[-1]
    """

    """
    def downloadFile(self, filename = None, systemPath = None):

        print 'Copying %s' % filename

        local_filename = os.path.join(systemPath, filename)
        file = open(local_filename, 'wb')
        self.ftp.retrbinary('RETR '+ filename, file.write)
        file.close()
        print 'file copied!'

        self.ftp.close()

        return local_filename
    """





    def readSiteContents(self):
        fileinfo = []

        #self.ftp.retrlines('NLST', filenames.append)
        self.ftp.retrlines('LIST', fileinfo.append)

        return fileinfo




def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  

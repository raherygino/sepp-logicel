import os

from PyQt5.QtCore import QFile, QIODevice, Qt
from PyQt5.QtWidgets import QFileDialog
from ..models.db.database import Database
from ..models.model.config_model import ConfigModel
from ..models.entity.configuration import Configuration
from ..common.config import cfg
from pathlib import Path
import shutil
from datetime import datetime
from qfluentwidgets import InfoBar, InfoBarPosition

class Function:
    USER_DIR = os.path.expanduser('~')
    def importFile(self, parent, title, fileType:str):
        configModel = ConfigModel()
        countConfig = len(configModel.fetch_all_items())
        directory = self.USER_DIR
        if countConfig != 0:
            directory = configModel.fetch_all_items()[0].directory
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(parent,title, directory,fileType, options=options)
        if fileName:
            splitted = fileName.split("/")
            directory = '/'.join([f'{nDir}' for nDir in splitted[0:len(splitted)-1]])
            if countConfig == 0:
                configModel.create(Configuration(0, directory, ""))
            else:
                configModel.update_item(1, directory=directory)
        return fileName


    def copyFile(self, file_path, destination_path):
        if not file_path:
            return

        #destination_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*);;Text Files (*.txt)")

        if destination_path:
            source_file = QFile(file_path)
            destination_file = QFile(destination_path)

            if source_file.open(QIODevice.ReadOnly) and destination_file.open(QIODevice.WriteOnly):
                total_size = source_file.size()
                chunk_size = 1024

                data = source_file.read(chunk_size)
                written_size = 0

                while data:
                    destination_file.write(data)
                    written_size += len(data)

                    progress = int((written_size / total_size) * 100)
                    #self.progress_bar.setValue(progress)

                    data = source_file.read(chunk_size)

                source_file.close()
                destination_file.close()

                #self.progress_bar.setValue(100)

    def copyFileToFolderApp(self, file_path, **kwargs) -> str:
        folderApp = f'{cfg.get(cfg.downloadFolder)}'
        if "folder" in kwargs:
            folderApp += f"/{kwargs.get('folder').replace(' ', '-')}"
        path = Path(folderApp)
        path.mkdir(parents=True, exist_ok=True)
        new_file_path = ""
        if file_path != "":
            splitted = file_path.split("/")
            nameF = kwargs.get('name') if "name" in kwargs else "icon"
            new_file = f'{nameF}.{splitted[len(splitted) - 1].split(".")[1]}'
            new_file_path = f'{folderApp}/{new_file}'
            self.copyFile(file_path, new_file_path)
        return new_file_path

    def deleteFolderEnv(self, name: str):
        folderApp = f'{cfg.get(cfg.downloadFolder)}/{name.replace(" ", "-")}'
        try:
            shutil.rmtree(folderApp)
        except OSError as e:
            print(f"Error while deleting: {e.filename} - {e.strerror}")

    def fileExist(self, path:str) -> bool:
        return os.path.exists(path)

    def deleteFolder(self, name):
        try:
            shutil.rmtree(name)
        except OSError as e:
            print(f"Error while deleting: {e.filename} - {e.strerror}")

    def deleteFile(self, file_path):
        if self.fileExist(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}")
    def folderOfFile(self, fileName):
        parsN = fileName.split("/")
        folder = ""
        for i, lnk in enumerate(parsN):
            if i < len(parsN) - 2:
                folder += f'{lnk}/'
            if i == len(parsN) - 2:
                folder += f'{lnk}'
        return folder
    def randomName(self) -> str:
        currentTime = datetime.now().time()
        return str(currentTime).replace(":", "").replace(".", "")
    
    
    def toastSuccess(self, title:str, content:str, parent):
        
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=parent
        )

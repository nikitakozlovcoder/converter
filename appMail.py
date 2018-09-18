import datetime
import os
import shutil


class ConvertFile:
    pathFolder = ""

    def __init__(self, pathFolder):
        self.pathFolder = pathFolder

    def __search_files(self):
        files = os.listdir(self.pathFolder)
        files_list = []

        for file in files:
            filename, file_extension = os.path.splitext(self.pathFolder + '/' + file)

            if file_extension == '.txt':
                files_list.append(file)
        return files_list

    def __count_rows(self, file):
        f = open(self.pathFolder + '/' + file)
        rows = 0
        for row in f:
            rows += 1
        f.close()
        return rows

    def __parse_files(self, files_list):

        parsed_files = []

        for file in files_list:
           # rows_count = self.__count_rows(file)
            f = open(self.pathFolder + '/' + file)
            file_rows = []
            i = 1
            user_input = 'y'
            for line in f:

                col = line.split(';')
                try:
                    col.remove('\n')
                except ValueError:
                    pass
                if len(col) < 6:
                    #if i < rows_count:
                    user_input = input("В файле {} строка {} будет пропущена, обработать файл? y - да.".format(file, i))
                    if user_input != 'y':
                        f.close()
                        break
                try:
                    col = ';'.join([col[0], col[1], col[5].replace('.', ',')])
                    file_rows.append(col)
                except IndexError:
                    pass
                i += 1

            if user_input != 'y':
                parsed_files.append('')
                continue
            parsed_files.append(file_rows)
            f.close()
            #print(file_rows)

        return parsed_files

    def __made_dir(self):
        today = datetime.date.today()
        #print(today.isoformat())
        path = self.pathFolder + '/' + today.isoformat()
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        try:
            os.mkdir(path + '/исправленные/')
        except FileExistsError:
            pass
        return path

    def __write_file(self, files_list, files):
        #print(files[1])
        i = 0
        for file in files_list:
            #print(i)
            #print(file)
            path = self.__made_dir()

            if os.path.exists(path + '/исправленные/' + file):
                print('Файл ' + path + '/исправленные/' + file + ' уже существует, файл не был изменен.')

            else:
                if files[i] != '':

                    f = open(path + '/исправленные/' + file, 'w+')

                    for item in files[i]:
                        #print(item)
                        f.write(item + '\n')
                    f.write('конец;;')
                    f.close()
                    shutil.copyfile(self.pathFolder + '/' + file, path + '/' + file)
                    base = os.path.splitext(path + '/' + file)[0]
                    try:
                        os.rename(path + '/' + file, base + ".csv")
                    except FileExistsError:
                        print('Не получилось изменить формат файла, файл с таким именем уже существует. ' + file)
                    os.remove(self.pathFolder + '/' + file)
            i += 1

            #print(self.pathFolder + '/' + file, path + '/исправленные/' + file)
    def run(self):
        files_list = self.__search_files()
        parsed_files = self.__parse_files(files_list)
        self.__write_file(files_list, parsed_files)
        input('Выполнение окончено')


Converter = ConvertFile('D:\excelConverterMail')
Converter.run()

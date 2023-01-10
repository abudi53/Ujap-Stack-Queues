import datetime
import logging
import pickle

import helper

config = helper.read_config()
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(config["Logger"]["LogFilePath"])

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def guardarObjeto(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
        logger.error("Exception occurred", exc_info=True)

def cargarObjeto(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)
        logger.error("Exception occurred", exc_info=True)

class Estructura():
    def __init__(self, path) -> None:
        self.path = path
        self.cDir = Directorio("C:", self.path)
        self.pathlist = [self.cDir]
        self.currentDir = self.cDir
        self.pathlist = cargarObjeto("data.pickle")
        while True:
            try:
                guardarObjeto(self.pathlist)         
                self.currentDir = self.pathlist[-1]
                self.path = self.currentDir.path
                orden = input(self.currentDir.path + "> ")
                logger.info(orden)
                if orden[:2] == "cd": #******CD*********
                    self.changeDir(orden[2:])
                elif orden[:5] == "mkdir": #**********MKDIR*********
                    check = 0
                    for i in self.currentDir.directorios:
                        if i.nombre == orden[6:]:
                            check = 1
                    if check == 0:
                        self.currentDir.directorios.append(self.mkDir(orden[6:]))
                    else:
                        print('Ya existe un directorio con el nombre "' + orden[6:] + '"')

                elif orden[:3] == "dir": #**********DIR*********
                    self.listDir(self.currentDir)
                elif orden[:5] == "rmdir": #**********RMDIR*********
                    self.rmDir(orden[6:])
                elif orden[:6] == "rename": #**********RENAME*********
                    try:
                        self.rename(orden.split(" ")[1], orden.split(" ")[2])
                    except IndexError:
                        print("Por favor, indique el nombre viejo y el nuevo.")
                        logger.exception("Exception occurred")
                        
                elif orden[:6] == "create": #**********CREATE*********
                    check = 0
                    for i in self.currentDir.directorios:
                        if i.tipo != "<DIR>":
                            if i.nombre == orden[7:]:
                                check = 1
                    if check == 0:
                        self.create(orden[7:])    
                    else:
                        print('Ya existe un fichero con el nombre "' + orden[6:] + '"')
                elif orden[:6] == "remove": #**********REMOVE*********:
                    self.remove(orden[7:])
                elif orden[:4] == "open": #**********OPEN*********:
                    self.open(orden[5:])
                    input()
                elif orden[:3] == "log": #**********LOG*********:
                    file = open(config["AppSettings"]["pathlog"], "r")
                    print(file.read())
                elif orden[:6] == "config": #**********CONFIG*********:
                    file = open(config["AppSettings"]["pathconfig"], "r")
                    print(file.read())
                elif orden[:4] == "help": #**********HELP*********:
                    file = open(config["AppSettings"]["pathhelp"], "r")
                    print(file.read())
                else:
                    print('"'+ orden + '" ' + 'no se reconoce como un comando interno o externo, programa o archivo por lotes ejecutable. \n')
            except Exception as e:
                logger.exception("Exception occurred")
    #vvvvvvvvvvvvvvDIRECTORIOSvvvvvvvvvvvvv
                
    def changeDir(self, orden):
        try:
            nombre = orden[1:]
            if orden == "..":
                if len(self.pathlist) > 1:
                    self.pathlist.pop()
        
                
            elif self.currentDir.directorios == []:
                print('No existe ningun directorio con el nombre "' + nombre + '"')
                
            else:
                check = 0
                for i in self.currentDir.directorios:
                    if i.nombre == nombre:
                        self.pathlist.append(i)
                        check = 1
                if check == 0:
                    print('No existe ningun directorio con el nombre "' + nombre + '"')
        except Exception as e:
            logger.exception("Exception occurred")
                    
    def mkDir(self, nombre):
        try:
            return Directorio(nombre, self.path + "\\" + nombre)
        except Exception as e:
            logger.exception("Exception occurred")
            
    def listDir(self, dir):
        try:
            for i in dir.directorios:
                print(("{:11} {:11} {:8} {:15}").format(i.fCreacion, i.hCreacion, i.tipo, i.nombre))
        except Exception as e:
            logger.exception("Exception occurred")
            
    def rmDir(self, dir):
        try:
            ch = 0
            for i in self.currentDir.directorios:
                if dir == i.nombre:
                    ch = 1
                    self.currentDir.directorios.remove(i)
            if ch == 0:
                print('No existe ningun directorio con el nombre "' + dir + '"')

        except Exception as e:
            logger.exception("Exception occurred")
    
    def rename(self, old, new):
        try:
            if self.currentDir.directorios == []:
                print('No existe ningun directorio con el nombre "' + old + '"')

            for i in self.currentDir.directorios:
                if old == i.nombre:
                    setattr(i, "nombre", new)
                    setattr(i, "path", self.path + "\\" + new)
                else:
                    print('No existe ningun directorio con el nombre "' + old + '"')
        except Exception as e:
            logger.exception("Exception occurred")
                
    #^^^^^^^^^^^^^^^^DIRECTORIOS^^^^^^^^^^^^^^^^
    #vvvvvvvvvvvvvvvvvFICHEROSvvvvvvvvvvvvvvvvvv
    def create(self, args): # PERMITE CREAR Y AGREGAR TEXTO DIRECTAMENTE O SIMPLEMENTE CREAR
        if len(args.split(" ")) == 1:
            try:
                self.currentDir.directorios.append(Fichero(args, args.split(".")[1]))
            except IndexError:
                print("Por favor indique una extension del archivo")
        elif len(args.split(" ")) > 1:
            self.currentDir.directorios.append(Fichero(args.split(" ")[0], args.split(" ")[0].split(".")[1]))
            setattr(self.currentDir.directorios[-1], "contenido", args.split(" ", 1)[1])
            
    def remove(self, arg):
        if arg == "":
            print("Por favor, indique el nombre del archivo")
        else:
            check = 0
            for i in self.currentDir.directorios:
                if i.tipo != "<DIR>":
                    if arg == i.nombre:
                        self.currentDir.directorios.remove(i)
                        check = 1
            if check == 0:
                print('No existe ningun fichero con el nombre "' + arg + '"')
                        
    def open(self, arg):
        if arg == "":
            print("Por favor, indique el nombre del archivo")
        else:
            check = 0
            for i in self.currentDir.directorios:
                if i.tipo != "<DIR>":
                    if i.nombre == arg:
                        print(i.contenido)
                        check = 1
            if check == 0:
                print('No existe un fichero con el nombre "' + arg + '"')

    #^^^^^^^^^^^^^^^^^^FICHEROS^^^^^^^^^^^^^^^^

        



class Directorio():
    def __init__(self, nombre, path) -> None:
        self.nombre = nombre
        self.path = path
        self.fCreacion = datetime.datetime.now().strftime("%x")
        self.hCreacion = datetime.datetime.now().strftime("%X")
        self.tipo = "<DIR>"
        self.directorios = []
        
class Fichero():
    def __init__(self, nombre, tipo) -> None:
        self.nombre = nombre
        self.tipo = tipo # Extension
        self.contenido = ""
        self.fCreacion = datetime.datetime.now().strftime("%x")
        self.hCreacion = datetime.datetime.now().strftime("%X")
        
        
path = config["AppSettings"]["path"]
usename = config["AppSettings"]["username"]
main = Estructura(path)
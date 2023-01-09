import datetime
import pickle

def guardarObjeto(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

def cargarObjeto(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

class Estructura():
    def __init__(self) -> None:
        self.path = "C:"
        self.cDir = Directorio("C:", self.path)
        self.pathlist = [self.cDir]
        self.currentDir = self.cDir
        self.pathlist = cargarObjeto("data.pickle")
        while True:
            guardarObjeto(self.pathlist)         
            self.currentDir = self.pathlist[-1]
            self.path = self.currentDir.path
            orden = input(self.currentDir.path + "> ")
            if orden[:2] == "cd": #******CD*********
                self.changeDir(orden[2:])
            elif orden[:5] == "mkdir": #**********MKDIR*********
                self.currentDir.directorios.append(self.mkDir(orden[5:]))
            elif orden[:3] == "dir": #**********DIR*********
                self.listDir(self.currentDir)
            elif orden[:5] == "rmdir": #**********RMDIR*********
                self.rmDir(orden[6:])
            elif orden[:6] == "rename": #**********RENAME*********
                try:
                    self.rename(orden.split(" ")[1], orden.split(" ")[2])
                except IndexError:
                    print("Por favor, indique el nombre viejo y el nuevo.")
                    
            elif orden[:6] == "create": #**********CREATE*********
                self.create(orden[7:])
            elif orden[:6] == "remove": #**********REMOVE*********:
                self.remove(orden[7:])
            elif orden[:4] == "open": #**********OPEN*********:
                self.open(orden[5:])
            else:
                print('"'+ orden + '" ' + 'no se reconoce como un comando interno o externo, programa o archivo por lotes ejecutable. \n')

    #****************DIRECTORIOS*************
                
    def changeDir(self, orden):
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
                    
    def mkDir(self, nombre):
        return Directorio(nombre[1:], self.path + "\\" + nombre[1:])
    
    def listDir(self, dir):
        for i in dir.directorios:
            print(("{:11} {:11} {:8} {:15}").format(i.fCreacion, i.hCreacion, i.tipo, i.nombre))
            
    def rmDir(self, dir):
        for i in self.currentDir.directorios:
            if dir == i.nombre:
                self.currentDir.directorios.remove(i)
            else:
                print('No existe ningun directorio con el nombre "' + dir + '"')
    
    def rename(self, old, new):
        if self.currentDir.directorios == []:
            print('No existe ningun directorio con el nombre "' + old + '"')

        for i in self.currentDir.directorios:
            if old == i.nombre:
                setattr(i, "nombre", new)
                setattr(i, "path", self.path + "\\" + new)
            else:
                print('No existe ningun directorio con el nombre "' + old + '"')
                
    #****************DIRECTORIOS*************
    #****************FICHEROS****************
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
            for i in self.currentDir.directorios:
                if i.tipo != "<DIR>":
                    if arg == i.nombre:
                        self.currentDir.directorios.remove(i)
                    else:
                        print('No existe ningun fichero con el nombre "' + arg + '"')
                        
    def open(self, arg):
        if arg == "":
            print("Por favor, indique el nombre del archivo")
        else:
            for i in self.currentDir.directorios:
                if i.tipo != "<DIR>":
                    if arg == i.nombre:
                        print(i.contenido)
                        input()
                    else:
                        print("No se ha encontrado el archivo. Por favor, vuelva a intentarlo.")
                else:
                    print("No se ha encontrado el archivo. Por favor, vuelva a intentarlo.")

    
    
    
    
    
    
    #****************FICHEROS****************

        



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
        
        
main = Estructura()
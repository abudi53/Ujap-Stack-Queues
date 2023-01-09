import datetime

class Estructura():
    def __init__(self) -> None:
        self.path = "C:"
        self.cDir = Directorio("C:", self.path)
        self.pathlist = [self.cDir]
        self.currentDir = self.cDir
        while True:
            self.currentDir = self.pathlist[-1]
            self.path = self.currentDir.path
            #print("CURRENT IS" + self.currentDir.nombre)
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
                self.rename(orden.split(" ")[1], orden.split(" ")[2])
            else:
                print('"'+ orden + '" ' + 'no se reconoce como un comando interno o externo, programa o archivo por lotes ejecutable. \n')
                
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
        for i in self.currentDir.directorios:
            if old == i.nombre:
                setattr(i, "nombre", new)
                setattr(i, "path", self.path + "\\" + new)



class Directorio():
    def __init__(self, nombre, path) -> None:
        self.nombre = nombre
        self.path = path
        self.fCreacion = datetime.datetime.now().strftime("%x")
        self.hCreacion = datetime.datetime.now().strftime("%X")
        self.tipo = "<DIR>"
        self.directorios = []
        
        
print(datetime.datetime.now().strftime("%x"))
main = Estructura()
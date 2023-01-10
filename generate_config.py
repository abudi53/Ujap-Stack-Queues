import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("AppSettings")
# ADD SETTINGS TO SECTION
config_file.set("AppSettings", "path", "C")
config_file.set("AppSettings", "userName", "Abudi")
config_file.set("AppSettings", "pathLog", "log/app.log")
config_file.set("AppSettings", "pathconfig", "config.ini")
config_file.set("AppSettings", "pathhelp", "help.txt")


config_file["Logger"]={
        "LogFilePath":"log/app.log",
        "LogLevel" : "Info"
        }

# SAVE CONFIG FILE
with open(r"config.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'config.ini' created")

# PRINT FILE CONTENT
read_file = open("config.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()
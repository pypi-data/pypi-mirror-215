class config(object):
    """Работа с конфигами VCFG"""
    def __init__(self, file):
        super(Configs, self).__init__()
        self.file = file
    
    def get(self, name):
        with open(self.file, "r+") as cfg:
            for i in cfg.readlines():
                if i.split("=")[0] == name:
                    return str(i.split("=")[1].strip()[1 : -1].strip())
        return None
    
    def set(self, name, text):
        with open(self.file, "r+") as cfg:
            lines = cfg.readlines()
            for i in range(len(lines)):
                if lines[i].split("=")[0] == name:
                    lines[i] = name + "=" + "\"" + text + "\"" + "\n"
                    cfg.seek(0)
                    cfg.writelines(lines)
                    return True
        return False
    
    def new(self, name, text):
        try:
            with open(self.file, "a") as cfg:
                cfg.write("\n" + name + "=" + "\""+text+"\"".strip())
                return True
        except:
            return False

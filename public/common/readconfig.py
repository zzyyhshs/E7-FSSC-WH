#coding=utf-8
__author__ = '崔畅'
import configparser
import codecs

class ReadConfig:
    """
    专门读取配置文件的，.ini文件格式
    """
    configpath = ""
    def __init__(self, filename):
        # configpath = os.path.join(prjDir,filename)
        self.configpath = filename
        # print(configpath)
        fd =  open(self.configpath,encoding="utf-8")
        data = fd.read()
        # remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            files = codecs.open(self.configpath, "w")
            files.write(data)
            files.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(self.configpath, encoding='utf-8')

    def getValue(self, env, name):
        """
        [projectConfig]
        project_path=E:/Python-Project/UItestframework
        :param env:[projectConfig]
        :param name:project_path
        :return:E:/Python-Project/UItestframework
        """
        return self.cf.get(env,name)

    def setValue(self,env,name,vlaue):
        if not self.cf.has_section(env):#看是否存在该Section，不存在则创建
            self.cf.add_section(env)
        self.cf.set(env,name,vlaue)
        self.cf.write(open(self.configpath, "w"))

if __name__ == '__main__':
    config= ReadConfig('modelConfig.ini')
    print(config.getValue("Modular","modular"))
    config.setValue("Modulars","modular","aa")
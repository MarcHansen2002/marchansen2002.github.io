import os

def ScriptDir():
    return os.path.dirname(os.path.abspath(__file__))
    
def SrcDir():
    return os.path.join(ScriptDir(), "src")
    
def OutputDir():
    return os.path.join(ScriptDir(), "docs")

def TemplatesDir():
    return os.path.join(SrcDir(), "Templates")
    
def YamlDir():
    return os.path.join(SrcDir(), "Data")
    
def CSSDir():
    return os.path.join(SrcDir(), "CSS")
    
def JSDir():
    return os.path.join(SrcDir(), "Scripts")

def GetTemplate(template):
    return os.path.join(TemplatesDir(), template)

def BuildDir(path):
    rel = os.path.relpath(os.path.dirname(path), YamlDir())
    output = os.path.join(OutputDir(), "html", rel)
    os.makedirs(output, exist_ok=True)
    return output
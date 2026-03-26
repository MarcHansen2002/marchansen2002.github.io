import yaml
import os
from pygments import highlight
from pygments.lexers import CSharpLexer
from pygments.formatters import HtmlFormatter

import Paths
import Utils
    
def IndexAbout(html, cls, search):
    if search in cls:
        cls = cls[search]
        main = cls.get("main", "")
        sub = cls.get("sub", "")
        
        htmlStr = f"""\
                        <h2>About</h2>
                        <p>{main}</p>
                        <p>{sub}</p>
"""
        return html.replace("@@INDEX_ABOUT@@", htmlStr)
    return html

def GenerateProjectCard(yaml, folder, tabs = 0):
    if folder == "":
        htmlStr = """<div class="card">\n"""
    else:
        htmlStr = f"""<div class="card" data-folder="{folder}">\n"""
        
    name = yaml.get("title", "")
    description = yaml.get("description", "")
    link = yaml.get("link", "")
    
    htmlStr +=f"""\
{Utils.Tabs(tabs)}<h3>{name}</h3>
{Utils.Tabs(tabs)}<p>{description}</p>
{Utils.Tabs(tabs)}<a href="{link}">View Project -></a>
{Utils.Tabs(tabs-1)}</div>
"""
    return htmlStr

def IndexProjects(html, cls, search):
    if search in cls:
        cls = cls[search]
        yaml = Utils.ReadYaml(os.path.join(Paths.YamlDir(), "projects.yaml"))
        if yaml != "":
            yaml = yaml["projects"]
            pinned = cls["pinned"]
            pinnedTitle = pinned.get("title", "")

            htmlStr = f"""\
                        <h2>Projects</h2>
                        <div class="cards base-projects">
                            <h3>{pinnedTitle}</h3>
"""
            
            # LOAD PINNED PROJECTS
            pinnedProjects = pinned.get("projects", [])
            for pinnedProject in pinnedProjects:
                htmlStr += f"{Utils.Tabs(7)}"
                htmlStr += GenerateProjectCard(yaml[pinnedProject], "", 8)
            
            htmlStr += f"""
                            <h3>More</h3>
                        </div>
                        
                        <div class="cards project-folders">
"""
        
            # LOAD BUTTON CATAGORIES
            catagoryList = cls.get("catagories", {})
            for catagory, data in catagoryList.items():
                catName = data.get("title", "")
                catDesc = data.get("description", "")
                
                htmlStr += f"""\
                            <div class="card folder-btn" data-folder="{catagory}">
                                <h3>{catName}</h3>
                                <p>{catDesc}</p>
                                <a>View Projects -></a>
                            </div>
"""
                
            htmlStr += """\
                        </div>
                        <div class="folder-panel">
                            <button class="back-btn"><h3><- Back</h3></button>
                            <div class ="cards folder-cards">
"""
           
            for catagory, data in catagoryList.items():
                catName = data.get("title", "")
                projects = data.get("projects", [])
                htmlStr += f"""\
                                <!-- {catagory} -->
                                <div class="folder" data-folder="{catagory}">
                                    <h3 data-folder="{catagory}">{catName}</h3>
"""
                for project in projects:
                    htmlStr += f"{Utils.Tabs(9)}"
                    htmlStr += GenerateProjectCard(yaml[project], catagory, 10)
                htmlStr += """\
                                </div>
"""
                    
            htmlStr += """\
                            </div>
                        </div>
"""
            
            return html.replace("@@INDEX_PROJECTS@@", htmlStr)
            
        return html    
    return html

def IndexSkills(html, cls, search):
    if search in cls:
        htmlStr = """\
                        <h2>Skills</h2>
                        <ul class="skills">
"""
        
        skills = cls.get("skills", [])
        for skill in skills:
            htmlStr += f"""\
                            <li>{skill}</li>
"""
            
        htmlStr += """\
                        </ul>
"""
        return html.replace("@@INDEX_SKILLS@@", htmlStr)
    return html
    
def IndexExperience(html, cls, search):
    if search in cls:
        
        yaml = Utils.ReadYaml(os.path.join(Paths.YamlDir(), "experience.yaml"))
        if yaml != "":
            htmlStr = """\
                        <h2>Education & Experience</h2>
                        <div class = "timeline">
                            <br>
"""
            experiences = yaml.get("experience", {})
            for experience, data in experiences.items():
                name = data.get("name", "")
                
                dates = data["date"]
                startDate = dates.get("start", "")
                endDate = dates.get("end", "")
                
                description = data.get("description", "")
                
                htmlStr += f"""\
                            <div class= "timeline-item">
                                <div class = "timeline-header">
                                    <h3>{name}</h3>
                                    <span>{startDate} - {endDate}</span>
                                    <p class = "subtitle">{description}</p>
                                </div>
                                <ul>
"""
                
                responsibilities = data.get("responsibilities", [])
                for responsibility in responsibilities:
                    htmlStr += f"""\
                                    <li>{responsibility}</li>
"""
                htmlStr += """\
                                </ul>
                            </div>
                            <br>
"""
                
            htmlStr += """\
                        </div>
"""
            return html.replace("@@INDEX_EXPERIENCE@@", htmlStr)
        return html
    return html

def IndexContact(html, cls, search):
    if search in cls:
        
        htmlStr = """\
                        <h2>Contact</h2>
                        <p>
"""
        
        contacts = cls.get("contact", {})
        for key, keyInfo in contacts.items():
            title = keyInfo.get("title", "")
            link = keyInfo.get("link", "")
            linkDisplay = keyInfo.get("linkDisplay", "")
            
            if link == "":
                htmlStr += f"""\
                            {title}: {linkDisplay}
"""
            else:
                htmlStr += f"""\
                            {title}: 
                            <a href="{link}" target="_blank">
                            {linkDisplay}
                            </a>
                            <br><br>
"""
        
        htmlStr += """\
                        </p>
"""
        return html.replace("@@INDEX_CONTACT@@", htmlStr)
    return html
    
def BuildIndex(yamlFile):
    filename = os.path.basename(yamlFile)
    data = Utils.ReadYaml(yamlFile)
    # READ TEMPLATE
    with open(Paths.GetTemplate("IndexTemplate.html.src"), encoding="utf-8") as f:
        template = f.read()
        
    # Generate File Paths
    rel_path = os.path.relpath(yamlFile, Paths.YamlDir())
    rel_path = os.path.splitext(rel_path)[0] + ".html"

    output_path = os.path.join(Paths.OutputDir(), rel_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html = template
    cls = data["index"]
   
    html = IndexAbout(html, cls, "about")
    html = IndexProjects(html, cls, "projects")
    html = IndexSkills(html, cls, "skills")
    html = IndexExperience(html, cls, "experience")
    html = IndexContact(html, cls, "contact")
   
    html = Utils.CleanUpHtml(html)
    
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(html)
    
#------------------------------------

# MAIN

# Ensure output directory exists
os.makedirs(Paths.OutputDir(), exist_ok=True)

full_path = os.path.join(Paths.YamlDir(), "Index.yaml")
BuildIndex(full_path)
    
#------------------------------------
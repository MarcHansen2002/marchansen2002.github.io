import yaml
import os
from pygments import highlight
from pygments.lexers import CSharpLexer
from pygments.formatters import HtmlFormatter

import Paths
import Utils

def InjectStyles(html):
    htmlStr = """\
        <link rel="stylesheet" href="../CSS/style.css">
        <link rel="stylesheet" href="../CSS/project.css"> 
        <link rel="stylesheet" href="../CSS/style.css">
        <script defer src="../Scripts/particles.js"></script>
        <link rel="stylesheet" href="../CSS/project.css">
"""
    return html.replace("@@styles@@", htmlStr)

def ProjectTitle(html, cls, search):
    if search in cls:
        htmlStr = Utils.GetYaml(cls, search)
        return html.replace("@@project_title@@", htmlStr)
    return html

def ProjectSubtitle(html, cls, search):
    if search in cls:
        htmlStr = f"""\
                        {Utils.GetYaml(cls, search)}
"""
        return html.replace("@@project_subtitle@@", htmlStr)
    return html
def ProjectOverview(html, cls, search):
    if search in cls:
        htmlStr = f"""\
            <section class = "section">
                <h2>Overview</h2>
                <p>
                {Utils.GetYaml(cls, search)}
                </p>
            </section>
"""
        return html.replace("@@project_overview@@", htmlStr)
    return html

def ProjectFeatureList(html, cls, search):
    if search in cls:
        htmlStr = """\
            <section class = "section">
                <h2>Key Features</h2>
                <ul class="feature-list">
"""
        # Generate List
        features = cls.get(search, [])
        for info in features:
            htmlStr += f"""\
                    <li>{info}</li>
"""
        
        htmlStr += """\
                </ul>
            </section>
"""
        return html.replace("@@project_featurelist@@", htmlStr)
    return html
    
def ProjectTechList(html, cls, search):
    if search in cls:
        htmlStr = """\
            <section class = "section">
                <h2>Technologies Used</h2>
                <div class = "tech-list">
"""
        
        # Generate List
        features = cls.get(search, [])
        for info in features:
            htmlStr += f"""\
                    <span>{info}</span>
"""
        
        htmlStr += """\
                </div>
            </section>
"""
        return html.replace("@@project_techlist@@", htmlStr)
    return html
    
def ProjectScreenshots(html, cls, search):
    if search in cls:
        htmlStr = """\
            <section class = "section">
                <h2>Screenshots</h2>
                <div class = "image-grid">
"""
        
        # Generate List
        features = cls.get(search, [])
        for info in features:
            htmlStr += f"""\
                    <img src='../Images/{info}'>
"""
        
        htmlStr += """\
                </div>
            </section>
"""
        return html.replace("@@project_screenshots@@", htmlStr)
    return html
    
def ProjectArchitecture(html, cls, search):
    if search in cls:
        htmlStr = f"""\
            <section class = "section">
                <h2>Architecture</h2>
                <p>
                {Utils.GetYaml(cls, search)}
                </p>
            </section>
"""
        return html.replace("@@project_architecture@@", htmlStr)
    return html
    
def ProjectChallenges(html, cls, search):
    if search in cls:
        htmlStr = f"""
            <section class = "section">
                <h2>Challenges & Solutions</h2>
                <p>
                {Utils.GetYaml(cls, search)}
                </p>
            </section>
"""
        return html.replace("@@project_challenges@@", htmlStr)
    return html
    
def ProjectLearned(html, cls, search):
    if search in cls:
        htmlStr = f"""\
            <section class = "section">
                <h2>What I learned</h2>
                <p>
                {Utils.GetYaml(cls, search)}
                </p>
            </section>
"""
        return html.replace("@@project_learned@@", htmlStr)
    return html
    
def ProjectLinks(html, cls, search):
    if search in cls:
        htmlStr = """\
                <div class="project-links">
"""
        
        links = cls.get("links", {})
        for link, linkInfo in links.items():
            name = linkInfo.get("name", "")
            url = linkInfo.get("link", "")
        
            htmlStr += f"""\
                    <a href='{url}' target="_blank">
                    {name}
                    </a>
                </div>
"""
        return html.replace("@@project_links@@", htmlStr)
    return html
    
def BuildProject(yamlFile):
    filename = os.path.basename(yamlFile)
    data = Utils.ReadYaml(yamlFile)
    with open(Paths.GetTemplate("ProjectTemplate.html.src"), encoding="utf-8") as f:
        template = f.read()
        
    # Generate File Paths
    rel_path = os.path.relpath(yamlFile, Paths.YamlDir())
    rel_path = os.path.splitext(rel_path)[0] + ".html"

    output_path = os.path.join(Paths.OutputDir(), rel_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html = template
    cls = data["project"]
    
    html = InjectStyles(html)
    
    html = ProjectTitle(html, cls, "title")
    html = ProjectSubtitle(html, cls, "subtitle")
    html = ProjectOverview(html, cls, "overview")
    html = ProjectFeatureList(html, cls, "features")
    html = ProjectTechList(html, cls, "tech")
    html = ProjectScreenshots(html, cls, "screenshots")
    html = ProjectArchitecture(html, cls, "architecture")
    html = ProjectChallenges(html, cls, "challenges")
    html = ProjectLearned(html, cls, "learned")
    html = ProjectLinks(html, cls, "links")
    
    html = Utils.CleanUpHtml(html)
    
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(html)
    
#------------------------------------

# MAIN

# Ensure output directory exists
os.makedirs(Paths.OutputDir(), exist_ok=True)

# Loop yaml files to generate project pages
for root, dirs, files in os.walk(os.path.join(Paths.YamlDir(), "Projects")):
    for file in files:
        if file.endswith(".yaml"):
            full_path = os.path.join(root, file)
            BuildProject(full_path)
    
#------------------------------------
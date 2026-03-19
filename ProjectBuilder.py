import yaml
import os
from pygments import highlight
from pygments.lexers import CSharpLexer
from pygments.formatters import HtmlFormatter

import Paths


def Tabs(amount):
    return "    " * amount

# Conversions
def GetYaml(cls, key):
    if key in cls:
        return cls[key]
    return "YAML NOT FOUND"
    
def HasYaml(cls, key):
    if key in cls:
        return true;
    return false;
    
def CleanUpHtml(html):
    variables = ["@@styles@@", "@@project_title@@", "@@project_subtitle@@", "@@project_overview@@",
    "@@project_featurelist@@", "@@project_techlist@@", "@@project_screenshots@@", "@@project_architecture@@", "@@project_challenges@@",
    "@@project_learned@@", "@@project_links@@"]
    
    for var in variables:
        html = html.replace(var, "")
    return html

def InjectStyles(html):
    htmlStr = ""
    htmlStr += """<link rel="stylesheet" href="../CSS/style.css">"""
    htmlStr += "\n"
    htmlStr += """<link rel="stylesheet" href="../CSS/project.css">"""
    htmlStr += "\n"
    htmlStr += """<script defer src="../Scripts/particles.js"></script>"""
    htmlStr += "\n"
    
    return html.replace("@@styles@@", htmlStr)

def ProjectTitle(html, cls, search):
    if search in cls:
        htmlStr = GetYaml(cls, search)
        return html.replace("@@project_title@@", htmlStr)
    return html
def ProjectSubtitle(html, cls, search):
    if search in cls:
        htmlStr = GetYaml(cls, search)
        return html.replace("@@project_subtitle@@", htmlStr)
    return html
def ProjectOverview(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>Overview</h2>\n"
        htmlStr += "<p>\n"
        htmlStr += GetYaml(cls, search)
        htmlStr += "\n</p>\n</section>\n"
        
        return html.replace("@@project_overview@@", htmlStr)
    return html
def ProjectFeatureList(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>Key Features</h2>\n"
        htmlStr += """<ul class="feature-list">""" + "\n"
        
        # Generate List
        features = cls.get(search, [])
        for info in features:
            htmlStr += "<li>" + info + "</li>\n"
        
        htmlStr += "</ul>\n</section>\n"
        return html.replace("@@project_featurelist@@", htmlStr)
    return html
def ProjectTechList(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>Technologies Used</h2>\n"
        htmlStr += """<div class="tech-list">""" + "\n"
        
        # Generate List
        features = cls.get(search, [])
        for info in features:
            htmlStr += "<span>" + info + "</span>\n"
        
        htmlStr += "</div>\n</section>\n"
        return html.replace("@@project_techlist@@", htmlStr)
    return html
def ProjectScreenshots(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>Screenshots</h2>\n"
        htmlStr += """<div class="image-grid">""" + "\n"
        
        # Generate List
        features = cls.get(search, [])
        for info in features:
            htmlStr += """<img src='../Images/""" + info + """'>\n"""
        
        htmlStr += "</div>\n</section>\n"
        return html.replace("@@project_screenshots@@", htmlStr)
    return html
def ProjectArchitecture(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>Architecture</h2>\n"
        htmlStr += "<p>\n"
        htmlStr += GetYaml(cls, search)
        htmlStr += "\n</p>\n</section>\n"
        return html.replace("@@project_architecture@@", htmlStr)
    return html
def ProjectChallenges(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>Challenges & Solutions</h2>\n"
        htmlStr += "<p>\n"
        htmlStr += GetYaml(cls, search)
        htmlStr += "\n</p>\n</section>\n"
        return html.replace("@@project_challenges@@", htmlStr)
    return html
def ProjectLearned(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<section class = "section">""" + "\n"
        htmlStr += "<h2>What I Learned</h2>\n"
        htmlStr += "<p>\n"
        htmlStr += GetYaml(cls, search)
        htmlStr += "\n</p>\n</section>\n"
        return html.replace("@@project_learned@@", htmlStr)
    return html
    
def ProjectLinks(html, cls, search):
    if search in cls:
        htmlStr = ""
        htmlStr += """<div class="project-links">""" + "\n"
        
        links = cls.get("links", {})
        for link, linkInfo in links.items():
            name = linkInfo.get("name", "")
            url = linkInfo.get("link", "")
        
            htmlStr += """<a href='""" + url + """' target="_blank">"""
            htmlStr += name
            htmlStr += "</a>"
        
        htmlStr +="\n</div>\n"
        return html.replace("@@project_links@@", htmlStr)
    return html
    
def BuildProject(yamlFile):
    filename = os.path.basename(yamlFile)
    # READ YAML
    with open(yamlFile) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse YAML in {filename}: {e}")
            return
        if data is None:
            print(f"[WARNING] Skipping {filename} - File is empty or contains only comments")
            return
    # READ TEMPLATE
    with open(Paths.GetTemplate("ProjectTemplate.html.src"), encoding="utf-8") as f:
        template = f.read()
        
    # Generate File Paths
    rel_path = os.path.relpath(yamlFile, Paths.YamlDir())
    rel_path = os.path.splitext(rel_path)[0] + ".html"

    output_path = os.path.join(Paths.OutputDir(), rel_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(rel_path)
    print(output_path)
    
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
    
    html = CleanUpHtml(html)
    
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
import yaml
import os
from pygments import highlight
from pygments.lexers import CSharpLexer
from pygments.formatters import HtmlFormatter

def Tabs(amount):
    return "    " * amount

def ReadYaml(path):
    with open(path) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse YAML in {filename}: {e}")
            return ""
        if data is None:
            print(f"[WARNING] Skipping {filename} - File is empty or contains only comments")
            return ""
        return data
        
def GetYaml(cls, key):
    if key in cls:
        return cls[key]
    return "YAML NOT FOUND"
    
def CleanUpHtml(html):
    variables = ["@@styles@@",                                                              # MISC
    "@@project_title@@", "@@project_subtitle@@", "@@project_overview@@",                    # Projects [0]
    "@@project_featurelist@@", "@@project_techlist@@", "@@project_screenshots@@",           # Projects [1]
    "@@project_architecture@@", "@@project_challenges@@", "@@project_learned@@",            # Projects [2]
    "@@project_links@@",                                                                    # Projects [3]
    "@@INDEX_ABOUT@@", "@@INDEX_SKILLS@@", "@@INDEX_CONTACT@@", "@@INDEX_PROJECTS@@"]       # Index [0]
    
    for var in variables:
        html = html.replace(var, "")
    return html
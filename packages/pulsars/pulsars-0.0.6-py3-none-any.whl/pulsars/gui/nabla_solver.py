import panel as pn

def nablaSolver(name="Physics & Solver"):

    txt = """## Physics"""
    text2=pn.pane.Markdown(txt)
    solverhome=pn.Row(text2,name=name)
    return solverhome
    
    
import panel as pn

def nablaMaterials(name="Materials"):

    txt = """## Materials plan"""
    text2=pn.pane.Markdown(txt)
    matrialshome=pn.Row(text2,name=name)
    return matrialshome
    
    
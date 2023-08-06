import streamlit.components.v1 as components
import os


_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_comments",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_comments", path=build_dir)

def st_comments(comments,delete_keyword="", max_height="500px",custom_css="",key="st_comments",min_height="100px",
                custom_font_awesome_url = "https://kit.fontawesome.com/c7cbba6207.js", delete_user="all"):
    """
    Component um Kommetare anzuzeigen zu löschen und zubearbeiten

    Parameters

    ----------

    comments : list
        Liste mit Kommentaren in Form von Dictionaries. Jedes Dictionary muss die Keys "id", "user", "date" und "text" enthalten.
    delete_keyword : str (Kann auch HTML sein)
        Keyword um Kommentare zu löschen. Standard ist "Delete". Wenn HTML verwendet wird, muss das Keyword in Anführungszeichen stehen.
    max_height : str
        Maximale Höhe des Components. Standard ist "500px".
    min_height : str
        Minimale Höhe des Components. Standard ist "100px".
    custom_css : str
        Custom CSS für den Component. Standard ist "".
    key : str
        Key für den Component. Standard ist "st_comments".
    custom_font_awesome_url : str
        URL für die Font Awesome Bibliothek. Standard ist "https://kit.fontawesome.com/c7cbba6207.js".
    delete_user : str
        Controls wether someone is allowed to delete all comments or only his own. Standard is "all". Other option is is the Name of the user (each name should be unique ;) or "none" if no deletion is allowed.

    """
            
       
    component_value = _component_func(comments=comments, delete_keyword=delete_keyword,default=comments, max_height=max_height, custom_css=custom_css, key=key,min_height= min_height,
                                      custom_font_awesome_url = custom_font_awesome_url, delete_user = delete_user)
                                    

    return component_value

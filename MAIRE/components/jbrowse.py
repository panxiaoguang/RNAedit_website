import reflex as rx

hello_path = rx.asset("jbrowse.js", shared=True)
public_hello_path = "$/public/" + hello_path


class JbrowseComponent(rx.NoSSRComponent):
    library = public_hello_path
    tag: str = "JbrowseComponent"
    is_default = True
    lib_dependencies: list[str] = ["@fontsource/roboto","@mui/x-data-grid","@jbrowse/react-linear-genome-view2","jbrowse-plugin-ucsc","json-stable-stringify"]
    transpile_packages: list[str] = ["@mui/x-data-grid"]
    assembly: rx.Var[dict]
    tracks: rx.Var[list]
    location: rx.Var[str]
    default_session: rx.Var[dict]


j_browse_linear_genome_view = JbrowseComponent.create




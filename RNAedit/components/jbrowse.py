import reflex as rx



class JbrowseComponent(rx.NoSSRComponent):
    library: str = "/public/jbrowse"
    tag: str = "JbrowseComponent"
    is_default = True
    lib_dependencies: list[str] = ["@fontsource/roboto","@jbrowse/react-linear-genome-view2","jbrowse-plugin-ucsc","json-stable-stringify"]

    assembly: rx.Var[dict]
    tracks: rx.Var[list]
    location: rx.Var[str]
    default_session: rx.Var[dict]

    get_session: rx.EventHandler[lambda x: [x]]

j_browse_linear_genome_view = JbrowseComponent.create




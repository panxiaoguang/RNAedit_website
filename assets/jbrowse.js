import "@fontsource/roboto";
import {
  createViewState,
  JBrowseLinearGenomeView,
} from "@jbrowse/react-linear-genome-view2";

import UCSC from "jbrowse-plugin-ucsc";

export default function JbrowseComponent({ assembly, tracks, location, defaultSession}) {
 
  const state = createViewState({
    assembly,
    tracks,
    location,
    plugins: [UCSC],
    defaultSession,
  });
  
  return (
    <div id="jbrowse_view">
      <JBrowseLinearGenomeView viewState={state} />
    </div>
  );
}

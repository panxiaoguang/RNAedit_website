import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functools import lru_cache
from typing import List, Dict, Tuple, Optional

# Constants for visualization
MAX_TRANSCRIPTS = 5  # Limit number of transcripts for performance
ARROW_INTERVAL = 2000  # Increase arrow interval to reduce elements
EXON_COLOR = "#1E90FF"
UTR_COLOR = "#FFA500"
MARGIN_BUFFER = 1000


def create_visualization_2(transcripts: List[Dict], dot_plot_data: Optional[List[Dict]] = None) -> go.Figure:
    """Optimized visualization function with improved performance
    
    Performance improvements:
    - Limit number of transcripts displayed
    - Reduce DOM elements by batch processing
    - Cache arrow calculations
    - Use ScatterGL for large datasets
    - Eliminate duplicate code paths
    
    Args:
        transcripts: List of transcript data
        dot_plot_data: Optional scatter plot data
    """
    if not transcripts:
        return go.Figure()
    
    # Limit transcripts for performance
    display_transcripts = transcripts[:MAX_TRANSCRIPTS]
    
    # Pre-calculate configuration
    config = _get_visualization_config(display_transcripts, dot_plot_data)
    
    # Create figure layout
    fig = _create_figure_layout(config)
    
    # Add transcript elements in batches
    _add_transcript_elements_batch(fig, display_transcripts, config)
    
    # Add scatter plot if needed
    if config['has_dot_plot']:
        _add_scatter_plot_optimized(fig, dot_plot_data, config)
    
    # Finalize layout
    _finalize_layout(fig, config)
    
    # Add truncation notice if needed
    if len(transcripts) > MAX_TRANSCRIPTS:
        fig.add_annotation(
            text=f"Showing {MAX_TRANSCRIPTS} of {len(transcripts)} transcripts",
            xref="paper", yref="paper",
            x=0.02, y=0.98, 
            showarrow=False,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        )
    
    return fig


def _get_visualization_config(transcripts: List[Dict], dot_plot_data: Optional[List[Dict]]) -> Dict:
    """Pre-calculate configuration to avoid repeated computations"""
    return {
        'has_dot_plot': dot_plot_data is not None and len(dot_plot_data) > 0,
        'gene_name': transcripts[0]["gene_name"] if transcripts else "Unknown Gene",
        'genome_min': min(t["transcript_start"] for t in transcripts),
        'genome_max': max(t["transcript_end"] for t in transcripts),
        'transcript_count': len(transcripts)
    }


def _create_figure_layout(config: Dict) -> go.Figure:
    """Create figure with optimized layout"""
    if config['has_dot_plot']:
        return make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.3, 0.7],  # Adjusted for better balance
            vertical_spacing=0.05
        )
    else:
        return go.Figure()


def _add_transcript_elements_batch(fig: go.Figure, transcripts: List[Dict], config: Dict) -> None:
    """Add transcript elements in optimized batches"""
    
    # Collect all shapes and traces for batch addition
    shapes = []
    hover_traces = []
    
    for i, transcript in enumerate(transcripts):
        y_level = config['transcript_count'] - i
        transcript_info = _extract_transcript_info(transcript)
        
        # Add transcript line
        shapes.append(_create_transcript_line(transcript_info, y_level, config))
        
        # Process exons and UTRs in batch
        exon_shapes, exon_traces = _process_exons_batch(transcript_info, y_level, config)
        utr_shapes, utr_traces = _process_utrs_batch(transcript_info, y_level, config)
        
        shapes.extend(exon_shapes)
        shapes.extend(utr_shapes)
        hover_traces.extend(exon_traces)
        hover_traces.extend(utr_traces)
        
        # Add optimized arrows
        _add_arrows_optimized(fig, transcript_info, y_level, config)
    
    # Batch add all shapes
    for shape in shapes:
        fig.add_shape(**shape)
    
    # Batch add all hover traces
    for trace_data in hover_traces:
        fig.add_trace(**trace_data)


def _extract_transcript_info(transcript: Dict) -> Dict:
    """Extract and cache transcript information"""
    return {
        'id': transcript["id"],
        'gene_name': transcript["gene_name"],
        'gene_type': transcript["gene_type"],
        'strand': transcript["strand"],
        'start': transcript["transcript_start"],
        'end': transcript["transcript_end"],
        'exons': transcript["coding_exons"],
        'utrs': transcript["utrs"]
    }


def _create_transcript_line(transcript_info: Dict, y_level: int, config: Dict) -> Dict:
    """Create transcript line shape"""
    shape_data = {
        'type': "line",
        'x0': transcript_info['start'],
        'x1': transcript_info['end'],
        'y0': y_level,
        'y1': y_level,
        'line': dict(color="gray", width=1)
    }
    
    if config['has_dot_plot']:
        shape_data.update({'row': 1, 'col': 1})
    
    return shape_data


def _process_exons_batch(transcript_info: Dict, y_level: int, config: Dict) -> Tuple[List[Dict], List[Dict]]:
    """Process all exons for a transcript in batch"""
    shapes = []
    traces = []
    
    # Merge overlapping exons to reduce DOM elements
    merged_exons = _merge_overlapping_regions(transcript_info['exons'])
    
    for exon_start, exon_end in merged_exons:
        # Create shape
        shape_data = {
            'type': "rect",
            'x0': exon_start,
            'x1': exon_end,
            'y0': y_level - 0.3,
            'y1': y_level + 0.3,
            'fillcolor': EXON_COLOR,
            'line': dict(color="black", width=1),
            'opacity': 1
        }
        
        if config['has_dot_plot']:
            shape_data.update({'row': 1, 'col': 1})
        
        shapes.append(shape_data)
        
        # Create hover trace with simplified data
        trace_data = {
            'trace': go.Scatter(
                x=[(exon_start + exon_end) / 2],
                y=[y_level],
                text=[f"<b>Transcript:</b> {transcript_info['id']}<br>"
                      f"<b>Element:</b> Coding Exon<br>"
                      f"<b>Coordinates:</b> {exon_start:,}-{exon_end:,}"],
                hoverinfo="text",
                mode="markers",
                marker=dict(size=0.1, color=EXON_COLOR, opacity=0),
                showlegend=False
            )
        }
        
        if config['has_dot_plot']:
            trace_data.update({'row': 1, 'col': 1})
        
        traces.append(trace_data)
    
    return shapes, traces


def _process_utrs_batch(transcript_info: Dict, y_level: int, config: Dict) -> Tuple[List[Dict], List[Dict]]:
    """Process all UTRs for a transcript in batch"""
    shapes = []
    traces = []
    
    # Convert UTR format and merge overlapping regions
    utr_regions = [(utr_start, utr_end) for _, utr_start, utr_end in transcript_info['utrs']]
    merged_utrs = _merge_overlapping_regions(utr_regions)
    
    for utr_start, utr_end in merged_utrs:
        # Create shape
        shape_data = {
            'type': "rect",
            'x0': utr_start,
            'x1': utr_end,
            'y0': y_level - 0.15,
            'y1': y_level + 0.15,
            'fillcolor': UTR_COLOR,
            'line': dict(color="black", width=1),
            'opacity': 1
        }
        
        if config['has_dot_plot']:
            shape_data.update({'row': 1, 'col': 1})
        
        shapes.append(shape_data)
        
        # Create hover trace with simplified data
        trace_data = {
            'trace': go.Scatter(
                x=[(utr_start + utr_end) / 2],
                y=[y_level],
                text=[f"<b>Transcript:</b> {transcript_info['id']}<br>"
                      f"<b>Element:</b> UTR<br>"
                      f"<b>Coordinates:</b> {utr_start:,}-{utr_end:,}"],
                hoverinfo="text",
                mode="markers",
                marker=dict(size=0.1, color=UTR_COLOR, opacity=0),
                showlegend=False
            )
        }
        
        if config['has_dot_plot']:
            trace_data.update({'row': 1, 'col': 1})
        
        traces.append(trace_data)
    
    return shapes, traces


@lru_cache(maxsize=100)
def _calculate_arrow_positions(start: int, end: int, length: int, merged_features_hash: str) -> Tuple[int, ...]:
    """Cache arrow position calculations to avoid repeated computations"""
    import hashlib
    
    # Reduce number of arrows for performance
    num_arrows = max(1, min(3, length // ARROW_INTERVAL))
    
    # Simple uniform distribution for performance
    if num_arrows == 1:
        return (start + length // 2,)
    
    step = length / (num_arrows + 1)
    return tuple(int(start + (i + 1) * step) for i in range(num_arrows))


def _add_arrows_optimized(fig: go.Figure, transcript_info: Dict, y_level: int, config: Dict) -> None:
    """Add arrows with optimized calculations and reduced count"""
    
    # Create simple hash for caching
    features_str = str(sorted(transcript_info['exons'] + [(s, e) for _, s, e in transcript_info['utrs']]))
    features_hash = str(hash(features_str))
    
    transcript_length = transcript_info['end'] - transcript_info['start']
    
    # Get cached arrow positions
    arrow_positions = _calculate_arrow_positions(
        transcript_info['start'], 
        transcript_info['end'], 
        transcript_length, 
        features_hash
    )
    
    # Add arrows in batch
    for pos in arrow_positions:
        arrow_data = {
            'x': pos,
            'y': y_level,
            'ax': pos - 100 if transcript_info['strand'] == "+" else pos + 100,
            'ay': y_level,
            'xref': "x",
            'yref': "y",
            'axref': "x",
            'ayref': "y",
            'showarrow': True,
            'arrowhead': 2,
            'arrowsize': 1,
            'arrowwidth': 1,
            'arrowcolor': "gray"
        }
        
        if config['has_dot_plot']:
            arrow_data.update({'row': 1, 'col': 1})
        
        fig.add_annotation(**arrow_data)


def _add_scatter_plot_optimized(fig: go.Figure, dot_plot_data: List[Dict], config: Dict) -> None:
    """Add scatter plot with performance optimizations"""
    
    if not dot_plot_data:
        return
    
    # Extract data in batch
    x_values = [point["x"] for point in dot_plot_data]
    y_values = [point["y"] for point in dot_plot_data]
    tissues = [point["tissue_name"] for point in dot_plot_data]
    
    # Use ScatterGL for better performance with large datasets
    trace_class = go.Scattergl if len(dot_plot_data) > 100 else go.Scatter
    
    fig.add_trace(
        trace_class(
            x=x_values,
            y=y_values,
            mode="markers",
            marker=dict(
                size=6,  # Reduced size for performance
                color="red",
                symbol="circle",
                line=dict(width=0.5, color="black")  # Thinner lines
            ),
            hovertemplate="<b>Position:</b> %{x:,}<br><b>Level:</b> %{y}<br><b>Tissue:</b> %{text}<extra></extra>",
            text=tissues,
            name="RNA editing level"
        ),
        row=2, col=1
    )


def _finalize_layout(fig: go.Figure, config: Dict) -> None:
    """Finalize figure layout with optimizations"""
    
    base_layout = {
        'title': {
            'text': config['gene_name'],
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        'plot_bgcolor': "white",
        'margin': dict(l=50, r=50, t=50, b=50),
        'hovermode': "closest"
    }
    
    if config['has_dot_plot']:
        fig.update_layout(**base_layout)
        
        # Update gene structure subplot
        fig.update_yaxes(visible=False, range=[0, config['transcript_count'] + 1], row=1, col=1)
        fig.update_xaxes(title="", showticklabels=False, row=1, col=1)
        
        # Update scatter plot subplot
        fig.update_yaxes(title="Editing Level", row=2, col=1)
        fig.update_xaxes(title="Genomic Position", row=2, col=1)
        
        # Set X-axis range for both subplots
        x_range = [config['genome_min'] - MARGIN_BUFFER, config['genome_max'] + MARGIN_BUFFER]
        fig.update_xaxes(range=x_range, row=1, col=1)
        fig.update_xaxes(range=x_range, row=2, col=1)
    else:
        base_layout.update({
            'xaxis_title': "Genomic Position",
            'yaxis': dict(
                visible=False,
                range=[0, config['transcript_count'] + 1]
            )
        })
        fig.update_layout(**base_layout)


def _merge_overlapping_regions(regions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Merge overlapping regions to reduce the number of DOM elements"""
    if not regions:
        return []
    
    # Sort regions by start position
    sorted_regions = sorted(regions, key=lambda x: x[0])
    merged = [sorted_regions[0]]
    
    for current in sorted_regions[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # Overlapping
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    
    return merged
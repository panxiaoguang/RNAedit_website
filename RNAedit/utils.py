import plotly.graph_objects as go
from plotly.subplots import make_subplots

def parse_gene_data(gene_data):
    transcript_data = gene_data.transcripts
    transcript_list = []
    for transcript in transcript_data:
        if not transcript.cdses and not transcript.utres:
            continue
        else:
            transcript_dict = {
                "id": transcript.transcript_id,
                "gene_name": gene_data.symbol,
                "gene_type": transcript.transcript_type,
                "strand": "+" if gene_data.strand == 1 else "-",
                "coding_exons": [(cds.start, cds.end) for cds in transcript.cdses],
                "utrs": [("UTR", utr.start, utr.end) for utr in transcript.utres],
                "transcript_start": transcript.start,
                "transcript_end": transcript.end,
            }
            transcript_list.append(transcript_dict)
    return transcript_list


def create_visualization(transcripts, dot_plot_data=None):
    """创建可视化图形, 类似UCSC基因浏览器的效果

    Args:
        transcripts: 转录本数据列表
        dot_plot_data: 可选，散点图数据，格式为[{"x": position, "y": value}, ...]
    """
    # 获取基因名称（从第一个转录本获取）
    gene_name = transcripts[0]["gene_name"] if transcripts else "Unknown Gene"
    # 检查是否有散点图数据
    has_dot_plot = dot_plot_data is not None and len(dot_plot_data) > 0

    # 创建子图布局
    if has_dot_plot:
        # 创建两个子图：上面是基因结构，下面是散点图
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,  # 共享X轴
            row_heights=[0.7, 0.3],  # 基因结构占70%，散点图占30%
            vertical_spacing=0.05,
        )  # 子图间距
    else:
        # 只有基因结构图
        fig = go.Figure()

    # 获取基因组坐标范围
    genome_min = min([t["transcript_start"] for t in transcripts])
    genome_max = max([t["transcript_end"] for t in transcripts])

    y_level = len(transcripts)  # 从上到下排列转录本

    # 使用统一的颜色
    exon_color = "#1E90FF"  # 蓝色用于外显子
    utr_color = "#FFA500"  # 橙色用于UTR

    # 绘制所有转录本的连接线（最底层）
    for transcript in transcripts:
        # 绘制转录本连接线
        if has_dot_plot:
            fig.add_shape(
                type="line",
                x0=transcript["transcript_start"],
                x1=transcript["transcript_end"],
                y0=y_level,
                y1=y_level,
                line=dict(color="gray", width=1),
                row=1,
                col=1,
            )
        else:
            fig.add_shape(
                type="line",
                x0=transcript["transcript_start"],
                x1=transcript["transcript_end"],
                y0=y_level,
                y1=y_level,
                line=dict(color="gray", width=1),
            )
        y_level -= 1

    # 重置y_level
    y_level = len(transcripts)

    # 绘制所有转录本的矩形（中间层）
    for transcript in transcripts:
        # 获取转录本信息
        transcript_id = transcript["id"]
        gene_name = transcript["gene_name"]
        gene_type = transcript["gene_type"]

        # 绘制编码区外显子
        for exon_start, exon_end in transcript["coding_exons"]:
            # 添加外显子矩形
            if has_dot_plot:
                fig.add_shape(
                    type="rect",
                    x0=exon_start,
                    x1=exon_end,
                    y0=y_level - 0.3,
                    y1=y_level + 0.3,
                    fillcolor=exon_color,
                    line=dict(color="black", width=1),
                    opacity=1,
                    row=1,
                    col=1,
                )
            else:
                fig.add_shape(
                    type="rect",
                    x0=exon_start,
                    x1=exon_end,
                    y0=y_level - 0.3,
                    y1=y_level + 0.3,
                    fillcolor=exon_color,
                    line=dict(color="black", width=1),
                    opacity=1,
                )

            # 添加悬停信息
            if has_dot_plot:
                fig.add_trace(
                    go.Scatter(
                        x=[(exon_start + exon_end) / 2],
                        y=[y_level],
                        text=[
                            f"<b>Transcript:</b> {transcript_id}<br><b>Gene:</b> {gene_name}<br><b>Type:</b> {gene_type}<br><b>Element:</b> Coding Exon<br><b>Coordinates:</b> {exon_start:,}-{exon_end:,}<br><b>Length:</b> {exon_end - exon_start:,}bp"
                        ],
                        hoverinfo="text",
                        mode="markers",
                        marker=dict(size=0.1, color=exon_color, opacity=0),
                        showlegend=False,
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[(exon_start + exon_end) / 2],
                        y=[y_level],
                        text=[
                            f"<b>Transcript:</b> {transcript_id}<br><b>Gene:</b> {gene_name}<br><b>Type:</b> {gene_type}<br><b>Element:</b> Coding Exon<br><b>Coordinates:</b> {exon_start:,}-{exon_end:,}<br><b>Length:</b> {exon_end - exon_start:,}bp"
                        ],
                        hoverinfo="text",
                        mode="markers",
                        marker=dict(size=0.1, color=exon_color, opacity=0),
                        showlegend=False,
                    )
                )

        # 绘制UTR区域
        for utr_type, utr_start, utr_end in transcript["utrs"]:
            # 添加UTR矩形（高度较低）
            if has_dot_plot:
                fig.add_shape(
                    type="rect",
                    x0=utr_start,
                    x1=utr_end,
                    y0=y_level - 0.15,
                    y1=y_level + 0.15,  # 高度是编码区的一半
                    fillcolor=utr_color,
                    line=dict(color="black", width=1),
                    opacity=1,
                    row=1,
                    col=1,
                )
            else:
                fig.add_shape(
                    type="rect",
                    x0=utr_start,
                    x1=utr_end,
                    y0=y_level - 0.15,
                    y1=y_level + 0.15,  # 高度是编码区的一半
                    fillcolor=utr_color,
                    line=dict(color="black", width=1),
                    opacity=1,
                )

            # 添加悬停信息
            if has_dot_plot:
                fig.add_trace(
                    go.Scatter(
                        x=[(utr_start + utr_end) / 2],
                        y=[y_level],
                        text=[
                            f"<b>Transcript:</b> {transcript_id}<br><b>Gene:</b> {gene_name}<br><b>Type:</b> {gene_type}<br><b>Element:</b> {utr_type}<br><b>Coordinates:</b> {utr_start:,}-{utr_end:,}<br><b>Length:</b> {utr_end - utr_start:,}bp"
                        ],
                        hoverinfo="text",
                        mode="markers",
                        marker=dict(size=0.1, color=utr_color, opacity=0),
                        showlegend=False,
                    ),
                    row=1,
                    col=1,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[(utr_start + utr_end) / 2],
                        y=[y_level],
                        text=[
                            f"<b>Transcript:</b> {transcript_id}<br><b>Gene:</b> {gene_name}<br><b>Type:</b> {gene_type}<br><b>Element:</b> {utr_type}<br><b>Coordinates:</b> {utr_start:,}-{utr_end:,}<br><b>Length:</b> {utr_end - utr_start:,}bp"
                        ],
                        hoverinfo="text",
                        mode="markers",
                        marker=dict(size=0.1, color=utr_color, opacity=0),
                        showlegend=False,
                    )
                )

        y_level -= 1

    # 如果有散点图数据，添加散点图
    if has_dot_plot:
        # 提取x和y值
        x_values = [point["x"] for point in dot_plot_data]
        y_values = [point["y"] for point in dot_plot_data]

        # 添加散点图
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="markers",
                marker=dict(
                    size=8,
                    color="red",
                    symbol="circle",
                    line=dict(width=1, color="black"),
                ),
                hoverinfo="text",
                text=[
                    f"Position: {x:,}<br>Value: {y}" for x, y in zip(x_values, y_values)
                ],
                name="Data Points",
            ),
            row=2,
            col=1,
        )

    # 重置y_level
    y_level = len(transcripts)

    # 最后添加标签和箭头（最上层，但会被矩形遮挡）
    for transcript in transcripts:
        # 获取转录本信息
        transcript_id = transcript["id"]
        gene_name = transcript["gene_name"]
        strand = transcript["strand"]

        # 不再添加转录本标签，移除此部分代码

        # 计算箭头位置，避开外显子和UTR区域
        arrow_positions = []
        transcript_length = (
            transcript["transcript_end"] - transcript["transcript_start"]
        )
        num_arrows = max(1, int(transcript_length / 1000))  # 每1kb一个箭头

        # 获取所有外显子和UTR的位置
        all_features = []
        for start, end in transcript["coding_exons"]:
            all_features.append((start, end))
        for _, start, end in transcript["utrs"]:
            all_features.append((start, end))

        # 合并重叠区间
        if all_features:
            all_features.sort()
            merged_features = [all_features[0]]
            for current in all_features[1:]:
                previous = merged_features[-1]
                if current[0] <= previous[1]:  # 有重叠
                    merged_features[-1] = (previous[0], max(previous[1], current[1]))
                else:
                    merged_features.append(current)

            # 在非特征区域放置箭头
            step = transcript_length / (num_arrows + 1)
            for i in range(1, num_arrows + 1):
                pos = transcript["transcript_start"] + i * step
                # 检查位置是否在任何特征内
                in_feature = False
                for start, end in merged_features:
                    if start <= pos <= end:
                        in_feature = True
                        break
                if not in_feature:
                    arrow_positions.append(pos)

        # 如果没有找到合适的位置，使用原来的方法
        if not arrow_positions:
            for i in range(num_arrows):
                pos = transcript["transcript_start"] + (i + 0.5) * (
                    transcript_length / num_arrows
                )
                arrow_positions.append(pos)

        # 绘制箭头
        for pos in arrow_positions:
            if strand == "+":
                if has_dot_plot:
                    fig.add_annotation(
                        x=pos,
                        y=y_level,
                        ax=pos - 100,
                        ay=y_level,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=1,
                        arrowcolor="gray",
                        row=1,
                        col=1,
                    )
                else:
                    fig.add_annotation(
                        x=pos,
                        y=y_level,
                        ax=pos - 100,
                        ay=y_level,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=1,
                        arrowcolor="gray",
                    )
            else:  # 负链箭头指向左侧
                if has_dot_plot:
                    fig.add_annotation(
                        x=pos,
                        y=y_level,
                        ax=pos + 100,
                        ay=y_level,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=1,
                        arrowcolor="gray",
                        row=1,
                        col=1,
                    )
                else:
                    fig.add_annotation(
                        x=pos,
                        y=y_level,
                        ax=pos + 100,
                        ay=y_level,
                        xref="x",
                        yref="y",
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=1,
                        arrowcolor="gray",
                    )

        y_level -= 1

    # 设置布局
    if has_dot_plot:
        fig.update_layout(
            title={
                'text': gene_name,
                'x': 0.5,  # 居中显示
                'xanchor': 'center',
                'yanchor': 'top'
            },
            # height=max(600, 50 * len(transcripts) + 200),  # 根据转录本数量调整高度
            plot_bgcolor="white",
            margin=dict(l=50, r=50, t=50, b=50),  # 减小左侧边距，因为不再显示转录本ID
        )

        # 更新基因结构子图
        fig.update_yaxes(visible=False, range=[0, len(transcripts) + 1], row=1, col=1)
        fig.update_xaxes(title="", showticklabels=False, row=1, col=1)

        # 更新散点图子图
        fig.update_yaxes(title="Value", row=2, col=1)
        fig.update_xaxes(title="Genomic Position", row=2, col=1)

        # 设置X轴范围，确保两个子图共享相同的X轴范围
        fig.update_xaxes(range=[genome_min - 1000, genome_max + 1000], row=1, col=1)
        fig.update_xaxes(range=[genome_min - 1000, genome_max + 1000], row=2, col=1)
    else:
        fig.update_layout(
            title={
                'text': gene_name,
                'x': 0.5,  # 居中显示
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Genomic Position",
            yaxis=dict(
                visible=False,  # 隐藏Y轴
                range=[0, len(transcripts) + 1],  # 设置Y轴范围
            ),
            hovermode="closest",
            # height=max(450, 50 * len(transcripts)),  # 根据转录本数量调整高度
            plot_bgcolor="white",
            margin=dict(l=50, r=50, t=50, b=50),  # 减小左侧边距，因为不再显示转录本ID
        )

    return fig





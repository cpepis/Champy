# Champy/plot_helpers.py

import plotly.graph_objects as go


def create_speedup_bar_chart(
    df_default,
    df_speedup,
    prefetchers,
    title,
    height=750,
    legend_title="Prefetcher",
    show_default=False,
):
    """
    Creates a grouped bar chart comparing speedup for different prefetchers.
    """
    fig = go.Figure()

    benchmarks = df_default["Benchmark"]
    for key, props in prefetchers.items():
        if not show_default and key == "default":
            continue

        color = props.get("color", None)
        line_color = props.get("edgecolor", None)
        hatch_pattern = props.get("hatch", None)

        fig.add_trace(
            go.Bar(
                x=benchmarks,
                y=df_speedup[key]["Speedup"],
                name=props["label"],
                marker=dict(
                    color=color,  # Sets the fill color
                    line=dict(color=line_color),  # Sets edge color
                    pattern_shape=hatch_pattern,  # Sets hatch pattern
                ),
            )
        )

    fig.update_layout(
        title=title,
        xaxis=dict(title="Benchmark", tickangle=-45),
        yaxis=dict(title="Speedup (%)"),
        barmode="group",
        legend_title=legend_title,
        height=height,
    )
    return fig

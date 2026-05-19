from __future__ import annotations

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output


def build_dashboard(df_sales_detail: pd.DataFrame) -> None:
    df = df_sales_detail.copy()
    df["full_date"] = pd.to_datetime(df["full_date"])

    min_date = df["full_date"].min().date()
    max_date = df["full_date"].max().date()

    countries = ["Todos"] + sorted(df["country"].dropna().unique().tolist())
    product_lines = ["Todos"] + sorted(df["product_line"].dropna().unique().tolist())

    start_date_widget = widgets.DatePicker(description="Data inicial", value=min_date)
    end_date_widget = widgets.DatePicker(description="Data final", value=max_date)
    country_widget = widgets.Dropdown(options=countries, value="Todos", description="País")
    product_line_widget = widgets.Dropdown(options=product_lines, value="Todos", description="Linha")
    top_n_widget = widgets.IntSlider(value=10, min=1, max=10, step=1, description="Top N")

    output = widgets.Output()

    def update_dashboard(change=None):
        with output:
            clear_output(wait=True)

            start_date = pd.to_datetime(start_date_widget.value)
            end_date = pd.to_datetime(end_date_widget.value)

            if pd.isna(start_date) or pd.isna(end_date):
                print("Selecione uma data inicial e uma data final.")
                return

            if start_date > end_date:
                print("A data inicial deve ser menor ou igual à data final.")
                return

            filtered = df[
                (df["full_date"] >= start_date) &
                (df["full_date"] <= end_date)
            ].copy()

            if country_widget.value != "Todos":
                filtered = filtered[filtered["country"] == country_widget.value]

            if product_line_widget.value != "Todos":
                filtered = filtered[filtered["product_line"] == product_line_widget.value]

            if filtered.empty:
                print("Nenhum registro encontrado para os filtros selecionados.")
                return

            ranked = (
                filtered
                .groupby("product_name", as_index=False)["total_sales"]
                .sum()
                .sort_values("total_sales", ascending=False)
                .head(top_n_widget.value)
            )

            display(ranked)

            plt.figure(figsize=(11, 6))
            sns.barplot(
                data=ranked,
                x="total_sales",
                y="product_name"
            )
            plt.title("Top produtos por vendas totais")
            plt.xlabel("Vendas totais")
            plt.ylabel("Produto")
            plt.tight_layout()
            plt.show()

    for widget in [
        start_date_widget,
        end_date_widget,
        country_widget,
        product_line_widget,
        top_n_widget,
    ]:
        widget.observe(update_dashboard, names="value")

    controls = widgets.VBox([
        widgets.HBox([start_date_widget, end_date_widget]),
        widgets.HBox([country_widget, product_line_widget, top_n_widget]),
    ])

    display(controls, output)
    update_dashboard()

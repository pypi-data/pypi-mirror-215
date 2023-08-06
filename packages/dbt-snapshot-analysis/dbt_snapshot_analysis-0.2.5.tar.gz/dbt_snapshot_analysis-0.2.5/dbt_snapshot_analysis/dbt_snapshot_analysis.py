import pandas as pd
import streamlit as st
from typing import List
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


from snapshot_utils import (
    get_metric_by_month,
    get_snapshot_as_of_date,
)


@st.cache_data()
def compute_all_metric_day_by_day(df: pd.DataFrame, date_range: List[str]):
    print("Computing metric day by day...")
    all_results = pd.DataFrame()
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    index = 0
    for day in date_range:
        index += 1
        day_date = datetime.strptime(day, "%Y-%m-%d")
        current_df = get_snapshot_as_of_date(df, day_date)
        metric_by_month = get_metric_by_month(
            current_df, "metric_value", "metric_date", "%Y-%m"
        )
        metric_by_month["computation_day"] = day_date.date()
        all_results = pd.concat([all_results, metric_by_month], ignore_index=True)
        progress = index / date_range.__len__()
        my_bar.progress(progress, text=progress_text)

    my_bar.empty()
    return all_results


def is_numeric_column(df, column_name):
    try:
        pd.to_numeric(df[column_name])
        return True
    except ValueError:
        return False


def is_date_column(df, column_name):
    try:
        pd.to_datetime(df[column_name])
        return True
    except ValueError:
        return False


@st.cache_data()
def parse_uploaded_file(uploaded_file):
    print("Parsing uploaded file...")
    df = pd.read_csv(uploaded_file, low_memory=False)

    # format dates
    try:
        df["dbt_valid_from"] = pd.to_datetime(df["dbt_valid_from"], unit="s")
        now = pd.Timestamp.now().timestamp()
        df["dbt_valid_to"] = df["dbt_valid_to"].fillna(now)
        df["dbt_valid_to"] = pd.to_datetime(df["dbt_valid_to"], unit="s")
    except ValueError as e:
        invalid_row_index = int(str(e).split(" ")[-1])
        print(f"Invalid row index: {invalid_row_index}")

    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    return df


@st.cache_data()
def get_metric_value_and_date(df, metric_column, date_column):
    is_numeric_column_valid = is_numeric_column(df, metric_column)
    is_date_column_valid = is_date_column(df, date_column)
    if is_numeric_column_valid and is_date_column_valid:
        df["metric_value"] = df[metric_column]
        df["metric_date"] = df[date_column]

        df = df[(df["metric_date"].notnull()) & (df["metric_value"].notnull())]
    else:
        st.write("Please select a valid metric column and a date column")
    return df


def run():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = parse_uploaded_file(uploaded_file)
        col1, col2 = st.columns(2)
        with col1:
            metric_column = st.selectbox("Select metric column", df.columns)
            is_numeric_column_valid = is_numeric_column(df, metric_column)
            if not is_numeric_column_valid:
                st.warning(
                    "Please select a valid metric column, it should be a numeric column."
                )

        with col2:
            date_column = st.selectbox("Select metric date column", df.columns)
            is_date_column_valid = is_date_column(df, date_column)
            if not is_date_column_valid:
                st.warning(
                    "Please select a valid date column, it should be supported by pandas.to_datetime."
                )

        tab1, tab2, tab3 = st.tabs(["Version", "Lifespan", "Data"])
        with tab1:
            st.markdown("## Distribution of versions per ID")
            st.header("Version distribution")
            unique_ids = df.groupby("id").size()
            print(f"Number of unique ids: {unique_ids.shape[0]}")
            versions_per_id = df.groupby("id").size().reset_index(name="num_versions")
            versions_count = versions_per_id["num_versions"].value_counts().sort_index()

            st.bar_chart(versions_count)

        with tab2:
            lifespandf = df.copy()
            lifespandf["lifespan"] = (
                lifespandf["dbt_valid_to"] - lifespandf["dbt_valid_from"]
            )
            print(lifespandf["lifespan"].describe())
            lifespandf["lifespan_numeric"] = pd.to_numeric(
                lifespandf["lifespan"], errors="coerce"
            )
            lifespandf["lifespan_days"] = lifespandf["lifespan_numeric"] / 86400
            fig = px.histogram(lifespandf["lifespan_days"], nbins=20)

            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.header("Dataframe")
            st.write(df)

        min_date = df["dbt_valid_from"].min()
        max_date = df["dbt_valid_from"].max()
        date_range = pd.date_range(start=min_date, end=max_date)
        date_range_str = date_range.strftime("%Y-%m-%d").tolist()

        if is_numeric_column_valid and is_date_column_valid:
            df = get_metric_value_and_date(df, metric_column, date_column)

            all_results = compute_all_metric_day_by_day(df, date_range_str)

            grouped_df = all_results.groupby("metric_date")

            st.set_option("deprecation.showPyplotGlobalUse", False)
            fig = go.Figure()

            for metric_name, group in grouped_df:
                fig.add_trace(
                    go.Scatter(
                        x=group["computation_day"],
                        y=group["metric_value"],
                        name=metric_name,
                    )
                )

            fig.update_layout(
                title="Metric Value Over Time",
                xaxis_title="Computation Day",
                yaxis_title="Metric Value",
                showlegend=True,
            )
            st.plotly_chart(fig)


def main():
    run()


if __name__ == "__main__":
    main()

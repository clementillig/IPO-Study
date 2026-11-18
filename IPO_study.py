import requests
import pandas as pd
import numpy as np
import re
import time
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# SETTINGS
BASE_URL = "https://www.skyipo.com/api"
START_YEAR = 2020
END_YEAR = 2026

OUTPUT_DIR = Path("ipo_tech_results")
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "IPOResearchStudy/1.0 (personal research)",
    "Accept": "application/json"
}

# IMPORTANT PRECISION
# SkyIPO's coverage is incomplete. The reported coverage estimate should be
# verified against the source before publication.

# Keywords used to identify technology companies; classification requires review.
TECH_KEYWORDS = [
    "technology",
    "information technology",
    "software",
    "semiconductor",
    "computer",
    "internet",
    "cloud",
    "cybersecurity",
    "artificial intelligence",
    "machine learning",
    "data processing",
    "data analytics",
    "electronics",
    "electronic equipment",
    "networking",
    "telecommunications equipment",
    "digital services",
    "saas",
    "fintech software",
    "robotics",
    "automation",
    " IT services",
]

# API CALL FUNCTIONS

def extract_records(payload):
    """Handle several possible JSON response structures."""
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ["ipos", "data", "results", "records"]:
            if key in payload:
                value = payload[key]
                if isinstance(value, list):
                    return value
                if isinstance(value, dict):
                    return extract_records(value)

    raise ValueError(
        "Unrecognised JSON structure: "
        + str(type(payload))
    )


def fetch_year(year):
    url = f"{BASE_URL}/ipos/{year}.json"
    print(f"Downloading IPOs for {year}...")

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    records = extract_records(response.json())

    print(f"{len(records)} records retrieved.")
    return records


def download_all():
    records = []

    for year in range(START_YEAR, END_YEAR + 1):
        try:
            records.extend(fetch_year(year))
        except requests.RequestException as e:
            print(f"HTTP error for {year}: {e}")
        except (ValueError, KeyError) as e:
            print(f"Data error for {year}: {e}")
        time.sleep(0.5)

    return pd.DataFrame(records)


# DATA CLEANING AND PREPARATION

def normalize_numeric_value(value):
    """Convert numeric strings using either decimal comma or decimal point.

    If both separators occur, a comma is treated as a thousands separator
    (e.g. '1,234.56'). If only a comma occurs, it is treated as a decimal
    separator (e.g. '12,56'). Native numeric values are left unchanged.
    """
    if pd.isna(value):
        return value
    if isinstance(value, (int, float, np.number)):
        return value

    value = str(value).strip().replace(" ", "")
    if "," in value and "." in value:
        value = value.replace(",", "")
    elif "," in value:
        value = value.replace(",", ".")
    return value


def prepare_data(df):
    if df.empty:
        raise ValueError("No IPO data retrieved.")

    # Map API field names to consistent internal names.
    df = df.rename(columns={
        "company": "company_name",
        "first_day_return_pct": "first_day_return",
        "return_1m_pct": "return_1m",
        "return_3m_pct": "return_3m",
        "return_6m_pct": "return_6m",
        "return_1y_pct": "return_1y",
        "excess_vs_spx_1m_pct": "excess_vs_spx_1m",
        "excess_vs_ixic_1m_pct": "excess_vs_ixic_1m",
        "excess_vs_dji_1m_pct": "excess_vs_dji_1m"
    })

    required_columns = [
        "symbol", "company_name", "ipo_date", "offer_price",
        "first_day_return", "sector", "industry"
    ]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing API fields: {missing}. Received: {list(df.columns)}"
        )

    # Dates
    df["ipo_date"] = pd.to_datetime(df["ipo_date"], errors="coerce")
    df["year"] = df["ipo_date"].dt.year

    # Convert numeric fields. A comma in a numeric string is treated as a
    # decimal separator unless a dot is also present (thousands separator case).
    numeric_columns = [
        "offer_price", "shares_offered", "gross_proceeds",
        "first_day_return", "return_1w", "return_1m", "return_3m",
        "return_6m", "return_1y", "current_vs_offer",
        "excess_vs_spx_1m", "excess_vs_spx_3m", "excess_vs_spx_6m",
        "excess_vs_spx_1y", "excess_vs_ixic_1m", "excess_vs_ixic_3m",
        "excess_vs_ixic_6m", "excess_vs_ixic_1y", "excess_vs_dji_1m",
        "excess_vs_dji_3m", "excess_vs_dji_6m", "excess_vs_dji_1y"
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].map(normalize_numeric_value),
                errors="coerce"
            )

    # Clean remaining text fields only AFTER numeric conversion. This removes
    # commas from labels such as 'Airbnb, Inc.' without corrupting decimal
    # strings such as '12,56' (which have already become 12.56).
    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for col in text_columns:
        df[col] = df[col].map(
            lambda value: value.replace(",", "").strip()
            if isinstance(value, str) else value
        )

    # Remove duplicates, restrict dates, and exclude non-IPO listing types
    # only if the API supplies a deal_type field.
    df = df.drop_duplicates(subset=["symbol", "ipo_date"])
    df = df[df["year"].between(START_YEAR, END_YEAR)].copy()

    if "deal_type" in df.columns:
        df = df[df["deal_type"].astype(str).str.lower().eq("ipo")].copy()

    return df


# TECHNOLOGY CLASSIFICATION

def classify_tech(row):
    company = str(row.get("company_name", "")).lower()
    symbol = str(row.get("symbol", "")).upper()
    sector = str(row.get("sector", "")).lower()
    industry = str(row.get("industry", "")).lower()
    combined = sector + " " + industry

    matches = [keyword for keyword in TECH_KEYWORDS if keyword in combined]

    if "technology" in sector:
        matches.append("Technology sector")

    # Explicit manual inclusion: Airbnb (ticker ABNB).
    if "airbnb" in company or symbol == "ABNB":
        matches.append("Manual inclusion: Airbnb")

    # Avoid classifying biotechnology as IT based only on the generic word
    # 'technology'. Keep any other independent technology match.
    if "biotechnology" in industry:
        matches = [m for m in matches if m not in {"technology", "Technology sector"}]
        if "airbnb" not in company and symbol != "ABNB":
            pass

    # Deduplicate while preserving order.
    matches = list(dict.fromkeys(matches))
    return bool(matches), ", ".join(matches)


def filter_technology(df):
    """Add classification columns to the full dataframe and return tech rows.

    The classification columns are deliberately added to df itself so that
    the full-universe review export can include both accepted and rejected IPOs.
    """
    classification = df.apply(classify_tech, axis=1)
    df["is_tech"] = [result[0] for result in classification]
    df["tech_match_reason"] = [result[1] for result in classification]
    return df[df["is_tech"]].copy()


# INDICATIVE COMPANY DESCRIPTIONS

def create_description(row):
    sector = row.get("sector", "Unknown sector")
    industry = row.get("industry", "Unknown industry")
    return f"Company classified in the {sector} sector, {industry} industry."


def add_descriptions(df):
    df = df.copy()
    df["activity_description"] = df.apply(create_description, axis=1)
    return df


# DESCRIPTIVE STATISTICS
RETURN_COLUMNS = {
    "First day": "first_day_return",
    "1 week": "return_1w",
    "1 month": "return_1m",
    "3 months": "return_3m",
    "6 months": "return_6m",
    "1 year": "return_1y",
    "Latest available": "current_vs_offer"
}


def calculate_statistics(df, group_name):
    results = []
    for horizon, column in RETURN_COLUMNS.items():
        if column not in df.columns:
            continue
        values = df[column].dropna()
        if values.empty:
            continue

        results.append({
            "group": group_name,
            "horizon": horizon,
            "sample_size": len(values),
            "mean": values.mean(),
            "median": values.median(),
            "std": values.std(),
            "min": values.min(),
            "max": values.max(),
            "p5": values.quantile(0.05),
            "p10": values.quantile(0.10),
            "p25": values.quantile(0.25),
            "p75": values.quantile(0.75),
            "p90": values.quantile(0.90),
            "p95": values.quantile(0.95),
            "negative_pct": (values < 0).mean() * 100,
            "loss_20_pct": (values <= -20).mean() * 100,
            "loss_50_pct": (values <= -50).mean() * 100,
            "loss_80_pct": (values <= -80).mean() * 100,
            "gain_100_pct": (values >= 100).mean() * 100,
            "gain_200_pct": (values >= 200).mean() * 100,
            "gain_500_pct": (values >= 500).mean() * 100,
            "skewness": values.skew(),
            # pandas kurt() reports excess kurtosis (normal distribution = 0).
            "kurtosis": values.kurt()
        })
    return results


def yearly_statistics(df):
    results = []
    for year, group in df.groupby("year"):
        results.extend(calculate_statistics(group, str(year)))
    return pd.DataFrame(results)


# EXPORT HELPERS: CSV + FORMATTED XLSX

def clean_for_export(df):
    """Remove commas from text cells, without converting numeric cells to text."""
    output = df.copy()
    text_columns = output.select_dtypes(include=["object", "string"]).columns
    for col in text_columns:
        output[col] = output[col].map(
            lambda value: value.replace(",", "").strip()
            if isinstance(value, str) else value
        )
    return output


def export_table(df, filename):
    """Write a CSV and a native Excel workbook with numeric cell formats."""
    output = clean_for_export(df)
    csv_path = OUTPUT_DIR / f"{filename}.csv"
    xlsx_path = OUTPUT_DIR / f"{filename}.xlsx"

    # Keep comma-delimited CSV for portability. Text commas have been removed.
    output.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Native XLSX avoids Excel having to guess decimal and delimiter settings.
    output.to_excel(xlsx_path, index=False, engine="openpyxl")

    workbook = load_workbook(xlsx_path)
    worksheet = workbook.active
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions

    headers = {cell.column: cell.value for cell in worksheet[1]}
    integer_columns = {"year", "sample_size", "shares_offered"}
    date_columns = {"ipo_date"}

    for col_idx, header in headers.items():
        column_letter = get_column_letter(col_idx)
        for row_idx in range(2, worksheet.max_row + 1):
            cell = worksheet.cell(row=row_idx, column=col_idx)
            if cell.value is None:
                continue
            if header in date_columns:
                cell.number_format = "yyyy-mm-dd"
            elif isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool):
                if header in integer_columns:
                    cell.number_format = "#,##0"
                elif header == "gross_proceeds":
                    cell.number_format = "#,##0.00"
                else:
                    # Returns and probability columns are expressed in
                    # percentage points (e.g. 25 means +25%), not Excel fractions.
                    cell.number_format = "0.00"

        # Set readable widths without making very long text columns enormous.
        values = [str(worksheet.cell(row=r, column=col_idx).value or "")
                  for r in range(1, min(worksheet.max_row, 200) + 1)]
        width = min(max(max((len(v) for v in values), default=10) + 2, 12), 45)
        worksheet.column_dimensions[column_letter].width = width

    workbook.save(xlsx_path)
    print(f"Created: {csv_path.resolve()}")
    print(f"Created: {xlsx_path.resolve()}")


# EXECUTION

def main():
    print("\n=== DOWNLOADING DATA ===")
    df = download_all()
    print("\nTotal records:", len(df))
    df = prepare_data(df)

    # Complete IPO universe
    export_table(df, "ipo_all")

    print("\n=== CLASSIFICATION ===")
    tech = filter_technology(df)
    print("Technology IPOs:", len(tech))

    # Sanity check: inspect raw first-day return values and units.
    print("\n=== FIRST-DAY RETURN CHECK ===")
    print(tech["first_day_return"].describe())
    print(tech["first_day_return"].head(10))

    # All IPOs, including those rejected by the technology classifier.
    classification_review = df[[
        "company_name", "symbol", "ipo_date", "sector", "industry",
        "is_tech", "tech_match_reason"
    ]]
    export_table(classification_review, "ipo_classification_review")

    # Firm-level returns for IPOs classified as technology (is_tech == True).
    # Each company occupies one row; each available time horizon has its own
    # column. Horizons absent from the API schema are simply omitted.
    individual_return_columns = [
        (label, column)
        for label, column in RETURN_COLUMNS.items()
        if column in tech.columns
    ]
    individual_returns = tech[[
        "company_name", "symbol", "ipo_date", "sector", "industry",
        "tech_match_reason"
    ]].copy()
    for label, column in individual_return_columns:
        individual_returns[label] = tech[column]

    # Count company-level performance patterns across all return horizons
    # actually available for each IPO. Missing horizons are ignored, and a
    # company must have at least one observed return to be eligible.
    available_horizon_labels = [label for label, _ in individual_return_columns]
    if available_horizon_labels:
        observed_returns = individual_returns[available_horizon_labels]
        individual_returns["observed_return_horizons"] = observed_returns.notna().sum(axis=1)
        has_observed_return = individual_returns["observed_return_horizons"] > 0
        highest_observed_return = observed_returns.max(axis=1, skipna=True)

        # Every observed return must be strictly below +50%.
        individual_returns["never_reached_+50pct"] = (
            has_observed_return & (highest_observed_return < 50)
        )
        # Every observed return must be strictly below 0%.
        individual_returns["negative_at_all_observed_horizons"] = (
            has_observed_return & (highest_observed_return < 0)
        )

        eligible_count = int(has_observed_return.sum())
        threshold_summary = pd.DataFrame([
            {
                "criterion": "Never reached +50%",
                "definition": "Every non-missing available return horizon is strictly below +50%.",
                "company_count": int(individual_returns["never_reached_+50pct"].sum()),
                "eligible_company_count": eligible_count,
                "percentage_of_eligible_companies": (
                    individual_returns["never_reached_+50pct"].sum() / eligible_count * 100
                    if eligible_count else np.nan
                )
            },
            {
                "criterion": "Negative at every observed horizon",
                "definition": "Every non-missing available return horizon is strictly below 0%.",
                "company_count": int(individual_returns["negative_at_all_observed_horizons"].sum()),
                "eligible_company_count": eligible_count,
                "percentage_of_eligible_companies": (
                    individual_returns["negative_at_all_observed_horizons"].sum() / eligible_count * 100
                    if eligible_count else np.nan
                )
            }
        ])
        export_table(threshold_summary, "ipo_tech_performance_thresholds")
    else:
        print("No return-horizon columns are available; threshold counts were not calculated.")

    export_table(individual_returns, "ipo_tech_individual_returns")

    tech = add_descriptions(tech)
    print("\nTechnology IPOs:", len(tech))
    export_table(tech, "ipo_tech_all")

    review = tech[[
        "company_name", "symbol", "ipo_date", "sector", "industry",
        "tech_match_reason", "activity_description"
    ]]
    export_table(review, "ipo_tech_review")

    # Statistics are exported to CSV/XLSX without printing tables to the console.
    overall = pd.DataFrame(calculate_statistics(tech, "All technology IPOs"))
    export_table(overall, "ipo_tech_statistics")

    yearly = yearly_statistics(tech)
    export_table(yearly, "ipo_tech_yearly")

    print("\n=== DATA QUALITY ===")
    for horizon, column in RETURN_COLUMNS.items():
        if column in tech.columns:
            missing = tech[column].isna().mean() * 100
            available = tech[column].notna().sum()
            print(f"{horizon}: {available} available; {missing:.1f}% missing")

    print("\n=== COMPLETED ===")
    print("Results saved in:", OUTPUT_DIR.resolve())
    print("Each dataset is exported in both CSV and XLSX format.")


if __name__ == "__main__":
    main()

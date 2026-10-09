import warnings

import pandas as pd


COMPOSITION_SUM_TOLERANCE = 5e-4
MAX_WARNING_EXAMPLES = 10


class CompositionBalanceWarning(UserWarning):
    """Warning raised when child composition fractions do not sum to one."""


def warn_for_unbalanced_compositions(
    composition_df: pd.DataFrame,
    tolerance: float = COMPOSITION_SUM_TOLERANCE,
) -> None:
    """Warn about parent resources whose child fractions do not sum to one.

    The check is informational: incomplete compositions remain valid model input
    and model execution continues. Values such as ``n/a`` are treated as empty
    hierarchy levels, consistently with the recovery model input processing.
    """
    df = composition_df.copy()
    layer_columns = ["Layer 1", "Layer 2", "Layer 3", "Layer 4"]
    df[layer_columns] = df[layer_columns].replace(
        {"n/a": "", "N/A": "", "NA": ""}
    ).fillna("")

    context_columns = [
        column
        for column in [
            "Waste Stream",
            "Location",
            "Year",
            "Scenario",
            "additionalSpecification",
            "Stock/ID",
        ]
        if column in df.columns
    ]

    levels = [
        (
            "components within products",
            (df["Layer 2"] != "") & (df["Layer 3"] == "") & (df["Layer 4"] == ""),
            ["Layer 1"],
        ),
        (
            "materials within components",
            (df["Layer 3"] != "") & (df["Layer 4"] == ""),
            ["Layer 1", "Layer 2"],
        ),
        (
            "elements within materials",
            df["Layer 4"] != "",
            ["Layer 1", "Layer 2", "Layer 3"],
        ),
    ]

    for level_name, row_mask, parent_columns in levels:
        level_df = df.loc[row_mask].copy()
        if level_df.empty:
            continue

        group_columns = context_columns + parent_columns
        sums = level_df.groupby(group_columns, dropna=False)["Value"].sum()
        unbalanced = sums[(sums - 1.0).abs() > tolerance]
        if unbalanced.empty:
            continue

        examples = []
        for parent, value in unbalanced.head(MAX_WARNING_EXAMPLES).items():
            parent_values = parent if isinstance(parent, tuple) else (parent,)
            label = ", ".join(
                f"{column}={parent_value}"
                for column, parent_value in zip(group_columns, parent_values)
            )
            examples.append(f"[{label}] sums to {value:.6g}")

        omitted = len(unbalanced) - len(examples)
        suffix = f"; {omitted} more" if omitted else ""
        warnings.warn(
            f"Composition fractions for {level_name} do not sum to 1 within "
            f"tolerance {tolerance:g} for {len(unbalanced)} parent resource(s): "
            + "; ".join(examples)
            + suffix,
            CompositionBalanceWarning,
            stacklevel=2,
        )

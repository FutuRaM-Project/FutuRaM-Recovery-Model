# User Guide — Recovery Model

**Author:** Harmjan de Vries  
**Date:** 21 November 2024

## Introduction

This document contains instructions for using the recovery model and documents the model's input-data format.

The recovery model computes material flows for a system with multiple resource layers. For example, elements are contained in materials, materials are contained in components, and components are contained in products. The model computes flows at each of these levels. For detailed information about how the recovery model works, consult the code documentation in `doc/Recovery_model_documentation.pdf`.

The model requires three CSV input files containing compositions, transfer coefficients, and inflows. Store all three files in the same input directory.

To run the model:

1. Create a folder for your data with a subfolder named `input_data`.
2. Place the composition, transfer-coefficient, and inflow files in `input_data`, using the filenames and column definitions described below.
3. Open `run_model.py` and set `data_folder` to the path of your data folder. If your layer names differ from `product`, `component`, `material`, and `element`, specify the applicable layer names.
4. Execute the Python file.

The following sections describe the required input formats.

## Transfer coefficients

**Filename:** `TCs.csv`

### Columns

- **Year** (optional): Year to which the transfer coefficient belongs.
- **Scenario** (optional): Scenario to which the transfer coefficient belongs.
- **Location** (optional): Location to which the transfer coefficient belongs.
- **additionalSpecification** (optional): Additional specification for the transfer coefficient.
- **Input_FlowID:** Stock/flow ID of the input flow.
- **Input_layer:** Layer to which the input resource belongs, such as product, component, or material.
- **Input_layer_key:** Input resource.
- **Output_FlowID:** Stock/flow ID of the output flow.
- **TC_target_layer:** Layer to which the output resource belongs.
- **TC_target_key:** Output resource.
- **value:** Value of the transfer coefficient.

### Example

![Example transfer-coefficient row](user-guide-assets/media/image1.png)

The example indicates that 32% of material M2 embedded in component C1 is preserved between flow F2 and flow F5.

> **Note:** An asterisk can be used to apply the same transfer coefficient to all resources in a layer. For example, `P*` as the input-layer key denotes that the coefficient applies to all input products.

## Compositions

**Filename:** `composition.csv`

### Columns

- **Year** (optional): Year to which the composition data point belongs.
- **Scenario** (optional): Scenario to which the composition data point belongs.
- **Location** (optional): Location to which the composition data point belongs.
- **additionalSpecification** (optional): Additional specification for the data point.
- **Stock/ID:** Stock/flow ID of the flow containing the resource.
- **Layer 1, Layer 2, Layer 3, Layer 4:** Hierarchical resources to which the composition data point applies.
- **Value:** Composition fraction describing the contribution of the rightmost specified resource to its parent resource.

### Example

![Example composition row](user-guide-assets/media/image2.png)

The example indicates that material M1 composes 52% of component C1 when component C1 is contained in product P1.

## Inflows

**Filename:** `inputs.csv`

### Columns

- **Year** (optional): Year of the inflow.
- **Scenario** (optional): Scenario associated with the inflow.
- **Location** (optional): Location associated with the inflow.
- **additionalSpecification** (optional): Additional specification for the inflow.
- **Stock/Flow ID:** Stock/flow ID of the inflow.
- **Substance_main_parent:** Inflow resource. This must be a resource from the highest hierarchical layer.
- **Value:** Quantity of the resource in the inflow. The model is agnostic to the unit used, but units must be consistent across inflows.

> **Note:** The inflow file determines which combinations of years, scenarios, locations, and additional specifications the model analyzes. These columns are optional, and any subset may be provided. When one of these dimensions is specified in the inflow file, the model uses matching entries from the transfer-coefficient and composition files when available. If the dimension is absent from those files, their data are assumed to apply to all values of that dimension.

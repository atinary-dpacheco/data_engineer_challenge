# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the "Technical Challenge: The Scientific Data Bridge" from Atinary Technologies - a data engineering challenge focused on processing and harmonizing scientific chemistry data (Buchwald-Hartwig reactions). The task involves parsing binary Protobuf files from the Open Reaction Database (ORD), extracting semantic information about chemical reactions, and transforming hierarchical data into standardized formats.

## Data Files

- `ord_challenge_subset.pb.gz` - Binary Protobuf data file (gzip compressed), contains 20 chemical reactions
- `ord_challenge_subset.json` - JSON representation of the same data for easier inspection
- `get_bh_dataset.py` - Data collection script (for reference only, not part of the challenge)

## Data Structure

The dataset follows the ORD schema with reactions containing:
- **inputs**: Chemical inputs organized by role (Base, metal and ligand, aryl halide, amine)
- **identifiers**: Reaction classification and custom indices
- **conditions**: Temperature and other reaction conditions
- **outcomes**: Products with yields
- **provenance**: Source information (publication URLs, experimenter, timestamps)

## Key Technical Details

- **Python 3.10+** is the minimum required version
- **Libraries commonly used**: `ord-schema`, `protobuf`, `pandas`, `rdkit`
- To parse the Protobuf file, use `ord-schema` which provides message definitions for ORD data
- SMILES strings are the standard representation for molecular structures

## Challenge Deliverables

1. `extraction_script.py` - Python script to parse and extract data
2. `processed_data.csv` - Standardized output with columns for reactants, products, yields, and conditions
3. `schema.dbml` or `schema.json` - Database architecture proposal
4. `DESIGN.md` - Design document explaining methodology and architectural decisions

## Data Processing Considerations

- Molecules must be identified semantically (aryl halides contain halogens, amines contain nitrogen)
- Handle molecules that have both halogen and nitrogen atoms (ambiguous classification)
- Yield percentages may come from "UPLC Analysis" or "Product Measurement" - prefer UPLC when available
- Units vary across records and need normalization
- Two data sources are combined: AstraZeneca ELN (10 reactions) and Merck HTE (10 reactions)

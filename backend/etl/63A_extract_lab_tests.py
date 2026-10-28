import os
import pandas as pd

# ============================================================
# STEP 63A
# Extract unique laboratory tests from lab_results.csv
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "lab_results.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "lab_tests_reference.csv"
)

CHUNK_SIZE = 250_000

REQUIRED_COLUMNS = [
    "Test_Name",
    "Unit",
    "Reference_Range"
]


def main():

    print("=" * 70)
    print("STEP 63A - EXTRACT LAB TEST MASTER DATA")
    print("=" * 70)

    print(f"\nInput file:")
    print(INPUT_FILE)

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"\nERROR: lab_results.csv not found:\n{INPUT_FILE}"
        )

    print("\nReading CSV in chunks...")
    print(f"Chunk size: {CHUNK_SIZE:,} rows")

    unique_tests = set()
    total_rows = 0

    reader = pd.read_csv(
        INPUT_FILE,
        usecols=REQUIRED_COLUMNS,
        chunksize=CHUNK_SIZE,
        dtype={
            "Test_Name": "string",
            "Unit": "string",
            "Reference_Range": "string"
        },
        low_memory=True
    )

    for chunk_number, chunk in enumerate(reader, start=1):

        total_rows += len(chunk)

        # Remove completely empty test names
        chunk = chunk.dropna(subset=["Test_Name"])

        # Normalize whitespace
        for column in REQUIRED_COLUMNS:
            chunk[column] = (
                chunk[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

        # Store unique combinations
        for row in chunk.itertuples(index=False, name=None):
            test_name, unit, reference_range = row

            if test_name:
                unique_tests.add(
                    (
                        test_name,
                        unit,
                        reference_range
                    )
                )

        print(
            f"Processed chunk {chunk_number:02d} | "
            f"Rows: {total_rows:,} | "
            f"Unique test combinations: {len(unique_tests):,}"
        )

    # --------------------------------------------------------
    # Convert unique combinations to DataFrame
    # --------------------------------------------------------

    result = pd.DataFrame(
        sorted(
            unique_tests,
            key=lambda x: (
                x[0].lower(),
                x[1].lower(),
                x[2].lower()
            )
        ),
        columns=[
            "Test_Name",
            "Unit",
            "Reference_Range"
        ]
    )

    # Additional cleanup
    result["Test_Name"] = result["Test_Name"].str.strip()
    result["Unit"] = result["Unit"].str.strip()
    result["Reference_Range"] = result["Reference_Range"].str.strip()

    result = result.drop_duplicates()

    # Assign deterministic test codes
    result.insert(
        0,
        "Test_Code",
        [
            f"LABT-{i:04d}"
            for i in range(1, len(result) + 1)
        ]
    )

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    result.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\n" + "=" * 70)
    print("STEP 63A COMPLETED")
    print("=" * 70)

    print(f"\nTotal source rows processed : {total_rows:,}")
    print(f"Unique lab test combinations: {len(result):,}")

    print(f"\nOutput file:")
    print(OUTPUT_FILE)

    print("\nFirst records:")
    print(result.head(20).to_string(index=False))

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
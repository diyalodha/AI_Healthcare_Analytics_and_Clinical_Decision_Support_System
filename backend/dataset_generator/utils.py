"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : utils.py

Purpose :
Reusable functions for synthetic healthcare dataset generation.

Author : Diya Lodha & Team
===========================================================
"""


import uuid
import random
import os

import pandas as pd

from faker import Faker
from datetime import datetime, timedelta

import config



# ==========================================================
# Faker Setup
# ==========================================================


fake = Faker()

Faker.seed(
    config.RANDOM_SEED
)


random.seed(
    config.RANDOM_SEED
)



# ==========================================================
# UUID Generator
# ==========================================================


def generate_uuid():

    return str(
        uuid.uuid4()
    )



# ==========================================================
# Fast Random Row Selection
# ==========================================================


def random_row(dataframe):

    return dataframe.iloc[
        random.randint(
            0,
            len(dataframe)-1
        )
    ]



# ==========================================================
# Date Generator
# ==========================================================


def generate_date(
        start_year=2015,
        end_year=2026
):

    start_date = datetime(
        start_year,
        1,
        1
    )


    end_date = datetime(
        end_year,
        12,
        31
    )


    days = (
        end_date-start_date
    ).days


    return (
        start_date +
        timedelta(
            days=random.randint(
                0,
                days
            )
        )
    ).date()



# ==========================================================
# Random Choice
# ==========================================================


def random_value(values):

    return random.choice(
        values
    )



# ==========================================================
# Save Reference DataFrame
# ==========================================================

def save_reference_dataframe(
        dataframe,
        filename
):

    path = os.path.join(
        config.REFERENCE_DIR,
        filename
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        f"Created {filename}"
    )


# ==========================================================
# Save Synthetic DataFrame
# ==========================================================

def save_dataframe(
        dataframe,
        filename
):

    path = os.path.join(
        config.SYNTHETIC_DIR,
        filename
    )

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        f"Created {filename}"
    )


# ==========================================================
# Save Synthetic DataFrame (Chunk / Append)
# ==========================================================

def save_dataframe_chunked(
        dataframe,
        filename,
        mode="w",
        header=True
):

    path = os.path.join(
        config.SYNTHETIC_DIR,
        filename
    )

    dataframe.to_csv(
        path,
        mode=mode,
        header=header,
        index=False
    )

# ==========================================================
# Progress Display
# ==========================================================


def show_progress(message):

    print("\n")
    print("="*70)
    print(message)
    print("="*70)
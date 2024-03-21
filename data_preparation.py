import logging
from enum import Enum

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

Process = Enum("process", ["bulk", "SOI", "SOS", "unknown", "FinFET"])
PAType = Enum("type", ("analog", "digital", "unknown"))


class PASpec(BaseModel):
    year: int = Field(..., ge=1800)
    month: int = Field(..., ge=0, le=12)
    author_name: str = ""
    paper_title: str = ""
    process: Process
    frequency: float = Field(..., ge=0)
    sat_power: float
    pae_max: float = Field(..., ge=0, le=100)
    P1dB: float
    PAE_1dB: float
    Gain: float
    EVM: float
    modulation_speed: float
    average_pout: float
    average_pae: float = Field(..., ge=0, le=100)
    modulation_type: str
    PA_type: PAType
    node: int


if __name__ == "__main__":
    logging.basicConfig(filename="prep.log", level=logging.INFO, filemode="w")
    for techno in [
        "CMOS",
    ]:  # "SiGe", "GaN", "GaAs", "InP", "LDMOS", "Others"]:
        data = pd.read_excel(
            io="data/raw/PA-Survey-v8.xlsx", sheet_name=techno, usecols="B:V"
        )
        data.rename(
            columns={
                "Process (CMOS_Bulk, CMOS_SOI, SiGe)": "process",
                "Year": "year",
                "Month": "month",
                "Last Name (1st Author)": "author_name",
                "Paper Title": "paper_title",
                "Frequency (GHz)": "frequency",
                "Psat (dBm)": "sat_power",
                "Process node": "node",
                "PAEmax (%)": "pae_max",
                "P1dB (dBm)": "P1dB",
                "PAE_1dB (%)": "PAE_1dB",
                "Gain (dB)": "Gain",
                "EVM (dB)": "EVM",
                "Modulation Speed (Msym/s)": "modulation_speed",
                "Average Pout (dBm)": "average_pout",
                "Average PAE (%)": "average_pae",
                "RF PA Note (Modulation Type)": "modulation_type",
                "RF PA Note (Analog PA or Digital PA)": "PA_type",
            },
            inplace=True,
        )
        clean_data = pd.DataFrame(columns=PASpec.model_fields)
        for d in data.to_dict(orient="records"):
            match str(d["process"]).strip():
                case "CMOS_Bulk" | "CMOS":
                    d["process"] = Process.bulk
                case (
                    "CMOS_SOI"
                    | "CMOS_PD_SOI"
                    | "CMOS_FD_SOI"
                    | "CMOS_PDSOI"
                    | "CMOS_FDSOI"
                    | "PD_SOI"
                    | "FD_SOI"
                ):
                    d["process"] = Process.SOI
                case "CMOS_SOS":
                    d["process"] = Process.SOS
                case "CMOS_FinFet":
                    d["process"] = Process.FinFET
                case np.nan:
                    d["process"] = Process.unknown
            match d["PA_type"]:
                case "analog" | "Analog":
                    d["PA_type"] = PAType.analog
                case nan:
                    d["PA_type"] = PAType.unknown
            if d["month"] is np.nan or d["month"] == "Early Access":
                d["month"] = 0
            if d["frequency"] is np.nan:
                d["frequency"] = 0
            d["node"] = str(d["node"]).lower().strip().replace("nm", "")
            d["node"] = 0 if d["node"] == "na" else d["node"]
            try:
                cd = PASpec(**d)
                clean_data.loc[len(clean_data)] = dict(cd)
            except ValidationError as e:
                logging.info(e)
                continue
        clean_data.to_csv(f"data/cleaned/{techno}.csv")

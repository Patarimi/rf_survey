import logging
from enum import Enum
from typing_extensions import Annotated, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

Process = Enum("process", ["bulk", "SOI", "SOS", "unknown", "FinFET", "SiGe", "BiCMOS"])
PAType = Enum("type", ("analog", "digital", "unknown"))


class PASpec(BaseModel):
    year: int = Field(..., ge=1800)
    month: Optional[Annotated[int, Field(ge=0, le=12)]] = 0
    author_name: str = ""
    paper_title: str = ""
    process: Process
    frequency: Optional[Annotated[float, Field(ge=0)]] = float("nan")
    sat_power: Optional[float] = float("nan")
    pae_max: Annotated[float, Field(ge=0, le=100)] = float("nan")
    P1dB: Optional[float] = float("nan")
    PAE_1dB: Optional[float] = float("nan")
    gain: Annotated[float, Field(le=100)] = float("nan")
    EVM: float = float("nan")
    modulation_speed: float = float("nan")
    average_pout: float = float("nan")
    average_pae: Optional[float] = float("nan")
    modulation_type: str = ""
    PA_type: PAType = PAType.unknown
    node: int = -1


if __name__ == "__main__":
    logging.basicConfig(filename="../prep.log", level=logging.INFO, filemode="w")
    for techno in [
        "SiGe",
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
                "Gain (dB)": "gain",
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
        for i, d in enumerate(data.to_dict(orient="records")):
            match str(d["process"]).replace(" ", "").replace("_", "").upper():
                case "CMOS_BULK" | "CMOS":
                    d["process"] = Process.bulk
                case "CMOSSOI" | "CMOSPDSOI" | "CMOSFDSOI" | "PDSOI" | "FDSOI":
                    d["process"] = Process.SOI
                case "CMOSSOS":
                    d["process"] = Process.SOS
                case "CMOSFINFET":
                    d["process"] = Process.FinFET
                case "SIGE" | "SIGEHBT":
                    d["process"] = Process.SiGe
                case "BICMOS" | "SIGEBICMOS":
                    d["process"] = Process.BiCMOS
                case np.nan:
                    d["process"] = Process.unknown
                case _:
                    logging.info(f"Line {i}: Could not parse {d["process"]}")
            match d["PA_type"]:
                case "analog" | "Analog":
                    d["PA_type"] = PAType.analog
                case nan:
                    d["PA_type"] = PAType.unknown
            if str(d["month"]).lower() == "early access":
                d["month"] = 0
            d["node"] = str(d["node"]).lower().strip()
            for radical in ("nm", "sige", "bi", "cmos", "hbt"):
                d["node"] = d["node"].replace(radical, "")
            d["node"] = d["node"].strip("_() ")
            if "um" in d["node"]:
                d["node"] = float(d["node"].replace("um", "").strip()) * 1000
            d["modulation_speed"] = (
                str(d["modulation_speed"]).lower().rstrip("-sy/mbpsc ")
            )
            for field in (
                "month",
                "year",
                "frequency",
                "pae_max",
                "average_pae",
                "average_pout",
                "gain",
                "sat_power",
                "P1dB",
                "PAE_1dB",
                "node",
                "EVM",
                "modulation_speed",
            ):
                data_s = str(d[field])
                if "/" in data_s:
                    data_s = data_s.split("/")[0]
                data_s = data_s.lower().rstrip("^(sde)* txhp")
                try:
                    d[field] = float(data_s)
                    if data_s == "nan" or data_s.strip() == "":
                        del d[field]
                except ValueError:
                    logging.info(
                        f"line {i}: Error in {field} field: {d[field]} parse as {data_s}"
                    )
                    del d[field]
            if d["modulation_type"] is np.nan:
                d["modulation_type"] = "unknown"

            try:
                cd = dict(PASpec(**d))
                clean_data.loc[len(clean_data)] = cd
            except ValidationError as e:
                if str(d["author_name"]) == "nan":
                    # These are empty rows at the end of the sheet
                    continue
                logging.info(f"line {i}: {e}")
                continue
        clean_data.to_csv(f"data/cleaned/{techno}.csv")

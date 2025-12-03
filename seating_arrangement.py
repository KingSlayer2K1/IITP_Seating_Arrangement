#!/usr/bin/env python3
"""
seating_arrangement.py

Main driver for seating allocation -> output pipeline.

This script:
  - reads timetable, roll map, room capacities
  - performs clash checks
  - calls allocator
  - normalizes allocator output to subject -> (room -> [rolls])
  - exports results (Excel + PDFs + organized folders) using output.exporter
"""

import argparse
import os
import logging
from typing import Any, Dict, List

from input.timetable_reader import TimetableReader
from input.roll_reader import read_subject_rolls, read_roll_name_map
from input.room_capacity_reader import read_room_capacity

from allocation.clash_checker import check_clashes
from allocation.allocator import allocate_students_to_rooms

from output.excel_writer import write_overall_output, write_seats_left
from utils.logger import get_logger

# Optional exporter (Excel + PDF + folder generation)
try:
    from output.exporter import export_all  # type: ignore
    HAS_EXPORTER = True
except Exception:
    HAS_EXPORTER = False


# ---------------------------------------------------------------
# NORMALIZER (unchanged, fully preserved)
# ---------------------------------------------------------------
def normalize_allocations(raw: Any, logger: logging.Logger) -> Dict[str, Dict[str, List[str]]]:
    """
    Ensure output shape:
        { subject: { room: [rolls] } }
    """
    if isinstance(raw, dict):
        sample_value = None
        if raw:
            sample_key = next(iter(raw))
            sample_value = raw[sample_key]

        # Case A — expected structure: subject -> room -> list
        if isinstance(sample_value, dict) or sample_value is None:
            for subj, room_data in raw.items():
                if room_data is None:
                    raw[subj] = {}
                    continue
                if not isinstance(room_data, dict):
                    if isinstance(room_data, list):
                        raw[subj] = {"MIXED": room_data}
                    else:
                        raise TypeError(f"Unexpected allocations[{subj}] type: {type(room_data)}")
                else:
                    for room, rolls in room_data.items():
                        if not isinstance(rolls, list):
                            raise TypeError(f"Allocations for {subj}/{room} must be list")
            return raw

        # Case B — dict(room -> rolls)
        if isinstance(sample_value, list):
            logger.warning("Allocator returned dict(room→rolls); wrapping into subject='MIXED'")
            wrapped = {"MIXED": {}}
            for room, rolls in raw.items():
                if not isinstance(rolls, list):
                    raise TypeError(f"Expected list for room {room}, got {type(rolls)}")
                wrapped["MIXED"][room] = rolls
            return wrapped

        raise TypeError("Unrecognized dict format for allocations")

    # Case C — list-based structures
    if isinstance(raw, list):
        normalized: Dict[str, Dict[str, List[str]]] = {}
        if not raw:
            return normalized

        first = raw[0]

        # list of tuples
        if isinstance(first, tuple) and (2 <= len(first) <= 3):
            for item in raw:
                if len(item) == 3:
                    subj, room, rolls = item
                else:
                    subj = "MIXED"
                    room, rolls = item
                if not isinstance(rolls, list):
                    raise TypeError("Rolls must be list")
                normalized.setdefault(subj, {}).setdefault(room, []).extend(rolls)
            return normalized

        # list of dicts
        if isinstance(first, dict):
            for item in raw:
                subj = item.get("subject") or item.get("subj") or "MIXED"
                room = item.get("room")
                rolls = item.get("rolls") or item.get("roll")

                if room is None or rolls is None:
                    if len(item) == 1:
                        room, rolls = next(iter(item.items()))
                    else:
                        raise TypeError("Malformed dict in allocations list")

                if not isinstance(rolls, list):
                    raise TypeError("Rolls must be list")

                normalized.setdefault(subj, {}).setdefault(room, []).extend(rolls)
            return normalized

        raise TypeError("Unrecognized list-based allocations structure")

    raise TypeError(f"Unsupported allocations type: {type(raw)}")


# ---------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="IITP Seating Arrangement Generator")
    parser.add_argument("--input", required=True, help="Input Excel file")
    parser.add_argument("--photos", required=False, default=None,
                        help="Folder with student photos (optional)")
    parser.add_argument("--output", required=True, help="Main output folder")
    parser.add_argument("--buffer", type=int, default=0, help="Seat buffer per room")
    parser.add_argument("--mode", choices=["dense", "sparse"], default="dense",
                        help="Seating mode")
    parser.add_argument("--log", default="errors.txt", help="Error log file")

    args = parser.parse_args()
    logger = get_logger(args.log)

    os.makedirs(args.output, exist_ok=True)

    logger.info("Reading timetable...")
    timetable = TimetableReader(args.input).read()

    logger.info("Reading roll-name map...")
    roll_name_map = read_roll_name_map(args.input)

    logger.info("Reading room capacities...")
    room_caps = read_room_capacity(args.input)

    logger.info("Starting seating allocation pipeline...")

    # timetable: [(date, session, [subjects])]
    for (date, session, subjects) in timetable:
        logger.info(f"=== Processing {date} / {session} ===")

        subject_rolls = {
            subj: read_subject_rolls(args.input, subj)
            for subj in subjects
        }

        # Clash check
        clash = check_clashes(subjects, subject_rolls)
        if clash:
            logger.error(f"❌ CLASH DETECTED: {clash}")
            print("\n❌ Clash detected — see log.\n")
            continue

        # Allocation
        try:
            allocations_raw, seats_left = allocate_students_to_rooms(
                subject_rolls=subject_rolls,
                room_caps=room_caps,
                buffer=args.buffer,
                mode=args.mode,
                logger=logger
            )
        except Exception as e:
            logger.exception("Allocator crashed: %s", e)
            print("Allocator failed — check log.")
            continue

        # Normalize
        try:
            allocations = normalize_allocations(allocations_raw, logger)
        except Exception as e:
            logger.exception("Normalization failure: %s", e)
            raise

        # Validate
        assigned_total = 0
        for subj, room_map in allocations.items():
            for room, rolls in room_map.items():
                if not isinstance(rolls, list):
                    raise TypeError(f"Room lists must be list, found {type(rolls)}")
                assigned_total += len(rolls)
        logger.info(f"Total assigned = {assigned_total}")

        # -------------------------------------------------------
        # EXPORT (Excel + PDFs + folder structure)
        # -------------------------------------------------------
        try:
            if HAS_EXPORTER:
                logger.info("Using exporter...")
                export_all(
                    args.output,         # ✅ FIXED
                    date,
                    session,
                    allocations,
                    seats_left,
                    roll_name_map,
                    args.photos
                )
            else:
                logger.info("Exporter missing — Excel only.")
                write_overall_output(args.output, date, session, allocations)
                write_seats_left(args.output, seats_left)

        except Exception as e:
            logger.exception("Export failed: %s", e)
            print("Export failed — see log.")
            continue

    print("\n Seating arrangement completed!")
    print(" Outputs stored in:", args.output)


if __name__ == "__main__":
    main()

"""
Administrative endpoints for development: clear persisted demo data
"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
from fastapi import Query

from src.api.routers.pill_identification import pill_identifier
from src.api.routers.medication_verification import medication_verifier

router = APIRouter()


@router.post('/clear-demo-data')
async def clear_demo_data(confirm: bool = Query(False)):
    """Clear demo data files: pill_database.json, medication_schedules.json, medications.json

    Requires confirm=true to actually delete files to avoid accidents.
    This endpoint removes on-disk JSON files and also clears the in-memory
    singletons so the running server immediately reflects an empty state.
    """
    if not confirm:
        raise HTTPException(status_code=400, detail='You must pass confirm=true to delete demo data')

    files = [
        Path('data/pill_database.json'),
        Path('data/medication_schedules.json'),
        Path('data/medications.json'),
        Path('data/dose_logs.json')
    ]

    removed = []
    for f in files:
        try:
            if f.exists():
                f.unlink()
                removed.append(str(f))
        except Exception:
            pass

    # Also clear in-memory singletons so the running server reflects the empty state
    try:
        pill_identifier.clear_database()
    except Exception:
        pass
    try:
        medication_verifier.clear_all_data()
    except Exception:
        pass

    return {"removed": removed}

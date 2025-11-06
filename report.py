def generate_report(diff, applied):
    return {
        "differences_detected": diff,
        "changes_applied": applied,
    }

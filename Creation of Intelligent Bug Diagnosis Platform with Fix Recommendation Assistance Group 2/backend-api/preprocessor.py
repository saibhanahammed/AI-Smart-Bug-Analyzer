import re

def clean_log_telemetry(text: str) -> str:
    """Removes HTML elements, normalizes spacing, and masks hex address clusters."""
    if not text:
        return ""
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Standardize whitespace and line endings
    text = re.sub(r'\s+', ' ', text)
    # Mask continuous hex strings or memory addresses
    text = re.sub(r'0x[0-9a-fA-F]+', '[HEX_ADDR]', text)
    return text.strip()
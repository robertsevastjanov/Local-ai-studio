
# Local AI Studio — Known Issues and Limitations

## ISSUE-001: Image generation returns a placeholder

**Type:** Missing Feature / Known Limitation  
**Priority:** High  
**Status:** Open

### Description
The application currently returns a solid pink placeholder image instead of generating an image based on the user's prompt.

### Steps to Reproduce
1. Start the FastAPI application.
2. Open http://127.0.0.1:8000/.
3. Enter a valid prompt: "A giant hornet flying over Riga".
4. Set steps to 8 and seed to 42.
5. Click Generate.

### Expected Result
The application generates an image corresponding to the user's prompt.

### Actual Result
The application displays a solid pink 512x512 image, regardless of the prompt.

### Root Cause
The current generator.py uses Pillow to create a fixed-color placeholder instead of invoking an AI image generation model.

### Suggested Resolution
Integrate a local text-to-image model and replace the placeholder implementation.

### Notes
This is an intentional development placeholder, not a newly discovered regression.

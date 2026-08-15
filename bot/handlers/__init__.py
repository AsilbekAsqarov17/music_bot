from .start import router as start_router
from .text_search import router as text_search_router
from .voice_recognition import router as voice_recognition_router

__all__ = ["start_router", "text_search_router", "voice_recognition_router"]
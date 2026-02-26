import re
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("api_security")

class PIIMaskingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts requests and responses to automatically 
    mask sensitive Personally Identifiable Information (PII) before it gets logged.
    """
    
    # Simple regex for finding 9-digit SSNs or Account Numbers
    SSN_PATTERN = re.compile(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b')
    # Simple regex for finding Emails
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

    def mask_string(self, text: str) -> str:
        # Mask SSN/Account numbers
        masked = self.SSN_PATTERN.sub('***-**-****', text)
        
        # Partially mask emails (show first character and domain)
        def email_replacer(match):
            email = match.group()
            user, domain = email.split('@')
            return f"{user[0]}***@{domain}"
            
        masked = self.EMAIL_PATTERN.sub(email_replacer, masked)
        return masked

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 1. Inspect the incoming request path/params and log it securely
        url_sampled = str(request.url)
        safe_url = self.mask_string(url_sampled)
        logger.info(f"Incoming Request: {request.method} {safe_url}")

        # 2. Process the request
        response = await call_next(request)
        
        # Note: In a real production system, you'd also want to inspect the 'Body' 
        # of the request/response, but that requires more complex async stream handling.
        
        return response

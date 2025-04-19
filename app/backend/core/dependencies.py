"""
Service dependencies module.
Contains factories and providers for dependency injection.
"""
from functools import lru_cache
from typing import Callable, Any, TypeVar, Optional, Dict, Type

from fastapi import Depends, Request

from app.backend.core.config import settings

# Type variable for service class types
T = TypeVar('T')

# Global service registry to avoid duplicate instantiations
_service_instances: Dict[Type, Any] = {}

def get_settings():
    """Get application settings.
    
    Returns:
        Application settings instance
    """
    return settings

@lru_cache()
def get_webhook_service():
    """Get webhook service instance.
    
    Returns:
        WebhookService: Initialized webhook service
    """
    from app.backend.services.webhook_service import WebhookService
    
    if WebhookService not in _service_instances:
        _service_instances[WebhookService] = WebhookService()
    return _service_instances[WebhookService]

def service_factory(service_class: Type[T], **kwargs) -> Callable[[], T]:
    """Create a dependency provider factory for a service class.
    
    Args:
        service_class: The service class to instantiate
        **kwargs: Additional kwargs to pass to the service constructor
        
    Returns:
        A callable dependency provider that returns the service instance
    """
    @lru_cache()
    def _get_service() -> T:
        # Only create a new instance if one doesn't exist
        if service_class not in _service_instances:
            _service_instances[service_class] = service_class(**kwargs)
        return _service_instances[service_class]
    
    return _get_service

def request_service_factory(
    service_class: Type[T], 
    **kwargs
) -> Callable[[Request], T]:
    """Create a dependency provider factory for a request-bound service.
    
    Args:
        service_class: The service class to instantiate
        **kwargs: Additional kwargs to pass to the service constructor
        
    Returns:
        A callable dependency provider that returns a new service instance for each request
    """
    def _get_request_service(request: Request) -> T:
        # Store the service in the request state
        service_key = f"service:{service_class.__name__}"
        
        # Create a new instance if one doesn't exist for this request
        if not hasattr(request.state, service_key):
            service_instance = service_class(request=request, **kwargs)
            setattr(request.state, service_key, service_instance)
            
        return getattr(request.state, service_key)
    
    return _get_request_service 
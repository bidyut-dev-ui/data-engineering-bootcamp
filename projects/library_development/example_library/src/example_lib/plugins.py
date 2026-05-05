"""
Plugin system for the example library.

This module demonstrates:
1. Plugin architecture patterns
2. Dynamic loading and registration
3. Plugin discovery and management
4. Hook systems and event handling
"""

import importlib
import inspect
import pkgutil
from typing import Any, Dict, List, Optional, Type, Callable, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import logging
from pathlib import Path

from .exceptions import PluginError

logger = logging.getLogger(__name__)


class Plugin(ABC):
    """
    Base class for all plugins.
    
    Plugins should inherit from this class and implement
    the required methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Get the plugin version."""
        pass
    
    @property
    def description(self) -> str:
        """Get the plugin description (optional)."""
        return ""
    
    @property
    def author(self) -> str:
        """Get the plugin author (optional)."""
        return ""
    
    def initialize(self) -> None:
        """
        Initialize the plugin.
        
        Called when the plugin is loaded. Use this for
        any setup that needs to happen before the plugin
        is used.
        """
        pass
    
    def cleanup(self) -> None:
        """
        Clean up the plugin.
        
        Called when the plugin is unloaded. Use this for
        any cleanup that needs to happen.
        """
        pass
    
    def get_config_schema(self) -> Optional[Dict[str, Any]]:
        """
        Get configuration schema for the plugin.
        
        Returns:
            Dictionary describing the configuration schema,
            or None if no configuration is needed.
        """
        return None
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate plugin configuration.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        return True


@dataclass
class PluginInfo:
    """Information about a registered plugin."""
    plugin_class: Type[Plugin]
    instance: Optional[Plugin] = None
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PluginManager:
    """
    Manages plugin loading, registration, and lifecycle.
    
    Features:
    - Dynamic plugin discovery
    - Plugin lifecycle management
    - Configuration management
    - Dependency resolution
    - Hook system integration
    """
    
    def __init__(self):
        """Initialize the plugin manager."""
        self._plugins: Dict[str, PluginInfo] = {}
        self._hooks: Dict[str, List[Callable]] = {}
        self._initialized = False
    
    def register_plugin(self, plugin_class: Type[Plugin], 
                       config: Optional[Dict[str, Any]] = None) -> str:
        """
        Register a plugin class.
        
        Args:
            plugin_class: Plugin class to register
            config: Plugin configuration
            
        Returns:
            Plugin ID
        """
        # Create plugin instance
        try:
            plugin_instance = plugin_class()
        except Exception as e:
            raise PluginError(
                f"Failed to instantiate plugin {plugin_class.__name__}: {e}",
                plugin_name=plugin_class.__name__
            ) from e
        
        # Get plugin name
        plugin_name = plugin_instance.name
        
        # Check if plugin already registered
        if plugin_name in self._plugins:
            logger.warning(f"Plugin '{plugin_name}' already registered, overwriting")
        
        # Store plugin info
        self._plugins[plugin_name] = PluginInfo(
            plugin_class=plugin_class,
            instance=plugin_instance,
            config=config or {},
            metadata={
                'module': plugin_class.__module__,
                'class': plugin_class.__name__,
            }
        )
        
        logger.info(f"Registered plugin: {plugin_name} v{plugin_instance.version}")
        
        return plugin_name
    
    def load_plugin_from_module(self, module_name: str, 
                               plugin_class_name: Optional[str] = None) -> str:
        """
        Load a plugin from a module.
        
        Args:
            module_name: Name of the module to load
            plugin_class_name: Name of the plugin class (if None, auto-discover)
            
        Returns:
            Plugin ID
        """
        try:
            # Import the module
            module = importlib.import_module(module_name)
            
            if plugin_class_name:
                # Load specific class
                plugin_class = getattr(module, plugin_class_name)
                if not inspect.isclass(plugin_class) or not issubclass(plugin_class, Plugin):
                    raise PluginError(
                        f"'{plugin_class_name}' is not a valid Plugin class",
                        plugin_name=plugin_class_name,
                        module=module_name
                    )
            else:
                # Auto-discover Plugin classes in the module
                plugin_classes = []
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Plugin) and 
                        obj != Plugin):
                        plugin_classes.append(obj)
                
                if not plugin_classes:
                    raise PluginError(
                        f"No Plugin classes found in module {module_name}",
                        module=module_name
                    )
                
                if len(plugin_classes) > 1:
                    logger.warning(
                        f"Multiple Plugin classes found in {module_name}, "
                        f"using first: {plugin_classes[0].__name__}"
                    )
                
                plugin_class = plugin_classes[0]
            
            # Register the plugin
            return self.register_plugin(plugin_class)
            
        except ImportError as e:
            raise PluginError(
                f"Failed to import module {module_name}: {e}",
                module=module_name
            ) from e
    
    def load_plugins_from_package(self, package_name: str) -> List[str]:
        """
        Load all plugins from a package.
        
        Args:
            package_name: Name of the package to scan
            
        Returns:
            List of plugin IDs loaded
        """
        loaded_plugins = []
        
        try:
            package = importlib.import_module(package_name)
            
            # Iterate through all modules in the package
            for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
                full_module_name = f"{package_name}.{module_name}"
                
                try:
                    plugin_id = self.load_plugin_from_module(full_module_name)
                    loaded_plugins.append(plugin_id)
                except PluginError as e:
                    logger.warning(f"Failed to load plugin from {full_module_name}: {e}")
                    continue
            
        except ImportError as e:
            raise PluginError(
                f"Failed to import package {package_name}: {e}",
                package=package_name
            ) from e
        
        return loaded_plugins
    
    def load_plugins_from_directory(self, directory: Union[str, Path]) -> List[str]:
        """
        Load plugins from a directory.
        
        Args:
            directory: Directory to scan for Python files
            
        Returns:
            List of plugin IDs loaded
        """
        directory = Path(directory)
        if not directory.exists() or not directory.is_dir():
            raise PluginError(
                f"Directory does not exist or is not a directory: {directory}",
                resource_path=str(directory)
            )
        
        loaded_plugins = []
        
        # Add directory to Python path temporarily
        import sys
        sys.path.insert(0, str(directory.parent))
        
        try:
            # Import each Python file in the directory
            for py_file in directory.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue
                
                module_name = py_file.stem
                package_name = directory.name
                
                try:
                    # Create a temporary module path
                    full_module_name = f"{package_name}.{module_name}"
                    
                    # Try to import
                    plugin_id = self.load_plugin_from_module(full_module_name)
                    loaded_plugins.append(plugin_id)
                except (ImportError, PluginError) as e:
                    logger.warning(f"Failed to load plugin from {py_file}: {e}")
                    continue
        
        finally:
            # Remove directory from Python path
            if str(directory.parent) in sys.path:
                sys.path.remove(str(directory.parent))
        
        return loaded_plugins
    
    def initialize_plugins(self) -> None:
        """Initialize all registered plugins."""
        if self._initialized:
            return
        
        for plugin_name, plugin_info in self._plugins.items():
            if plugin_info.enabled:
                try:
                    plugin_info.instance.initialize()
                    logger.debug(f"Initialized plugin: {plugin_name}")
                except Exception as e:
                    logger.error(f"Failed to initialize plugin {plugin_name}: {e}")
                    plugin_info.enabled = False
        
        self._initialized = True
    
    def cleanup_plugins(self) -> None:
        """Clean up all registered plugins."""
        for plugin_name, plugin_info in self._plugins.items():
            if plugin_info.enabled and plugin_info.instance:
                try:
                    plugin_info.instance.cleanup()
                    logger.debug(f"Cleaned up plugin: {plugin_name}")
                except Exception as e:
                    logger.error(f"Failed to clean up plugin {plugin_name}: {e}")
        
        self._initialized = False
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """
        Get a plugin instance by name.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin instance or None if not found
        """
        plugin_info = self._plugins.get(plugin_name)
        if plugin_info and plugin_info.enabled:
            return plugin_info.instance
        return None
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        List all registered plugins.
        
        Returns:
            List of plugin information dictionaries
        """
        plugins = []
        
        for plugin_name, plugin_info in self._plugins.items():
            plugin_instance = plugin_info.instance
            
            plugins.append({
                'name': plugin_name,
                'version': plugin_instance.version if plugin_instance else 'unknown',
                'description': plugin_instance.description if plugin_instance else '',
                'author': plugin_instance.author if plugin_instance else '',
                'enabled': plugin_info.enabled,
                'initialized': self._initialized,
                'config': plugin_info.config,
                'metadata': plugin_info.metadata,
            })
        
        return plugins
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        Enable a plugin.
        
        Args:
            plugin_name: Name of the plugin to enable
            
        Returns:
            True if plugin was enabled, False otherwise
        """
        if plugin_name not in self._plugins:
            return False
        
        plugin_info = self._plugins[plugin_name]
        if not plugin_info.enabled:
            plugin_info.enabled = True
            
            # Initialize if manager is already initialized
            if self._initialized and plugin_info.instance:
                try:
                    plugin_info.instance.initialize()
                except Exception as e:
                    logger.error(f"Failed to initialize plugin {plugin_name}: {e}")
                    plugin_info.enabled = False
                    return False
            
            return True
        
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable a plugin.
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            True if plugin was disabled, False otherwise
        """
        if plugin_name not in self._plugins:
            return False
        
        plugin_info = self._plugins[plugin_name]
        if plugin_info.enabled:
            plugin_info.enabled = False
            
            # Clean up if manager is initialized
            if self._initialized and plugin_info.instance:
                try:
                    plugin_info.instance.cleanup()
                except Exception as e:
                    logger.error(f"Failed to clean up plugin {plugin_name}: {e}")
            
            return True
        
        return False
    
    def set_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        """
        Set configuration for a plugin.
        
        Args:
            plugin_name: Name of the plugin
            config: Configuration dictionary
            
        Returns:
            True if configuration was set, False otherwise
        """
        if plugin_name not in self._plugins:
            return False
        
        plugin_info = self._plugins[plugin_name]
        plugin_instance = plugin_info.instance
        
        if plugin_instance:
            # Validate configuration
            if not plugin_instance.validate_config(config):
                raise PluginError(
                    f"Invalid configuration for plugin {plugin_name}",
                    plugin_name=plugin_name
                )
        
        plugin_info.config = config
        return True
    
    # Hook system methods
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """
        Register a callback for a hook.
        
        Args:
            hook_name: Name of the hook
            callback: Callback function
        """
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        
        self._hooks[hook_name].append(callback)
        logger.debug(f"Registered hook '{hook_name}' for {callback.__name__}")
    
    def call_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Call all registered callbacks for a hook.
        
        Args:
            hook_name: Name of the hook to call
            *args: Arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
            
        Returns:
            List of results from all callbacks
        """
        if hook_name not in self._hooks:
            return []
        
        results = []
        for callback in self._hooks[hook_name]:
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Hook '{hook_name}' callback failed: {e}")
        
        return results
    
    def has_hook(self, hook_name: str) -> bool:
        """
        Check if a hook has any registered callbacks.
        
        Args:
            hook_name: Name of the hook
            
        Returns:
            True if hook has callbacks
        """
        return hook_name in self._hooks and len(self._hooks[hook_name]) > 0


# Convenience functions for global plugin management

_global_plugin_manager: Optional[PluginManager] = None


def get_global_plugin_manager() -> PluginManager:
    """
    Get the global plugin manager instance.
    
    Returns:
        Global PluginManager instance
    """
    global _global_plugin_manager
    if _global_plugin_manager is None:
        _global_plugin_manager = PluginManager()
    return _global_plugin_manager


def register_plugin(plugin_class: Type[Plugin], 
                   config: Optional[Dict[str, Any]] = None) -> str:
    """
    Register a plugin with the global plugin manager.
    
    Args:
        plugin_class: Plugin class to register
        config: Plugin configuration
        
    Returns:
        Plugin ID
    """
    manager = get_global_plugin_manager()
    return manager.register_plugin(plugin_class, config)


def get_plugin(plugin_name: str) -> Optional[Plugin]:
    """
    Get a plugin from the global plugin manager.
    
    Args:
        plugin_name: Name of the plugin
        
    Returns:
        Plugin instance or None if not found
    """
    manager = get_global_plugin_manager()
    return manager.get_plugin(plugin_name)


def list_plugins() -> List[Dict[str, Any]]:
    """
    List all plugins in the global plugin manager.
    
    Returns:
        List of plugin information dictionaries
    """
    manager = get_global_plugin_manager()
    return manager.list_plugins()


def initialize_plugins() -> None:
    """Initialize all plugins in the global plugin manager."""
    manager = get_global_plugin_manager()
    manager.initialize_plugins()


def cleanup_plugins() -> None:
    """Clean up all plugins in the global plugin manager."""
    manager = get_global_plugin_manager()
    manager.cleanup_plugins()
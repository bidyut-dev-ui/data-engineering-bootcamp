"""
Command-line interface for the example library.

This module demonstrates:
1. Building CLI applications with Click
2. Command grouping and organization
3. Configuration management via CLI
4. Plugin management via CLI
5. Interactive shell features
"""

import sys
import json
import yaml
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    import click
except ImportError:
    print("Error: Click is required for CLI functionality. Install with: pip install click")
    sys.exit(1)

from .core import DataProcessor, ConfigManager, Cache
from .utils import format_size, human_readable_time, slugify, safe_parse_json
from .plugins import get_global_plugin_manager, list_plugins, initialize_plugins, cleanup_plugins
from .exceptions import ExampleLibError


# Create CLI group
@click.group()
@click.version_option()
def cli():
    """Example Library CLI - A comprehensive Python library demonstration."""
    pass


# Configuration commands
@cli.group()
def config():
    """Configuration management commands."""
    pass


@config.command()
@click.option('--file', '-f', type=click.Path(), help='Configuration file path')
@click.option('--key', '-k', help='Configuration key')
@click.option('--value', '-v', help='Configuration value')
@click.option('--format', '-F', type=click.Choice(['json', 'yaml']), default='json',
              help='Output format')
def show(file: Optional[str], key: Optional[str], value: Optional[str], format: str):
    """Show configuration."""
    config_manager = ConfigManager(file)
    
    if key:
        config_value = config_manager.get(key)
        if config_value is None:
            click.echo(f"Key '{key}' not found in configuration")
            return
        
        if format == 'json':
            click.echo(json.dumps(config_value, indent=2))
        else:
            click.echo(yaml.dump(config_value, default_flow_style=False))
    else:
        all_config = {}
        # Get all configuration (simplified - in real implementation would need introspection)
        click.echo("Configuration:")
        click.echo("=" * 50)
        
        if format == 'json':
            click.echo(json.dumps(all_config, indent=2))
        else:
            click.echo(yaml.dump(all_config, default_flow_style=False))


@config.command()
@click.option('--file', '-f', type=click.Path(), required=True,
              help='Configuration file path')
@click.option('--watch/--no-watch', default=False,
              help='Watch for configuration changes')
def watch(file: str, watch: bool):
    """Watch configuration file for changes."""
    config_manager = ConfigManager(file)
    
    if watch:
        click.echo(f"Watching configuration file: {file}")
        try:
            config_manager.start_watching()
            click.echo("Press Ctrl+C to stop watching...")
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            config_manager.stop_watching()
            click.echo("\nStopped watching configuration file")
    else:
        click.echo(f"Configuration file: {file}")
        click.echo("Use --watch to start watching for changes")


# Data processing commands
@cli.group()
def process():
    """Data processing commands."""
    pass


@process.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(),
              help='Output file path')
@click.option('--format', '-F', type=click.Choice(['json', 'yaml', 'txt']),
              default='json', help='Output format')
def file(input_file: str, output: Optional[str], format: str):
    """Process a file."""
    processor = DataProcessor()
    
    try:
        # Read input file
        with open(input_file, 'r') as f:
            if input_file.endswith('.json'):
                data = json.load(f)
            elif input_file.endswith(('.yaml', '.yml')):
                data = yaml.safe_load(f)
            else:
                data = f.read()
        
        # Process data
        result = processor.process(data)
        
        # Output result
        if output:
            with open(output, 'w') as f:
                if format == 'json':
                    json.dump(result, f, indent=2)
                elif format == 'yaml':
                    yaml.dump(result, f, default_flow_style=False)
                else:
                    f.write(str(result))
            click.echo(f"Processed data written to: {output}")
        else:
            if format == 'json':
                click.echo(json.dumps(result, indent=2))
            elif format == 'yaml':
                click.echo(yaml.dump(result, default_flow_style=False))
            else:
                click.echo(str(result))
        
        # Show stats
        stats = processor.get_stats()
        click.echo(f"\nProcessing stats:")
        click.echo(f"  Duration: {human_readable_time(stats.get('duration', 0))}")
        click.echo(f"  Items processed: {stats.get('processed', 0)}")
        click.echo(f"  Errors: {stats.get('errors', 0)}")
        
    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)
        sys.exit(1)


@process.command()
@click.argument('data')
@click.option('--format', '-F', type=click.Choice(['json', 'yaml']),
              default='json', help='Input format')
def string(data: str, format: str):
    """Process a string."""
    processor = DataProcessor()
    
    try:
        # Parse input data
        if format == 'json':
            parsed_data = safe_parse_json(data)
            if parsed_data is None:
                click.echo("Error: Invalid JSON data", err=True)
                sys.exit(1)
        else:  # yaml
            parsed_data = yaml.safe_load(data)
        
        # Process data
        result = processor.process(parsed_data)
        
        # Output result
        click.echo(json.dumps(result, indent=2))
        
    except Exception as e:
        click.echo(f"Error processing string: {e}", err=True)
        sys.exit(1)


# Utility commands
@cli.group()
def utils():
    """Utility commands."""
    pass


@utils.command()
@click.argument('text')
@click.option('--separator', '-s', default='_',
              help='Word separator')
@click.option('--max-length', '-m', type=int, default=50,
              help='Maximum length')
def slug(text: str, separator: str, max_length: int):
    """Convert text to a slug."""
    result = slugify(text, separator, max_length)
    click.echo(result)


@utils.command()
@click.argument('size_bytes', type=int)
def format(size_bytes: int):
    """Format file size in human-readable format."""
    result = format_size(size_bytes)
    click.echo(result)


@utils.command()
@click.argument('seconds', type=float)
def time(seconds: float):
    """Format time duration in human-readable format."""
    result = human_readable_time(seconds)
    click.echo(result)


# Plugin commands
@cli.group()
def plugins():
    """Plugin management commands."""
    pass


@plugins.command()
def list():
    """List all available plugins."""
    manager = get_global_plugin_manager()
    plugins_list = manager.list_plugins()
    
    if not plugins_list:
        click.echo("No plugins available")
        return
    
    click.echo("Available plugins:")
    click.echo("=" * 80)
    
    for plugin in plugins_list:
        status = "✓" if plugin['enabled'] else "✗"
        click.echo(f"{status} {plugin['name']} v{plugin['version']}")
        if plugin['description']:
            click.echo(f"    {plugin['description']}")
        if plugin['author']:
            click.echo(f"    Author: {plugin['author']}")
        click.echo(f"    Enabled: {plugin['enabled']}")
        click.echo()


@plugins.command()
@click.argument('plugin_name')
def enable(plugin_name: str):
    """Enable a plugin."""
    manager = get_global_plugin_manager()
    
    if manager.enable_plugin(plugin_name):
        click.echo(f"Plugin '{plugin_name}' enabled")
    else:
        click.echo(f"Failed to enable plugin '{plugin_name}'", err=True)
        sys.exit(1)


@plugins.command()
@click.argument('plugin_name')
def disable(plugin_name: str):
    """Disable a plugin."""
    manager = get_global_plugin_manager()
    
    if manager.disable_plugin(plugin_name):
        click.echo(f"Plugin '{plugin_name}' disabled")
    else:
        click.echo(f"Failed to disable plugin '{plugin_name}'", err=True)
        sys.exit(1)


@plugins.command()
def init():
    """Initialize all plugins."""
    try:
        initialize_plugins()
        click.echo("All plugins initialized")
    except Exception as e:
        click.echo(f"Error initializing plugins: {e}", err=True)
        sys.exit(1)


@plugins.command()
def cleanup():
    """Clean up all plugins."""
    try:
        cleanup_plugins()
        click.echo("All plugins cleaned up")
    except Exception as e:
        click.echo(f"Error cleaning up plugins: {e}", err=True)
        sys.exit(1)


# Cache commands
@cli.group()
def cache():
    """Cache management commands."""
    pass


@cache.command()
@click.option('--max-size', '-m', type=int, default=1000,
              help='Maximum cache size')
@click.option('--ttl', '-t', type=int, default=300,
              help='Default time-to-live in seconds')
def stats(max_size: int, ttl: int):
    """Show cache statistics."""
    cache_instance = Cache(max_size=max_size, default_ttl=ttl)
    stats = cache_instance.get_stats()
    
    click.echo("Cache statistics:")
    click.echo("=" * 50)
    click.echo(f"  Max size: {max_size}")
    click.echo(f"  Default TTL: {ttl}s")
    click.echo(f"  Current size: {stats.get('size', 0)}")
    click.echo(f"  Hits: {stats.get('hits', 0)}")
    click.echo(f"  Misses: {stats.get('misses', 0)}")
    click.echo(f"  Evictions: {stats.get('evictions', 0)}")
    
    if 'hit_rate' in stats:
        click.echo(f"  Hit rate: {stats['hit_rate']:.2%}")


@cache.command()
@click.option('--max-size', '-m', type=int, default=1000,
              help='Maximum cache size')
@click.option('--ttl', '-t', type=int, default=300,
              help='Default time-to-live in seconds')
def clear(max_size: int, ttl: int):
    """Clear the cache."""
    cache_instance = Cache(max_size=max_size, default_ttl=ttl)
    cache_instance.clear()
    click.echo("Cache cleared")


# Interactive shell
@cli.command()
@click.option('--config', '-c', type=click.Path(),
              help='Configuration file path')
def shell(config: Optional[str]):
    """Start an interactive shell."""
    click.echo("Example Library Interactive Shell")
    click.echo("Type 'help' for available commands, 'exit' to quit")
    click.echo("=" * 50)
    
    # Initialize components
    config_manager = ConfigManager(config) if config else ConfigManager()
    processor = DataProcessor()
    cache = Cache()
    
    while True:
        try:
            command = click.prompt("example-lib>", type=str)
            
            if command.lower() in ('exit', 'quit', 'q'):
                click.echo("Goodbye!")
                break
            
            elif command.lower() == 'help':
                click.echo("Available commands:")
                click.echo("  help          - Show this help")
                click.echo("  exit/quit/q   - Exit the shell")
                click.echo("  config show   - Show configuration")
                click.echo("  process <data>- Process data")
                click.echo("  cache stats   - Show cache statistics")
                click.echo("  plugins list  - List plugins")
            
            elif command.startswith('config show'):
                all_config = {}
                click.echo(json.dumps(all_config, indent=2))
            
            elif command.startswith('process '):
                data = command[8:].strip()
                try:
                    result = processor.process(data)
                    click.echo(f"Result: {result}")
                except Exception as e:
                    click.echo(f"Error: {e}")
            
            elif command == 'cache stats':
                stats = cache.get_stats()
                click.echo(f"Cache stats: {stats}")
            
            elif command == 'plugins list':
                plugins_list = list_plugins()
                if plugins_list:
                    for plugin in plugins_list:
                        click.echo(f"{plugin['name']} - {plugin['description']}")
                else:
                    click.echo("No plugins available")
            
            else:
                click.echo(f"Unknown command: {command}")
                click.echo("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            click.echo("\nGoodbye!")
            break
        except EOFError:
            click.echo("\nGoodbye!")
            break
        except Exception as e:
            click.echo(f"Error: {e}")


# Main entry point
def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except ExampleLibError as e:
        click.echo(f"Library error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
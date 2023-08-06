import importlib.util
import os
import logging
import json
import sys
import threading
import glob
import re
import jsonschema
import time
import schemaser
import builtins
import uuid
import zipfile
import inspect
import asyncio

from .exceptions import AppError
from .node import Node, NodeProxy, Componentable, Eventable
from .util import sortPacks, Cache, ResourcePath, Context

__version__ = '0.0.2'
__root_app__ = None

logger = logging.getLogger('Pack')

def exit(code:int=None) -> None:
    if code is None: logger.error(f'Stopping!')
    else: logger.error(f'Proccess crashed with exit code: {code}')
    builtins.exit(code)

def getApp():
    """Returns the root App"""
    if __root_app__ is None: raise AppError('App has not started yet! Use .run() to start your app.')
    return __root_app__

class ManifestProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'ManifestProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ManifestProxy) and self.__dict__ == other.__dict__

class Manifest:
    __slots__ = (
        'name',
        'description',
        'uuid',
        '_modules',
        '_version',
        '_dependencies',
        '_path',
        '_permission_level',
        '_icon',
        '__file__',
        '__path__'
    )

    def __init__(self, name:str, description:str, uuid:str):
        """
        A class used to describe a manifest.json file.

        Arguments
        ---
        `name` - Name of the pack.

        `description` - Description of the pack.

        `uuid` - UUID of this pack.

        `scripts` - A list of scripts.

        `version` - The packs version.

        `path` - This packs path.

        `modules` - This of modules this pack uses.

        `dependencies` - List of pack dependencies.

        Methods
        ---
        enable_scripts, set_version, set_path, set_icon, add_module, remove_module, clear_modules, add_dependency, remove_dependency, clear_dependencies, from_dict, to_dict, schema, join
        """
        self.name = str(name)
        self.description = str(description)
        self.uuid = str(uuid)

    @property
    def permission_level(self):
        return getattr(self, '_permission_level', False)
    
    @permission_level.setter
    def permission_level(self, value:bool):
        self.permission_level(value)

    def set_permission_level(self, value:int):
        """
        Whether or not this pack can load scripts.

        Arguments
        ---
        `value` - True if it can load scripts. False if it cannot load scripts (default)
        """
        if value is None: self._permission_level = 0
        elif isinstance(value, int):
            self._permission_level = value
        else:
            raise TypeError(f'Expected int or None but got {value.__class__.__name__} instead.')

    @property
    def version(self):
        return getattr(self, '_version', None)
    
    @version.setter
    def version(self, version):
        self.set_version(version=version)
    
    def set_version(self, *, version:list[int]):
        """
        Sets the version for the pack.

        Arguments
        ---
        `version` - The version to set in the format [major, minor, patch]
        """
        if version is None:
            try:
                del self._version
            except AttributeError:
                pass
        else:
            self._version = Version(*version)

        return self

    @property
    def path(self):
        return str(getattr(self, '_path', None))  # type: ignore

    @path.setter
    def path(self, fp):
        self.set_path(fp=fp)

    def set_path(self, *, path:str):
        """
        Sets the path for the pack.

        Arguments
        ---
        `path` - This packs path
        """
        if path is None:
            try:
                del self._path
            except AttributeError:
                pass
        else:
            self._path = str(path)

        return self
    
    @property
    def icon(self):
        return ManifestProxy(getattr(self, '_icon', {}))  # type: ignore

    def set_icon(self, *, fp:str):
        """
        Sets the icon for the pack.

        Arguments
        ---
        `fp` - Path to the pack icon to use.
        """
        if fp is None:
            try:
                del self._icon
            except AttributeError:
                pass
        else:
            self._icon = {
                'fp': str(fp)
            }

        return self
    
    @property
    def modules(self) -> list:
        return [ManifestProxy(d) for d in getattr(self, '_modules', [])]  # type: ignore
    
    def add_module(self, *, version:list[int], type:str, uuid:str, path:str=None):
        """
        Adds a module to the manifest.

        Arguments
        ---
        `version` - The version of this module.

        `type` - The type of module to load.
        
        `uuid` - UUID of this module.
        
        `path` - If type=script this is the realitive path to the Python file.
        """
        module = {
            'version': version,
            'type': str(type),
            'uuid': str(uuid),
            'path': str(path)
        }
        try:
            self._modules.append(module)
        except AttributeError:
            self._modules = [module]
        return self

    def remove_module(self, index:int):
        """
        Removes a module at a specified index.

        Arguments
        ---
        `index` - Index in Manifest.modules to delete.
        """
        try:
            del self._modules[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_modules(self):
        """
        Removes all modules from this manifest.
        """
        try:
            self._nodes.clear()
        except AttributeError:
            self._nodes = []
        return self

    @property
    def dependencies(self) -> list:
        return [ManifestProxy(d) for d in getattr(self, '_dependencies', [])]  # type: ignore
    
    def add_dependency(self, *, uuid:str, version:list=None, min_version:list=None, description:str=None):
        """
        Adds a dependency to the manifest.

        Arguments
        ---
        `uuid` - UUID of the pack that is needed. Should match the UUID defined at the top of the manifest.json of the needed pack.

        `version` - The exact version that is needed.

        `min_version` - The minimum allowed version.

        `description` - Descirption of this dependcy.
        """
        dependency = {
            'description': str(description),
            'uuid': str(uuid),
            'version': version,
            'min_version': min_version
        }
        if dependency['version'] is not None:
            dependency['version'] = Version(*dependency['version'])
            
        if dependency['min_version'] is not None:
            dependency['min_version'] = Version(*dependency['min_version'])

        try:
            self._dependencies.append(dependency)
        except AttributeError:
            self._dependencies = [dependency]
        return self

    def remove_dependency(self, index:int):
        """
        Removes a dependency at a specified index.

        Arguments
        ---
        `index` - Deletes the dependent pack from Manifest.dependencies.
        """
        try:
            del self._dependencies[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_dependencies(self):
        """
        Removes all dependencies from this manifest.
        """
        try:
            self._dependencies.clear()
        except AttributeError:
            self._dependencies = []
        return self

    def to_dict(self) -> dict:
        """
        Converts a :class:`Manifest` to a :class:`dict`
        """
        result = {
            key[1:]: getattr(self, key)
            for key in self.__slots__
            if key[0] == '_' and hasattr(self, key)
        }
        return result
    
    @classmethod
    def from_dict(cls, data:dict):
        """
        Converts a :class:`dict` to a :class:`Manifest`
        """
        self = cls.__new__(cls)

        self.name = data.get('name', None)
        self.description = data.get('description', None)
        self.uuid = data.get('uuid', None)
        self.version = data.get('version', None)

        if self.name is not None:
            self.name = str(self.name)

        if self.description is not None:
            self.description = str(self.description)
            
        if self.uuid is not None:
            self.uuid = str(self.uuid)

        # special cases

        for dep in data.get('dependencies', []):
            self.add_dependency(**dep)
            
        for mod in data.get('modules', []):
            self.add_module(**mod)

        return self

    @classmethod
    def schema(self):
        """
        This classes JSON schema used for validation when loading the file.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema",
            'type': 'object',
            'required': [
                'name',
                'description',
                'uuid',
                'version'
            ],
            'properties': {
                "name": {
                    'type': 'string'
                },
                "description": {
                    'type': 'string'
                },
                'uuid': {
                    'type': 'string'
                },
                "version": {
                    'type': 'array',
                    'type': 'array',
                    'items': {
                        'type': 'integer'
                    },
                    'minItems': 3,
                    'maxItems': 3
                },
                "modules": {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'required': [
                            'version',
                            'type',
                            'uuid'
                        ],
                        'properties': {
                            'version': {
                                'type': 'array',
                                'items': {
                                    'type': 'integer'
                                },
                                'minItems': 3,
                                'maxItems': 3
                            },
                            "type": {
                                'type': 'string'
                            },
                            "uuid": {
                                'type': 'string'
                            },
                            'path': {
                                'type': 'string'
                            }
                        },
                        'additionalProperties': False
                    }
                },
                "dependencies": {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'required': [
                            'uuid'
                        ],
                        'anyOf': [
                            {'required': ['version']},
                            {'required': ['min_version']}
                        ],
                        'properties': {
                            'uuid': {
                                'type': 'string'
                            },
                            'version': {
                                'type': 'array',
                                'items': {
                                    'type': 'integer'
                                },
                                'minItems': 3,
                                'maxItems': 3
                            },
                            'min_version': {
                                'type': 'array',
                                'items': {
                                    'type': 'integer'
                                },
                                'minItems': 3,
                                'maxItems': 3
                            },
                            'description': {
                                'type': 'string'
                            }
                        },
                        'additionalProperties': False
                    }
                }
            },
            'additionalProperties': False
        }

    def join(self, *paths:str):
        """
        Joins all paths realitive to this packs path.
        """
        return os.path.join(self.path, re.sub(r'^/|^\\|^./|^.\\', '', os.path.join(*paths))).replace('/', '\\')

class Script:
    def __init__(self, app, name:str, fp:str):
        """
        WARNING: Do not use! use App.add_script(name, fp)

        Arguments
        ---
        `app` - The root App.

        `name` - Name of the script.

        `fp` - File path to the Python script.

        Methods
        ---
        load, on_enable, on_disable
        """
        self.app = app
        self.name = name
        self.fp = fp
        self.module = None

        if os.path.isdir(self.fp): self.fp = os.path.join(self.fp, '__init__.py')
        if os.path.exists(self.fp)==False: logger.warning(f"'{self.fp}' Script not found!")

    def load(self):
        """
        Runs the Python script
        """
        global loading_script
        spec = importlib.util.spec_from_file_location(self.name, self.fp)
        foo = importlib.util.module_from_spec(spec)
        sys.modules[self.name] = foo
        spec.loader.exec_module(foo)
        self.app.loading_script = foo
        self.module = foo
        self.on_enable()

    def on_enable(self):
        """
        Runs the Python scripts on_enable method if defined.
        """
        ctx = Context(None, None)
        ctx.logger = logging.getLogger(self.name)
        try: self.module.on_enable(ctx)
        except (AttributeError): pass
        return self
    
    def on_disable(self):
        """
        Runs the Python scripts on_disable method if defined.
        """
        ctx = Context(None, None)
        ctx.logger = logging.getLogger(self.name)
        try: self.module.on_disable(ctx)
        except (AttributeError): pass
        return self

class _node:
    def __init__(self, module, rule:str, cls, mimetype:str=None, resourcepath_command=None, description:str=None):
        """Internal class"""
        self.app = getApp()
        self.module = module
        self.src = '' # Python file that created this node
        self.path = rule
        self.path_args = {}
        self.cls = cls
        self.traits = self.cls.traits # Traits are used for the JSON schema
        self._mimetype = mimetype
        self.resourcepath_command = resourcepath_command
        self.name = str(cls.__name__).lower()
        self.on_error = None
        if mimetype is None: self._mimetype = 'application/json'

        if resourcepath_command is None: self.resourcepath_command = self.resourcepath

        self.description = description
        if description is None: self.description = '...'

    @property
    def ref(self):
        # ResourcePath(self.module.module_type, self.name)
        return str

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value

    @property
    def mimetype(self):
        """Returns the _mimetype that this node should use."""
        for other in self.app.mimetypes:
            mime = self._mimetype.split('/')
            # if len(mime) == 2:
            #     if m.type == mime[0]:
            #         if m.subtype is None: return m.func
            #         elif m.subtype == mime[1]: return m.func
            # elif len(mime) == 1:
            #     if m.type == mime[0]:
            #         return m.func
            
            m = None
            if len(mime) == 2: m = _mimetype(mime[0], mime[1])
            elif len(mime) == 1: m = _mimetype(mime[0])
            if m == other: return other
                
        logger.warning(f"mimetype '{self._mimetype}' is not defined!")
        return None

    def to_schema(self):
        try: return to_schema(self.cls, self, self.traits)
        except Exception as err:
            logger.exception(str(err)+f" when loading {self.cls}")
            exit(1)

    def resourcepath(self, node:Node, path:str, manifest:Manifest, **kw):
        """Returns the namespace id of this item"""
        res = os.path.dirname(self.path).replace('*', '')
        return os.path.relpath(path, manifest.join(res)).replace('\\','/').replace(os.path.splitext(path)[1], '')
        
    # REGISTER COMPONENTS
    def add_component(self, func, name:str=None, description:str=None):
        """
        Adds a component to the node.

        Arguments
        ---
        `func` - The function to run when this component is defined.

        `name` - Name of the component to add.

        `description` - Description of the component to add.
        """
        com = _component(Context(self, self.module), func, name, description)
        try:
            self.__components__[com.name] = com
        except AttributeError:
            self.__components__ = {com.name: com}

        return com

    def remove_component(self, name:str):
        """
        Removes a component at a specified name.

        Arguments
        ---
        `name` - Name of the component to remove.
        """
        try:
            del self.__components__[name]
        except (AttributeError, IndexError):
            pass

        return self
        
    def clear_components(self):
        """
        Removes all components from this node.
        """
        try:
            self.__components__.clear()
        except AttributeError:
            self.__components__ = {}
        return self

    def component(self, name:str=None, description:str=None):
        """
        Register a new component for this node.

        Arguments
        ---
        `name` - Name of the node to register.

        `description` - Description of the node to register.
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            return self.add_component(func, name, description)
        return decorator

    def error(self):
        """
        Function to run when an error occors.
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            self.on_error = func
        return decorator

class _event:
    def __init__(self, ctx:Context, func, name:str=None, description:str=None):
        """Internal class"""
        self.ctx = ctx
        self.app = getApp()
        self.src = '' # Python file that created this event
        self.func = func
        self.name = name
        self.on_error = None
        if name is None: self.name = str(func.__name__)

        self.description = description
        if description is None: self.description = '...'

    def error(self):
        """
        Function to run when an error occors.
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            self.on_error = func
        return decorator

    async def call(self, options:dict, extra:dict={}):
        """
        Trigger this event.
        """
        ctx = self.ctx.copy().add_extras(**extra)
        ctx.logger = logging.getLogger(self.func.__module__)
        try:
            return await self.func(ctx, **options)
        except Exception as err:
            if self.on_error is not None:
                return await self.on_error(ctx, err)
            else:
                ctx.logger.exception(err)
                exit(-1)
    
class _component:
    def __init__(self, ctx:Context, func, name:str=None, description:str=None):
        """Internal class"""
        self.ctx = ctx
        self.src = '' # Python file that created this component
        self.func = func
        self.on_error = None
        if name is None: self.name = self.ctx.module.namespace+':'+func.__name__
        else: self.name = self.ctx.module.namespace+':'+name
        
        self.description = description
        if description is None: self.description = '...'
        
    def error(self):
        """
        Function to run when an error occors.
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            self.on_error = func
        return decorator

    async def call(self, options:dict, extra:dict={}):
        """
        Trigger this component.
        """
        ctx = self.ctx.copy().add_extras(**extra)
        ctx.logger = logging.getLogger(self.func.__module__)
        try:
            return await self.func(ctx, **options)
        except Exception as err:
            if self.on_error is not None:
                return await self.on_error(ctx, err)
            else:
                ctx.logger.exception(err)
                exit()
    
class _mimetype:
    def __init__(self, type:str, subtype:str=None, func=None):
        self.func = func
        self.type = type
        self.subtype = subtype
        self.on_error = None
       
    def __eq__(self, other):
        if isinstance(other, _mimetype) and self.type == other.type:
            if self.subtype is not None and other.subtype is not None:
                if self.subtype == other.subtype: return True
                else:return False
            return True
        return False

    def __str__(self):
        if self.subtype is None: return f'{self.type}/*'
        return f'{self.type}/{self.subtype}'
 
    def error(self):
        """
        Function to run when an error occors.
        """
        def decorator(func):
            self.on_error = func
        return decorator

    async def call(self, file:str, node:_node, subtype:str) -> Node:
        """
        Trigger this mimetype.
        """
        if self.func is not None:
            ctx = Context(node, None, subtype=subtype).add_extras(file=file)
            ctx.logger = logging.getLogger(self.func.__module__)
            try:
                item = await self.func(ctx)
                item.on_load(ctx)
                return item
            except Exception as err:
                if self.on_error is not None:
                    return await self.on_error(ctx, err)
                else:
                    ctx.logger.exception(err)
                    exit(-1)
        else:
            raise TypeError(f'{self} mimetype is not callable!')

class AppProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'AppProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AppProxy) and self.__dict__ == other.__dict__

class App:
    def __init__(self, default_namespace:str='default', ui:bool=False):
        """
        The root app.

        Arguments
        ---
        `default_namespace` - The default namespace for components. if namespace is "foo" then a component can be defined "foo:bar" or "bar"

        `ui` - When true it will use UI's when needed. For example when ui=False a pack contains a script it will ask via console. When ui=True it will use a Tkinter window.

        Methods
        ---
        bind, unbind, call_bind_event, get_node, add_module, remove_module, clear_modules, add_mimetype, remove_mimetype, clear_mimetypes, add_script, remove_script, clear_scripts, add_path, remove_path, clear_paths, reload, unload, load, dump_registries, run
        """
        global __root_app__
        __root_app__ = self
        self.root_path = None
        self.logger = logger
        self.default_namespace = default_namespace
        self.ui = ui
        self.packs = {}
        self.alive:bool = False
        self.loading_script = None # script that is currently being loaded
        self.bind_events = {}
        self.cache = Cache()

        # reg
        self.nodes = {}
        self.items = {} # registry from packs
        self.nodes = {}
        self.events = {}
        self.all_packs = {} # All packs
        self.enabled_packs = {} # All enabled packs
        self.disabled_packs = {} # All disabled packs
    
    def __getitem__(self, path:str) -> dict:
        if re.match(r'^(.*)\.(.*)$', path):
            module, node_type = path.split('.')
            if module in self.items and node_type in self.items[module]:
                items = self.items[module][node_type]
                return items
        raise KeyError(path)

    def builtins(self):
        """
        Load builtin mimetypes
        
        Supported:
        - application/json
        - application/yaml (Needs PyYAML)
        - application/zip
        - application/tar
        - image/* (Needs Pillow)
        - audio/* (Needs pygame)
        - video/* (Needs opencv-python)
        """
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
        import tarfile
        # xml
        @self.mimetype('application', 'json')
        async def application_json(ctx:Context) -> Node: # ctx.file, ctx.node, ctx.subtype
            valid, data = validate(ctx.file, ctx.node.to_schema(), 'json')
            if valid:
                n = ctx.node.cls.from_dict(data)
                n.__file__ = ctx.file
                return n
        
        @self.mimetype('application', 'zip')
        async def application_zip(ctx:Context) -> Node:
            zip = zipfile.ZipFile(ctx.file)
            n = ctx.node.cls.from_dict({'zip': zip})
            n.__file__ = ctx.file
            return n
            
        @self.mimetype('application', 'tar')
        async def application_tar(ctx:Context) -> Node:
            tar = tarfile.TarFile(ctx.file)
            n = ctx.node.cls.from_dict({'tar': tar})
            n.__file__ = ctx.file
            return n
            
        try:
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # hide message
            import pygame
            pygame.init()

            @self.mimetype('audio')
            async def audio(ctx:Context) -> Node:
                audio = pygame.mixer.Sound(ctx.file)
                n = ctx.node.cls.from_dict({'audio': audio})
                n.__file__ = ctx.file
                return n
        except ImportError: pass

        try:
            import cv2
            @self.mimetype('video')
            async def video(ctx:Context) -> Node:
                video = cv2.VideoCapture(ctx.file)
                n = ctx.node.cls.from_dict({'video': video})
                n.__file__ = ctx.file
                return n
        except ImportError: pass

        try:
            import yaml
            @self.mimetype('application', 'yaml')
            async def application_yaml(ctx:Context) -> Node:
                valid, data = validate(ctx.file, ctx.node.to_schema(), 'yaml')
                if valid:
                    n = ctx.node.cls.from_dict(data)
                    n.__file__ = ctx.file
                    return n
        except ImportError: pass
        
        try:
            from PIL import Image
            import imghdr
            @self.mimetype('image')
            async def image(ctx:Context) -> Node:
                ext = imghdr.what(ctx.file)
                if ext is not None and (ctx.subtype is not None and ext==ctx.subtype):
                    img = Image.open(ctx.file)
                    n = ctx.node.cls.from_dict({'image': img})
                    n.__file__ = ctx.file
                    return n
                else: logging.warning(f"'{ctx.file}' Failed to load image! Expected a {str(ctx.subtype).upper()} but got a {ext.upper()}")
        except ImportError: pass

    def add_bind(self, event:str, func):
        """
        Run a function when a certain event triggers.

        Arguments
        ---
        `event` - The event type to bind to.
        
        `func` - The function to run.

        Events
        ---
        `on_load` - After all packs have been loaded.
        
        `on_unload` - Before all packs have been unloaded.

        `on_reload` - When all packs are being reloaded.

        `on_import` - After a pack has been imported.
        """
        if event is None: event  = func.__name__
        try: self.bind_events[str(event)].append(func)
        except KeyError: self.bind_events = {event: [func]}
        return self
    
    def bind(self, event:str=None):
        """
        Run a function when a certain event triggers.

        Arguments
        ---
        `event` - The event type to bind to.
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            return self.add_bind(event, func)
        return decorator
    
    def unbind(self, event:str):
        """
        Removes a bind event.

        Arguments
        ---
        `event` - The event type to remove.
        """
        del self.bind_events[str(event)]

    def trigger_bind(self, event:str, ctx:Context=None):
        """
        Runs the bind event callbacks.
        """
        funcs = self.bind_events.get(str(event))

        if ctx is None:
            ctx = Context(None, None)
            ctx.logger = self.logger

        if funcs is not None:
            for f in funcs:
                asyncio.create_task(f(ctx))
        return self

    def get_node(self, name) -> Node:
        """
        Returns with the Node.

        Arguments
        ---
        `name` - The name of the node to get.
        """
        if isinstance(name, Node):
            name = name.__class__.__name__.lower()

        for module_type, nodes in self.nodes.items():
            node = nodes.get(name)
            if node is not None: return node

    def get_item(self, path:str, name:str=None) -> dict|Node:
        """
        Returns the item or items that this targets.
        
        Arguments
        ---
        `path` - The module_type.node_type to look in. Example "data.item" will search in module "data" and look for all "item" nodes

        `name` - The name of the node to get.
        """
        if name is not None: return self[path].get(name)
        return self[path]

    @property
    def modules(self) -> dict:
        return getattr(self, '_modules', [])
    
    def add_module(self, module_type:str, namespace:str, cls):
        """
        Adds a module to the app.

        Arguments
        ---

        `module_type` - The module type.

        `namespace` - Namespace of this modules items.

        `cls` - The Module class. 
        """
        try:
            self._modules[module_type][namespace] = cls
        except AttributeError:
            self._modules = {module_type: {namespace: cls}}

        except KeyError:
            self._modules[module_type] = {namespace: cls}
        return cls
    
    def remove_module(self, name:str):
        """
        Removes a module at a specified name.

        Arguments
        ---
        `name` - Name in App.modules to delete.
        """
        try:
            del self._modules[name]
        except (AttributeError, KeyError):
            pass
        return self

    def clear_modules(self):
        """
        Removes all modules from this app.
        """
        try:
            self._modules.clear()
        except AttributeError:
            self._modules = {}
        return self
    
    @property
    def mimetypes(self) -> list:
        return [d for d in getattr(self, '_mimetypes', [])]
    
    def add_mimetype(self, func, type:str, subtype:str=None):
        """
        Adds a mimetype to the app.

        WARNING: Use App.mimetype decorator function instead.

        Arguments
        ---
        `func` - The function to call.

        `type` - The type of mimetype. type/subtype

        `subtype` - The subtype of mimetype. type/subtype
        """
        # mimetype = {'func': func, 'type': type, 'subtype': subtype} # OLD
        mimetype = _mimetype(type, subtype, func)
        try:
            self._mimetypes.append(mimetype)
        except AttributeError:
            self._mimetypes = [mimetype]
        return mimetype
    
    def remove_mimetype(self, index:int):
        """
        Removes a mimetype at a specified index.

        Arguments
        ---
        `index` - Index in App.mimetypes to delete.
        """
        try:
            del self._mimetypes[index]
        except (AttributeError, KeyError):
            pass
        return self

    def clear_mimetypes(self):
        """
        Removes all scripts from this app.
        """
        try:
            self._mimetypes.clear()
        except AttributeError:
            self._mimetypes = []
        return self
    
    def mimetype(self, type, subtype:str=None):
        """
        Adds a mimetype to the app.

        Arguments
        ---
        `type` - The type of mimetype. type/subtype

        `subtype` - The subtype of mimetype. type/subtype
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            return self.add_mimetype(func, type, subtype)
        return decorator

    @property
    def scripts(self) -> dict[Script]:
        return getattr(self, '_scripts', {})
    
    def add_script(self, name:str, fp:str):
        """
        Adds a script to the app.

        Arguments
        ---

        `name` - Name of the script.

        `fp` - Path to the Python FILE or Python PACKAGE.
        """
        script = Script(self, name, fp)
        try:
            if script.name not in self._scripts:
                self._scripts[script.name] = script
            else:
                logger.warning(f"'{script.fp}' Duplicate script found '{script.name}'")
        except AttributeError:
            self._scripts = {script.name: script}
        return script
    
    def remove_script(self, name:str):
        """
        Removes a script at a specified name.

        Arguments
        ---
        `name` - Name in App.scripts to delete.
        """
        try:
            del self._scripts[name]
        except (AttributeError, KeyError):
            pass
        return self

    def clear_scripts(self):
        """
        Removes all scripts from this app.
        """
        try:
            self._scripts.clear()
        except AttributeError:
            self._scripts = {}
        return self
    
    @property
    def paths(self) -> list:
        return [AppProxy(d) for d in getattr(self, '_paths', [])]  # type: ignore
    
    def get_default_path(self) -> AppProxy:
        for p in self.paths:
            if p.default == True: return p
        if len(self.paths) >= 1: return self.paths[0] 
        return None

    def add_path(self, path, allowed_modules:list[str]=None, default:bool=False, permission_level:int=0):
        """
        Adds a path to the app.

        Arguments
        ---

        `path` - Folder to load all packs.

        `allowed_modules` - List of allowed modules for this path.

        `default` - If True this is the default path to place imported packs.

        `permission_level` - Permission level of this path.

        0 - No scripts. (default)

        1 - Will ask user for permission to load the script.

        2 - Highest level, can load scripts without asking the user.
        """
        try:
            os.makedirs(path, exist_ok=True)
            self._paths.append({'path':path, 'perm': permission_level, 'default': default, 'allowed_modules': allowed_modules})
        except AttributeError:
            self._paths = [{'path':path, 'perm': permission_level, 'default': default, 'allowed_modules': allowed_modules}]
        return self

    def remove_path(self, index:int):
        """
        Removes a path at a specified index.

        Arguments
        ---
        `index` - Index in App.paths to delete.
        """
        try:
            del self._paths[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_paths(self):
        """
        Removes all paths from this app.
        """
        try:
            self._paths.clear()
        except AttributeError:
            self._paths = []
        return self
    
    def reload(self):
        """
        Reload all packs

        Arguments
        ---
        `threaded` - When true it will reload all packs in a new thread.
        """
        self.unload()
        self.trigger_bind('on_reload')
        logger.info('Reloading!')
        asyncio.run(self.load())

    def unload(self):
        """
        Unloads all packs.
        """
        # Unload all nodes
        self.trigger_bind('on_unload')
        for module_name, modules in self.items.items():
            for node_name, nodes in modules.items():
                for name, node in nodes.items():
                    ctx = Context(node, None)
                    try:
                        node.on_unload(ctx)
                    except Exception as err:
                        ctx.logger.exception(err)
            
        self.cache.clear('images') # Clear cached images
        self.clear_mimetypes()
        self.clear_modules()
        self.events = {}
        self.nodes = {}
        self.items = {}
        self.all_packs = {}
        self.enabled_packs = {}
        self.disabled_packs = {}

        for name, script in self.scripts.items(): script.on_disable()
        self.clear_scripts()

    async def load(self):
        """
        Load all packs from the configured paths.
        
        WARNING: If you need to reload all packs use App.reload instead!
        """
        self.builtins()
        start = time.time()

        # Validate packs
        for p in self.paths:
            for name in os.listdir(p.path):
                path = os.path.join(p.path, name)
                manifest_path = os.path.join(path, 'manifest.json')
                if os.path.exists(manifest_path):
                    valid, data = validate(manifest_path, Manifest.schema())
                    if valid:
                        manifest = Manifest.from_dict(data)
                        manifest.__file__:str = manifest_path
                        manifest.__path__:AppProxy = p
                        manifest.set_permission_level(p.perm)
                        manifest.set_path(path=path)
                        # icon = os.path.join(path, 'pack_icon.png')
                        # if os.path.isfile(icon):
                        #     manifest.set_icon(fp=icon)
                        # manifest.set_icon()

                        # Check if pack is in list
                        register = True
                        for pack in self.list_packs():
                            if pack['Name'] == manifest.uuid: register = False
                        if register:
                            self.register_pack(uuid=manifest.uuid, version=manifest.version)
                        self.all_packs[str(manifest.uuid)] = manifest
         
        # TODO algrithm to re-order path list for depcies
        # pack1 requires pack2. so it should order them [pack2, pack1] that way pack2 loads first, then pack1
        self.all_packs = sortPacks(self.all_packs)

        # Assign enabled and disabled packs
        for uuid, p in self.all_packs.items():
            with open(os.path.join(self.root_path, 'packs.json'), 'r') as r:
                _packs = json.load(r)['Packs']
                enabled_packs = _packs.get('Enabled', [])
                for i in enabled_packs:
                    if i['Name'] == uuid:
                        self.enabled_packs[str(uuid)] = p

                disabled_packs = _packs.get('Disabled', [])
                for j in disabled_packs:
                    if j['Name'] == uuid:
                        self.disabled_packs[str(uuid)] = p

        # Check dependencies
        for uuid, manifest in self.enabled_packs.items():
            for dep in manifest.dependencies:
                res = self.enabled_packs.get(dep.uuid)
                if res is None:
                    logger.warning(f"'{manifest.path}' Missing dependency with ID '{dep.uuid}' and version {dep.version}")
                else:
                    if dep.version is not None:
                        if manifest.version != dep.version:
                            logger.warning(f"'{manifest.path}' Missing dependency with ID '{dep.uuid}' and version {dep.version}")

                    elif dep.min_version is not None:
                        if manifest.version < dep.min_version:
                            logger.warning(f"'{manifest.path}' Missing dependency with ID '{dep.uuid}' and version {dep.min_version}")

        # Load scripts
        askokscript = None
        for uuid, manifest in self.enabled_packs.items():
            for module in manifest.modules:
                if module.type == 'script': # Built-in module type 'script'
                    if manifest.permission_level >= 1:
                        if manifest.permission_level >= 2:
                            script_fp = manifest.join(module.path)
                            script = self.add_script(module.uuid[0:8], script_fp)
                            script.load()
                        else:
                            # TODO if app has UI this should use a seperate method for UI implemntation.
                            if askokscript == None:
                                askokscript = self.askyesno('Do you want to allow this pack to make changes to your PC? Only load packs from authors you trust.') 

                            if askokscript:
                                script_fp = manifest.join(module.path)
                                script = self.add_script(module.uuid[0:8], script_fp)
                                script.load()

        self.loading_script = None
        # Load modules and nodes
        for uuid, manifest in self.enabled_packs.items():
            for module in manifest.modules:
                if module.type != 'script':
                    # Block modules 
                    if manifest.__path__.allowed_modules is not None and module.type not in manifest.__path__.allowed_modules:
                        logger.warning(f"'{module.type}' module is not allowed in '{manifest.path}'")
                        continue

                    regs = self.nodes.get(module.type)
                    if regs is not None:
                        for name, node in regs.items(): # Search for nodes
                            files = glob.glob(manifest.join(node.path), recursive=True)
                            for file in files:
                                if node.mimetype is not None:
                                    types = node._mimetype.split('/')
                                    subtype = None
                                    if len(types) == 2: subtype = types[1]
                                    # reg = node.mimetype(file, node, subtype)
                                    reg = await node.mimetype.call(file=file, node=node, subtype=subtype)
                                    if reg is not None:
                                        reg._app = self
                                        name = node.resourcepath_command(node, file, manifest)
                                        try:
                                            self.items[module.type][node.name][name] = reg
                                        except KeyError:
                                            self.items[module.type][node.name] = {name: reg}


                    else:
                        logger.warning(f"'{manifest.path}' {module.type} is not a valid module type! Allowed values: {', '.join(self.nodes)}, script")

        tme = round(time.time() - start, 2)
        logger.info(f'Done! ({tme} ms)')
        self.trigger_bind('on_load')

    def askyesno(self, prompt:str) -> bool:
        """
        Ask a question; return true if the answer is yes
        """
        if self.ui:
            from tkinter import messagebox
            res = messagebox.askyesno('App', prompt)
            return res
        else:
            res = input(str(prompt)+' (Y/n) ')
            if res.strip().lower() == 'y': return True
        return False

    def dump_registries(self, path:str=''):
        """
        Generates a folder of files that list all loaded registries.

        Arguments
        ---
        `path` - Path to dump all registries
        """
        if self.alive:
            for module_type, module in self.items.items():
                node_path = os.path.join(path, 'gen', str(module_type))
                os.makedirs(node_path, exist_ok=True)
                result = {}
                for node_name, node in module.items():
                    result[node_name] = {'entries': {}}
                    index = 0
                    for name in node:
                        result[node_name]['entries'][name] = {'protocol_id': index}
                        index +=1
                with open(os.path.join(node_path, 'registries.json'), 'w') as w:
                    w.write(json.dumps(result, indent=4))
        else:
            raise RuntimeError('App must be running before you can run this method!')

    def register_pack(self, uuid:str, version:list[int, int, int]):
        """
        Add this pack to the packs.json
        
        Arguments
        ---
        `uuid` - UUID of the pack to registesr.

        `version` - Version of the pack to register.
        """
        pack = os.path.join(self.root_path, 'packs.json')
        with open(pack, 'r') as r:
            packs = json.load(r)
            packs['Packs']['Enabled'].append({'Name': str(uuid), 'Version': str(version)})

        with open(pack, 'w') as w:
            w.write(json.dumps(packs))

    def list_packs(self):
        """
        Returns a list of all packs
        """
        packs = []
        with open(os.path.join(self.root_path, 'packs.json'), 'r') as r:
            res = json.load(r)
            for e in res['Packs']['Enabled']: packs.append(e)
            for d in res['Packs']['Disabled']: packs.append(d)
        return packs

    def enable_pack(self, uuid:str):
        """
        Enables this pack. Run .reload() to apply the changes.

        Arguments
        ---
        `uuid` - UUID of the pack to enable.
        """
        pack = os.path.join(self.root_path, 'packs.json')
        with open(pack, 'r') as r:
            packs = json.load(r)
            disabled = packs['Packs']['Disabled']
            i=0
            for p in disabled:
                if p['Name'] == uuid:
                    packs['Packs']['Enabled'].append(p)
                    del packs['Packs']['Disabled'][i]
                    continue
                i+=1

        with open(pack, 'w') as w:
            w.write(json.dumps(packs))

    def disable_pack(self, uuid:str):
        """
        Disabled this pack. Run .reload() to apply the changes.

        Arguments
        ---
        `uuid` - UUID of the pack to enable.
        """
        pack = os.path.join(self.root_path, 'packs.json')
        with open(pack, 'r') as r:
            packs = json.load(r)
            enabled = packs['Packs']['Enabled']
            i=0
            for p in enabled:
                if p['Name'] == uuid:
                    packs['Packs']['Disabled'].append(p)
                    del packs['Packs']['Enabled'][i]
                    continue
                i+=1

        with open(pack, 'w') as w:
            w.write(json.dumps(packs))

    def lock_pack(self, uuid:str, state:str='enable'):
        """
        Locks this pack in enable/disable state.

        Arguments
        ---
        `uuid` - UUID of the pack to lock.

        `state` - When set to 'enabled' this pack will always be enabled can cannot be changed. When set to 'disabled' this pack will always be disabled and cannot be changed.
        """
        if state=='enabled': self.enable_pack(uuid)
        elif state=='disabled': self.disable_pack(uuid)

    def unlock_pack(self, uuid:str):
        """
        Unlocks this pack.

        Arguments
        ---
        `uuid` - UUID of the pack to unlock.
        """
        self.enable_pack(uuid)

    async def import_pack(self, fp:str) -> bool:
        """
        Copies this pack to the default pack folder. Run .reload() to apply the changes.

        Arguments
        ---
        `fp` - File path to the ZIP file to import.

        `threaded` - Import this file in a new thread.
        """
        dpath = self.get_default_path()
        if dpath is not None:
            path = os.path.join(dpath.path, uuid.uuid4().hex)
            os.makedirs(path, exist_ok=True)
            if os.path.isfile(fp):
                with zipfile.ZipFile(fp) as zip:
                    try:
                        valid, data = validates(zip.read('manifest.json'), Manifest.schema(), filename=os.path.join(fp, 'manifest.json'))
                        if valid:
                            packs = self.list_packs()
                            shouldImport = True
                            for pack in packs:
                                if pack['Name'] is data['uuid']:
                                    shouldImport = False
                            if shouldImport:
                                zip.extractall(path)
                                await self.trigger_bind('on_import', Context(None, None, path=path))
                                return True
                            else:
                                return False
                    except KeyError: pass
        else:
            raise AppError('Paths have not been set!')            
        return False

    def run(self, path:str, logger:bool=True):
        """
        Runs the app.
        
        Arguments
        ---
        `path` - The root script path.

        `multithreaded` - When true it will load all packs using multiple threads for faster loading times.

        `logger` - When false it will disable the built-in logger.
        """
        self.root_path = path
        packs = os.path.join(self.root_path, 'packs.json')
        if os.path.exists(packs) == False:
            with open(packs, 'w') as w:
                w.write(json.dumps({'Packs': {'Disabled': [], 'Enabled': []}}))

        if self.alive is False:
            if logger is False: logger.disabled = True
            self.alive = True
            asyncio.run(self.load())

class ModuleProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'ModuleProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ModuleProxy) and self.__dict__ == other.__dict__

class Module:
    def __init__(self, module_type:str, namespace:str):
        """
        Defines a modules nodes when defined in the packs manifest.json.

        Arguments
        ---
        `namespace` - The namespace used for components. `<namespace>:<component_name>`

        `module_type` - The type of module this is. example; "data" for server side modules, "resources" is for client side modules.

        Methods
        ---
        add_node, remove_node, clear_nodes, node, add_event, remove_event, clear_events, event
        """
        self.app = getApp()

        self.src = self.app.loading_script.__file__ if self.app.loading_script is not None else '?'
        self.namespace = str(namespace)
        self.module_type = str(module_type)

        if self.module_type not in self.app.items: self.app.items[self.module_type] = {}

        self.app.add_module(self.module_type, self.namespace, self)

    @property
    def nodes(self) -> list:
        return [str(d) for d in getattr(self, '_nodes', [])]  # type: ignore

    def add_node(self, cls:Node, *, rule:str, mimetype:str=None, resourcepath_command=None, description:str=None):
        """
        Creates a node from a regular class.

        WARNING: Do not use! Use Module.node decorator method instead.

        Arguments
        ---
        `path` - The glob path to load these file(s) from.

        `mimetype` - The mimetype to except for this node.

        `resourcepath_command` - The command to generate the resrouce path.

        `description` - Description of the node.
        """
        node = _node(self, rule, cls, mimetype, resourcepath_command)
        node.src = self.src
        try:
            if node.name not in self.app.nodes[self.module_type]:
                self.app.nodes[self.module_type][node.name] = node
            else:
                logger.warning(f"'{node.src}' Duplicate node found '{node.name}'")
        except KeyError:
            self.app.nodes[self.module_type] = {node.name: node}

        return node

    def remove_node(self, name:str):
        """
        Removes a node with the specified name.

        Arguments
        ---
        `name` - Name of the node to remove.
        """
        try:
            del self._nodes[name]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_nodes(self):
        """
        Removes all nodes from this module.
        """
        try:
            self._nodes.clear()
        except AttributeError:
            self._nodes = []
        return self

    def node(self, rule:str, mimetype:str=None, resourcepath_command=None, description:str=None):
        """
        Creates a node from a regular class.

        Arguments
        ---
        `path` - The glob path to load these file(s) from.

        `mimetype` - The mimetype to except for this node.

        `resourcepath_command` - The command to generate the resrouce path.
        """
        def decorator(cls):
            return self.add_node(cls, rule=rule, mimetype=mimetype, resourcepath_command=resourcepath_command, description=description)
        return decorator
    
    @property
    def events(self) -> list:
        return [str(d) for d in getattr(self, '_events', [])]  # type: ignore
    
    def add_event(self, func, name:str=None, description:str=None):
        """
        Creates an event from a regular function.

        WARNING: Do not use! Use Module.event decorator method instead.

        Arguments
        ---
        `name` - Name of this event.
        """
        ctx = Context(None, self)
        event = _event(ctx, func, name, description)
        event.src = self.src
        if event.name not in self.app.events:
            self.app.events[event.name] = event
        else:
            logger.warning(f"'{event.src}' Duplicate event found '{event.name}'")
        return event

    def remove_event(self, name:str):
        """
        Removes an event with the specified name.

        Arguments
        ---
        `name` - Name of the event to delete.
        """
        try:
            del self._events[name]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_events(self):
        """
        Removes all events from this module.
        """
        try:
            self._events.clear()
        except AttributeError:
            self._events = {}
        return self

    def event(self, name:str=None, description:str=None):
        """
        Creates an event from a regular function.

        Arguments
        ---
        `name` - Name of this event.
        """
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('command function must be a coroutine function')
            return self.add_event(func, name, description)
        return decorator
    
class Version:
    __slots__ = (
        'major',
        'minor',
        'patch'
    )

    def __init__(self, major:int=0, minor:int=0, patch:int=0):
        """
        Describes a pack version using [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
        
        Arguments
        ---
        `major` - version when you make incompatible API changes

        `minor` - version when you add functionality in a backward compatible manner

        `path` - version when you make backward compatible bug fixes

        Methods
        ---
        __str__, __eq__, __le__, __ge__, __lt__, __gt__
        """
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'
    
    def __eq__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
    
    def __le__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) <= (other.major, other.minor, other.patch)

    def __ge__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) >= (other.major, other.minor, other.patch)
    
    def __lt__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
    
    def __gt__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)

def validates(s:str, schema:dict, type:str='json', filename:str='none.json') -> tuple[bool, dict]:
    """
    Tests if instances passes the schema.

    Arguments
    ---
    `fp` - string to JSON or YAML.

    `schema` - The JSON schema to validate with.

    `type` - The type of validation. json, yaml

    `filename` - Name of the file for errors.

    Returns
    `tuple` - Returns a 2 length tuple. The first value is whether it passed the test. The second is the parsed isntance.
    """
    try:
        match type.lower():
            case 'json':  instance = json.loads(s)
            case 'yaml': 
                import yaml
                instance = yaml.safe_load(s)
            case _:
                raise KeyError(f"'{type}' is not a supported validation type. Must be json or yaml")
        jsonschema.validate(instance, schema)
        return (True, instance)
    except json.JSONDecodeError as err:
        logger.warning(f"'{filename}' DecodeError: {err}")
    except jsonschema.ValidationError as err:
        pos = ''
        index=0
        for p in err.absolute_path:
            if isinstance(p, int): pos+=f'[{p}]'
            else:
                if index!=0: pos+='.'
                pos+=str(p)
            index+=1
        att = f" at '{pos}'"
        if pos=='': att = ''
        logger.warning(f"'{filename}' ValidationError: {err.message}"+att)
    except Exception as err:
        logger.warning(f"'{filename}' {err}: {err}")
    
    return False, None

def validate(fp:str, schema:dict, type:str='json') -> tuple[bool, dict]:
    """
    Tests if instances passes the schema. `.read()`

    Arguments
    ---
    `fp` - Path to the JSON file to open and validate.

    `schema` - The JSON schema to validate with.

    `type` - The type of validation. json, yaml

    Returns
    `tuple` - Returns a 2 length tuple. The first value is whether it passed the test. The second is the parsed isntance.
    """
    if os.path.isfile(fp):
        with open(fp, 'r') as r:
            return validates(r.read(), schema, type, fp)

    return (False, None)

# DEPRIVED use App.mimetype
def mimetype(type:str, subtype:str=None):
    def decorator(func):
        return getApp().add_mimetype(func, type, subtype)
    return decorator

# Replace to_json_type, to_schema, and schema with schemiser
def to_schema(cls_or_func, node=None, traits:list=[], root:dict=None, skiparg:int=-1) -> dict:
    """
    Creates a jsonschema from a class or function.

    Arguments
    ---
    `node` - The jsonpack._node.

    `cls_or_func` - A class or function to create a jsonschema from.

    `traits` - A list of traits for this schema. components, events, images.

    `child` - Whether or not this is a child event.

    `skiparg` - Argument index to skip. (used to skip the first CONTEXT arg for nodes and events).
    """
    result = schemaser.to_schema(cls_or_func, root=root, skiparg=skiparg)

    # Inject Components
    if 'components' in traits:
        prop = result['properties']['components']
        if isinstance(node, _node) and prop['type'] == 'object':
            for k,v in node.__components__.items():
                prop['properties'][str(k)] = schemaser.to_schema(v.func, result, skiparg=0)

    # Inject Events
    if 'events' in traits:
        app = getApp()
        prop = result['properties']['events']
        prop['additionalProperties'] = {
            'type': 'object',
            'properties': {},
            'additionalProperties': False
        }
        for k,v in app.events.items():
            prop['additionalProperties']['properties'][str(k)] = schemaser.to_schema(v.func, result, skiparg=0)
            
    return result

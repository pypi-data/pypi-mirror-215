import logging
import jsonpack

def topological_sort(nodes: dict[str, list[str]]) -> list[str]:
    # Calculate the indegree for each node
    indegrees = {k: 0 for k in nodes.keys()}
    for name, dependencies in nodes.items():
        for dependency in dependencies:
            indegrees[dependency] += 1

    # Place all elements with indegree 0 in queue
    queue = [k for k in nodes.keys() if indegrees[k] == 0]

    final_order = []

    # Continue until all nodes have been dealt with
    while len(queue) > 0:

        # node of current iteration is the first one from the queue
        curr = queue.pop(0)
        final_order.insert(0,curr) # add dep at START instead of END.

        # remove the current node from other dependencies
        for dependency in nodes[curr]:
            indegrees[dependency] -= 1

            if indegrees[dependency] == 0:
                queue.append(dependency)

    # check for circular dependencies
    if len(final_order) != len(nodes):
        jsonpack.logger.error('Circular dependency found.')
        jsonpack.exit()
    return final_order

def sortPacks(packs:dict):
    """Sort packs depending on their dpendency"""

    # format
    _packs = {}
    for uuid, p in packs.items():
        _packs[p.uuid] = []
        for dep in p.dependencies:
            _packs[p.uuid].append(dep.uuid)

    # sort
    sorted = topological_sort(_packs)

    # unformat
    sorted_packs = {}
    for uuid in sorted: sorted_packs[uuid] = packs[uuid]
    return sorted_packs

class Cache:
    def __init__(self):
        """
        Used to store values.
        
        Methods
        ---
        append, clear, get
        """
        self.cache = {}

    def append(self, name:str, value):
        """
        Add a new value to cache.
        
        Arguments
        ---
        `name` - Name of the cache to append to.

        `value` - The value of cache to set
        """
        try:
            self.cache[name].append(value)
        except KeyError:
            self.cache[name] = [value]

        return self.get(name, -1)

    def clear(self, name:str):
        """
        Clears all cache in this name.

        Arguments
        ---
        `name` - Name of the cache to clear.
        """
        try:
            self.cache[name].clear()
        except KeyError: pass
        return self

    def get(self, name:str, index:int, default=None):
        """
        Returns the cached value.

        Arguments
        ---
        `name` - Name of the cache.

        `index` - Index in cache to fetch.

        `default` - Default value to return if cache item cannot be found.
        """
        try:
            return self.cache[name][index]
        except IndexError:
            return default
        
class ResourcePath:
    def __init__(self, module_type:str, node_name:str):
        """
        Describes a resrouce path used for annotations.

        Arguments
        ---
        `module_type` - The node type that it should except.

        `node_name` - The node name that is should except.

        Methods
        ---
        exists
        """
        self.module_type = module_type
        self.node_name = node_name

    # def __annotation__(self):
    #     return str

    # TODO
    def exists(self) -> bool:
        """
        Checks if this resource path exists
        """
        raise NotImplementedError()
    
class Context:
    def __init__(self, node, module, **extras):
        """
        Arguments
        ---
        `node` - The node that this context came from.

        `module` - The module that this context came from.

        **extras - Extra arguments to pass.

        Methods
        ---
        add_extras, copy, from_dict, to_dict
        """
        self.logger = logging.getLogger('Unknown') # Fallback logger
        self.node = node
        self.module = module
        self.app = jsonpack.getApp()
        self.add_extras(**extras)

    def add_extras(self, **kw):
        """
        Extra arguments to pass.
        """
        for key, value in kw.items(): setattr(self, str(key), value)
        return self

    def copy(self):
        """
        Creates a copy of this class.
        """
        return self.__class__.from_dict(self.to_dict())
    
    @classmethod
    def from_dict(cls, data:dict):
        """
        Converts a :class:`dict` to a :class:`Context`.
        """
        self = cls.__new__(cls)
        for key, value in data.items():
            setattr(self, str(key), value)
        return self

    def to_dict(self) -> dict:
        """
        Converts a :class:`Context` to a :class:`dict.`
        """
        result = {
            key: getattr(self, key)
            for key in self.__dict__
        }
        return result

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'Context({inner})'

# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashFlow(Component):
    """A DashFlow component.


Keyword arguments:

- children (boolean | number | string | dict | list; optional)

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- clickedEdge (dict; optional)

- clickedNode (dict; optional)

- connectedEdge (dict; optional)

- dagre_direction (string; optional)

- edges (list; optional)

- nodes (list; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_flow_diagrams'
    _type = 'DashFlow'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, nodes=Component.UNDEFINED, edges=Component.UNDEFINED, clickedNode=Component.UNDEFINED, clickedEdge=Component.UNDEFINED, connectedEdge=Component.UNDEFINED, dagre_direction=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'clickedEdge', 'clickedNode', 'connectedEdge', 'dagre_direction', 'edges', 'nodes']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'clickedEdge', 'clickedNode', 'connectedEdge', 'dagre_direction', 'edges', 'nodes']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(DashFlow, self).__init__(children=children, **args)

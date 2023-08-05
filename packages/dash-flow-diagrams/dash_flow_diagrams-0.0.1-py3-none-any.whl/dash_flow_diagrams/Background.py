# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Background(Component):
    """A Background component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional)

- color (string; default "#81818a")

- gap (number; default 16)

- size (number; default 0.5)

- style (dict; optional)

- variant (string; default "dots")"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_flow_diagrams'
    _type = 'Background'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, variant=Component.UNDEFINED, gap=Component.UNDEFINED, size=Component.UNDEFINED, color=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'color', 'gap', 'size', 'style', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'color', 'gap', 'size', 'style', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Background, self).__init__(**args)

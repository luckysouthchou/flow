from cistar_dev.core.generator import Generator

from numpy import pi, sin, cos, linspace


class CircleGenerator(Generator):
    """
    Generator for loop circle used in MIT traffic simulation. Requires from net_params:
     - length: length of the circle
     - lanes: number of lanes in the circle
     - speed_limit: max speed limit of the circle
     - resolution: number of nodes resolution
    """

    def __init__(self, net_params, net_path, cfg_path, base):
        """
        See parent class
        """
        length = net_params["length"]
        lanes = net_params["lanes"]
        self.name = "%s-%dm%dl" % (base, length, lanes)

        super().__init__(net_params, net_path, cfg_path, base)

    def specify_nodes(self, net_params):
        """
        See parent class
        """
        length = net_params["length"]
        r = length / pi

        nodes = [{"id": "bottom", "x": repr(0),  "y": repr(-r)},
                 {"id": "right",  "x": repr(r),  "y": repr(0)},
                 {"id": "top",    "x": repr(0),  "y": repr(r)},
                 {"id": "left",   "x": repr(-r), "y": repr(0)}]

        return nodes

    def specify_edges(self, net_params):
        """
        See parent class
        """
        length = net_params["length"]
        resolution = net_params["resolution"]
        r = length / pi
        edgelen = length / 4.

        edges = [{"id": "bottom", "type": "edgeType",
                  "from": "bottom", "to": "right", "length": repr(edgelen),
                  "shape": " ".join(["%.2f,%.2f" % (r * cos(t), r * sin(t))
                                     for t in linspace(-pi / 2, 0, resolution)])},
                 {"id": "right", "type": "edgeType",
                  "from": "right", "to": "top", "length": repr(edgelen),
                  "shape": " ".join(["%.2f,%.2f" % (r * cos(t), r * sin(t))
                                     for t in linspace(0, pi / 2, resolution)])},
                 {"id": "top", "type": "edgeType",
                  "from": "top", "to": "left", "length": repr(edgelen),
                  "shape": " ".join(["%.2f,%.2f" % (r * cos(t), r * sin(t))
                                     for t in linspace(pi / 2, pi, resolution)])},
                 {"id": "left", "type": "edgeType",
                  "from": "left", "to": "bottom", "length": repr(edgelen),
                  "shape": " ".join(["%.2f,%.2f" % (r * cos(t), r * sin(t))
                                     for t in linspace(pi, 3 * pi / 2, resolution)])}]

        return edges

    def specify_types(self, net_params):
        """
        See parent class
        """
        lanes = net_params["lanes"]
        speed_limit = net_params["speed_limit"]
        types = [{"id": "edgeType", "numLanes": repr(lanes), "speed": repr(speed_limit)}]

        return types

    def specify_routes(self, net_params):
        """
        See parent class
        """
        rts = {"top": ["top", "left", "bottom", "right"],
               "left": ["left", "bottom", "right", "top"],
               "bottom": ["bottom", "right", "top", "left"],
               "right": ["right", "top", "left", "bottom"]}

        return rts

    # TODO: may be able to get rid of all together (replace with routing controller)
    def specify_rerouters(self, net_params):
        """
        See parent class
        """
        rerouting = [{"name": "rerouterTop",    "from": "top",    "route": "routebottom"},
                     {"name": "rerouterBottom", "from": "bottom", "route": "routetop"},
                     {"name": "rerouterLeft",   "from": "left",   "route": "routeright"},
                     {"name": "rerouterRight",  "from": "right",  "route": "routeleft"}]

        return rerouting

class Ns3Vector:
    def __init__(self, textvector):
        elements = textvector.split(':')
        self.x = float(elements[0])
        self.y = float(elements[1])
        self.z = float(elements[2]) if len(elements) > 2 else 0.0

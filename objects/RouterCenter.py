class RouterCenter:
    _instance = None

    @staticmethod
    def get_instance():
        if RouterCenter.__instance is None:
            RouterCenter()
        return RouterCenter.__instance

    def __init__(self):
        if RouterCenter.__instance is not None:
            raise Exception("RouterCenter is a singleton class!")
        RouterCenter.__instance = self
        self.routers = {}

    def add_router(self, router):
        for ip in router.ips:
            self.routers[ip] = router

    def get_routers(self):
        return self.routers
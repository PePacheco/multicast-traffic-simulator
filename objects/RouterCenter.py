class RouterCenter:
    __instance = None

    @staticmethod
    def get_instance():
        if RouterCenter.__instance is None:
            RouterCenter()
        return RouterCenter.__instance

    def __init__(self):
        if RouterCenter.__instance is not None:
            raise Exception("RouterCenter is a singleton class!")
        else:
            RouterCenter.__instance = self
        self.routers = {}

    def add_router(self, router):
        self.routers[router.ip] = router

    def get_routers(self):
        return self.routers
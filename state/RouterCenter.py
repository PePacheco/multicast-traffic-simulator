class RouterCenter:
    _instance = None
    routers = {}

    @staticmethod
    def get_instance():
        if RouterCenter._instance is None:
            RouterCenter._instance = RouterCenter()
        return RouterCenter._instance

    def _init_(self):
        if RouterCenter._instance is not None:
            raise Exception("RouterCenter is a singleton class!")
        RouterCenter._instance = self


    def add_router(self, router):
        for ip in router.ips:
            self.routers[ip] = router

    def get_routers(self):
        return self.routers
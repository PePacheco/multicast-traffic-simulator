class RouterCenter:
    _instance = None
    routers = {}
    router_ids: str = []

    @staticmethod
    def get_instance():
        if RouterCenter._instance is None:
            RouterCenter._instance = RouterCenter()
        return RouterCenter._instance



    def _init_(self):
        if RouterCenter._instance is not None:
            raise Exception("RouterCenter is a singleton class!")
        RouterCenter._instance = self

    def add_router_id(self, rid):
        self.router_ids.append(rid)

    def add_router(self, router):
        for ip in router.ips:
            ip_without_mask = ip
            self.routers[ip_without_mask] = router        

    def get_routers(self):
        return self.routers
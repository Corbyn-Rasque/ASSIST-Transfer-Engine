from sources.adapter.base           import Adapter

 #import Availability, Area, Categories
import sources.web.transferrability as web

import models.transferrability as model

class Availability(Adapter[web.Availability, model.Availability]):
    def adapt(self, source: web.Availability) -> model.Availability:



        
        return model.Availability()